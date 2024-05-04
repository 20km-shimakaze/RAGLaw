import datasets
from datasets import Dataset
from tqdm import tqdm


def load_datasets(path: str):
    """
    加载datasets数据
    :param path:
    :return:
    """
    datasets_data = datasets.load_dataset(path)
    return datasets_data


def splice_prompt(data: list, prompt_type: str):
    """
    从字典数据组合为prompt句子
    :param data:
    :param prompt_type:
    :return:
    """
    content = []
    data_list = range(len(data))
    if prompt_type == 'law_book':
        data_name = ['type', 'title', 'chapter1', 'chapter2', 'chapter3', 'content']
        for i in tqdm(data_list, desc="Processing items"):
            sentence = []
            for name in data_name:
                data_str = data[i][name]
                if data_str != '' and data_str is not None:
                    if name == 'content':
                        sentence.append(':\n')
                        sentence.append(data_str)
                    else:
                        sentence.append(data_str)
                        sentence.append(' ')
            content.append(''.join(sentence))
    else:
        raise TypeError(f"Unexpected prompt_type: expected 'law_book', got {prompt_type}")
    return content


if __name__ == '__main__':
    data = load_datasets('./law_data/law_book')['train']
    law_book = []
    data_list = len(data)
    for i in tqdm(data, desc="233"):
        law_book.append(i)
    ans = splice_prompt(law_book, "law_book")
    print(ans[:3])
