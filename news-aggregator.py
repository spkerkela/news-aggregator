import nltk
import os
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from goose3 import Goose
from hashlib import md5
urls = []
with open("urls.txt") as urlfile:
    urls = [line.strip() for line in urlfile.readlines()]
g = Goose()
ps = PorterStemmer()
def hasher(string):
    m = md5()
    m.update(string.encode("utf-8"))
    return m.hexdigest()

stop_words = set(stopwords.words("english"))

def summarize(url):
    article = g.extract(url=url)
    text = article.cleaned_text
    words = word_tokenize(text)
    freq_table = dict()
    for word in words:
        word = ps.stem(word.lower())
        if len(word) < 2:
            continue
        if word in stop_words:
            continue
        if word in freq_table:
            freq_table[word] += 1
        else:
            freq_table[word] = 1
    sentences = list(dict.fromkeys(sent_tokenize(text)))
    sentence_value = dict()
    for sentence in sentences:
        for word_value in freq_table:
            value = freq_table[word_value]
            if word_value in sentence.lower():
                hash_val = hasher(sentence)
                if hash_val in sentence_value:
                    sentence_value[hash_val] += value
                else:
                    sentence_value[hash_val] = value

    sum_values = 0
    for sentence in sentence_value:
        sum_values += sentence_value[sentence]
    average = int(sum_values / len(sentence_value))
    summary = ''
    for sentence in sentences:
        hash_val = hasher(sentence)
        if hash_val in sentence_value and sentence_value[hash_val] > (1.5 * average):
            summary += " " + sentence
    filename = "output/" + hasher(article.title) + '.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename, 'w')
    print(len(text), len(summary))
    if len(summary) > 0:
        f.write(article.title+'\n')
        f.write(summary)


for url in urls:
    summarize(url)
