import datasets
from datasets import Dataset


def load_datasets(path: str):
    """
    加载datasets数据
    :param path:
    :return:
    """
    datasets_data = datasets.load_dataset(path)
    return datasets_data


def splice_prompt(data: dict, prompt_type: str):
    """
    从字典数据组合为prompt句子
    :param data:
    :param prompt_type:
    :return:
    """
    content = []
    if prompt_type == 'law_book':
        data_name = ['type', 'title', 'chapter1', 'chapter2', 'chapter3', 'content']
        for i in range(len(data)):
            sentence = []
            for name in data_name:
                data_str = data[name][i]
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
    data = load_datasets('../law_data/law_book')['train'][:10]
    splice = splice_prompt(data, 'law_book')
    print(splice)
