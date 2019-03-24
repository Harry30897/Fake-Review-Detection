import sys
import csv
from datetime import datetime as dt
from math import ceil
import pandas as pd


first_pronouns = [
    'i', 'me', 'we', 'us',
    'myself', 'ourselves',
    'mine', 'my', 'our', 'ours'
]


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
    return ceil(float(count / len(review)) * 100) / 100.0


def count_first_pronouns(review):
    review = review.split(" ")
    count = 0
    for word in review:
        if word.lower() in first_pronouns:
            count += 1
    return count


def main():
    content_file, meta_file = sys.argv[1], sys.argv[2]
    columns = [
        'reviewID',
        'reviewerID',
        'length',
        'c_letters',
        'c_words',
        'f_pronouns',
        'rating',
        'label'
    ]
    features = pd.DataFrame(
        columns=columns
    )
    count = 0
    with open(content_file, 'r') as reviews, open(meta_file, 'r') as meta_data:
        rows = []
        for review, meta in zip(reviews, meta_data):
            new_row = {}
            meta = meta.split(' ')
            new_row['reviewID'] = meta[1]
            new_row['reviewerID'] = meta[2]
            new_row['length'] = total_length(review)
            new_row['c_letters'] = capital_letters(review)
            new_row['c_words'] = capital_words(review)
            new_row['f_pronouns'] = count_first_pronouns(review)
            new_row['rating'] = meta[8]
            new_row['label'] = meta[4]
            rows.append(new_row)
            count += 1
            print('Extracted: {}'.format(count), end='\r')
    features = features.append(rows, ignore_index=True)
    features = features.set_index('reviewID')
    features.to_csv('features.csv')


if __name__ == '__main__':
    main()
