import torch
from torch import nn
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import numpy

# tokenizer = AutoTokenizer.from_pretrained('./model')
# model = AutoModelForCausalLM.from_pretrained('./model')
# text = "Replace me by any text you'd like."
# encoded_input = tokenizer(text, return_tensors='pt')
# # print(encoded_input[0].shape)
# output = model(**encoded_input)

device = "cuda:0"

train_data = pd.read_csv('./data/train.csv')
test_data = pd.read_csv('./data/test.csv')
train_label = pd.get_dummies(train_data['target'], prefix='encode').iloc[:, :].values
print(train_label[:5])

train_fea = train_data['text'].tolist()
test_fea = test_data['text'].tolist()
# train_label = train_data['target'].tolist()

tokenizer = AutoTokenizer.from_pretrained('./model')
train_data_fea = tokenizer(train_fea, return_tensors='pt', padding=True)
test_data_fea = tokenizer(test_fea, return_tensors='pt', padding=True)


class MyDataset(Dataset):
    def __init__(self):
        self.train_fea_input_ids = train_data_fea['input_ids']
        self.train_fea_token_type_ids = train_data_fea['token_type_ids']
        self.train_fea_attention_mask = train_data_fea['attention_mask']
        self.train_label = torch.tensor(train_label, dtype=torch.float32, device=device)

    def __len__(self):
        return len(self.train_fea_input_ids)

    def __getitem__(self, item):
        return self.train_fea_input_ids[item], self.train_fea_token_type_ids[item], \
            self.train_fea_attention_mask[item], self.train_label[item]


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.bert = AutoModelForCausalLM.from_pretrained('./model')
        self.seq = nn.Sequential(
            nn.Flatten(),
            nn.Linear(30522, 5120), nn.ReLU(),
            nn.Linear(5120, 1024), nn.ReLU(),
            nn.Linear(1024, 128), nn.ReLU(),
            nn.Linear(128, 16), nn.ReLU(),
            nn.Linear(16, 2)
        )

    def forward(self, input_ids, token_type_ids, attention_mask):
        # 数据 第一个句子 [cls]
        # print(token)
        token = self.bert(input_ids=input_ids, token_type_ids=token_type_ids, attention_mask=attention_mask)[0][:, 0, :]
        return self.seq(token)


dataloader = DataLoader(dataset=MyDataset(), batch_size=64, shuffle=False)

net = Net().to(device)
loss = nn.CrossEntropyLoss()


def train(epochs, lr, weight_decay):
    net.train()
    optim = torch.optim.SGD(net.parameters(), lr=lr, weight_decay=weight_decay)
    for epoch in range(epochs):
        loss_all = 0
        net.train()
        for X1, X2, X3, y in dataloader:
            X1 = X1.to(device)
            X2 = X2.to(device)
            X3 = X3.to(device)
            y = y.to(device)
            optim.zero_grad()
            predict = net(X1, X2, X3).to(torch.float32)
            # print(f'predict:\n{predict[:3]}')
            # print(f'y:\n{y[:3]}')
            # print(f'predict:\n{predict}')
            l = loss(predict, y)
            # print(f'loss:\n{l}')
            l.sum().backward()
            optim.step()
            loss_all += l.sum()
        print(f'loss_all: {loss_all}')

    # get answer
    net.eval()
    predict = []
    idx = 0
    st = 200
    while True:
        if idx >= len(test_data):
            break
        pre = net(test_data_fea['input_ids'][idx:idx+st].to(device), test_data_fea['token_type_ids'][idx:idx+st].to(device), test_data_fea['attention_mask'][idx:idx+st].to(device)).tolist()
        idx += st
        print(pre)
        predict += pre
    # predict = net(test_data_fea['input_ids'].to(device), test_data_fea['token_type_ids'].to(device), test_data_fea['attention_mask'].to(device))
    # answer = [1 if x > 0.5 else 0 for x in predict]
    print(f'pre:{predict[:3]}')
    answer = numpy.argmax(predict, axis=1)
    print(len(answer), len(test_data['id'].tolist()))
    submission = {'id': test_data['id'].tolist(), 'target': answer}
    df = pd.DataFrame(submission)
    df.to_csv('submission.csv', index=False)


if __name__ == '__main__':
    train(20, 0.001, 0.15)
