import sys
import csv
from math import ceil


first_pronouns = ['i', 'me', 'we', 'us', 'myself', 'ourselves', 'mine', 'my', 'our', 'ours']


def total_length(review):
    review = review.split(" ")
    return len(review)


def capital_letters(review):
    review = review.split(" ")
    count = 0
    for word in review:
        if not word.islower():
            count += 1
    return ceil(float(count / len(review)) * 100) / 100.0


def capital_words(review):
    review = review.split(" ")
    count = 0
    for word in review:
        if word.isupper():
            count = count + 1
    return ceil(float(count/len(review)) * 100) / 100.0


def count_first_pronouns(review):
    review = review.split(" ")
    count = 0
    for word in review:
        if word.lower() in first_pronouns:
            count += 1
    return count        

filename = sys.argv[1]
with open(filename, 'r') as file:
    for line in csv.reader(file, dialect='excel-tab'):
        print('Content: ', line[3])
        print('Total Length: ', total_length(line[3]))
        print('Capital Letter Ratio: ', capital_letters(line[3]))
        print('Capital Words Ratio: ', capital_words(line[3]))
        print('Pronouns Count', count_first_pronouns(line[3]))
        break


