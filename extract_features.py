import sys
import csv
import re
from math import ceil
import pandas as pd


first_pronouns = [
    'i', 'me', 'we', 'us',
    'myself', 'ourselves',
    'mine', 'my', 'our', 'ours'
]


def total_length(review):
    return len(review)


def avg_word_length(review):
    return ceil(sum(len(word) for word in review) / len(review) * 100) / 100.0


def capital_letters(review):
    count = 0
    for word in review:
        if not word.islower():
            count += 1
    return ceil(float(count / len(review)) * 100) / 100.0


def capital_words(review):
    count = 0
    for word in review:
        if word.isupper():
            count = count + 1
    return ceil(float(count / len(review)) * 100) / 100.0


def count_first_pronouns(review):
    count = 0
    for word in review:
        if word.lower() in first_pronouns:
            count += 1
    return count


def create_reviewer_dict(filename):
    reviewers = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.split(' ')
            if line[2] not in reviewers.keys():
                reviewers[line[2]] = {'count': 1}
                reviewers[line[2]][line[0]] = line[8]
            else:
                reviewers[line[2]]['count'] += 1
                if line[0] not in reviewers[line[2]].keys():
                    reviewers[line[2]][line[0]] = line[8]
                else:
                    if int(line[8]) > int(reviewers[line[2]][line[0]]):
                        reviewers[line[2]][line[0]] = line[8]
    return reviewers


def main():
    content_file, meta_file = sys.argv[1], sys.argv[2]
    columns = [
        'reviewID',
        'reviewerID',
        'length',
        'avg_w_len',
        'c_letters',
        'c_words',
        'f_pronouns',
        'rating',
        # 'word_num_avg',
        'total_reviews',
        # 'rating_var',
        'max_rating',
        'label'
    ]
    features = pd.DataFrame(
        columns=columns
    )
    count = 0
    reviewer_dict = create_reviewer_dict(meta_file)
    with open(content_file, 'r') as reviews, open(meta_file, 'r') as meta_data:
        rows = []
        for review, meta in zip(reviews, meta_data):
            new_row = {}
            meta = meta.split(' ')
            review = re.sub(r'\W+', ' ', review)
            review = review.split(' ')
            new_row['reviewID'] = meta[1]
            new_row['reviewerID'] = meta[2]
            new_row['length'] = total_length(review)
            new_row['avg_w_len'] = avg_word_length(review)
            new_row['c_letters'] = capital_letters(review)
            new_row['c_words'] = capital_words(review)
            new_row['f_pronouns'] = count_first_pronouns(review)
            new_row['rating'] = meta[8]
            # new_row['word_num_avg'] = reviewer_dict[meta[2]][0]
            new_row['total_reviews'] = reviewer_dict[meta[2]]['count']
            # new_row['rating_var'] = reviewer_dict[meta[2]][0]
            new_row['max_rating'] = reviewer_dict[meta[2]][meta[0]]
            new_row['label'] = meta[4]
            rows.append(new_row)
            count += 1
            print('Extracted: {}'.format(count), end='\r')
    features = features.append(rows, ignore_index=True)
    features = features.set_index('reviewID')
    features.to_csv('features.csv')


if __name__ == '__main__':
    main()
