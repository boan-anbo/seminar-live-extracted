from typing import List

from pypinyin import pinyin, lazy_pinyin


def name_to_pinyin(words: str) -> str:
    return ''.join(lazy_pinyin(words)).capitalize()

if __name__ == '__main__':
    result = name_to_pinyin("吕叔湘")
    print(result)



