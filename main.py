"""
Keyword extractor
By Tal D.
"""

import re
import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/Special:Random"


def main():
    filtered_text = extract_text_from_url(URL)
    word_count_dict = count_words_in_list(filtered_text)
    keywords_dict = extract_keywords_from_dict(word_count_dict)
    print(keywords_dict)

    top_10 = list(keywords_dict.keys())[:10]
    print("Suggested keywords: ", top_10)


def extract_text_from_url(url):
    # TODO prevent css keywords from getting in
    content = requests.get(url).text
    soup = BeautifulSoup(content, "html.parser")
    print("From: ", soup.title.string)
    text = soup.get_text().rstrip()
    text = re.split('\'|\s', text)
    filtered_text = list(filter(lambda word: word.isalnum(), text))
    return filtered_text


def count_words_in_list(word_list):
    word_list.sort()
    word_count_dict = {}

    for raw_word in word_list:
        word = raw_word.capitalize()
        if word not in word_count_dict.keys():
            if word[:-1] in word_count_dict.keys():
                word_count_dict[word[:-1]] += 1
            else:
                word_count_dict[word] = 1
        else:
            if word[:-1] in word_count_dict.keys():
                word_count_dict[word[:-1]] += 1
            else:
                word_count_dict[word] += 1

    return word_count_dict


def extract_keywords_from_dict(word_count_dict):
    # TODO pay more attention to words in h1, h2 and h3 titles
    sorted_word_dict = sorted(word_count_dict.items(), key=lambda key_value: key_value[1], reverse=True)

    with open("blacklist", 'r') as file:
        common_words = [word.strip() for word in file.readlines()]

    keywords = {}

    for word, count in sorted_word_dict:
        if word.lower() not in common_words:
            if count > 1 and len(word) > 1:
                keywords[word] = count

    return keywords


if __name__ == '__main__':
    main()
