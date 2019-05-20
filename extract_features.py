import sys
import re
from math import ceil
import pandas as pd
import logging

logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)

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
            rating = int(line[8])
            if line[2] not in reviewers.keys():
                reviewers[line[2]] = {'count': 1}
                reviewers[line[2]][line[0]] = rating
                if rating > 3:
                    reviewers[line[2]]['positive'] = 1
                    reviewers[line[2]]['negative'] = 0
                else:
                    reviewers[line[2]]['positive'] = 0
                    reviewers[line[2]]['negative'] = 1
                if line[4] == 'N':
                    reviewers[line[2]]['genuine'] = 1
                else:
                    reviewers[line[2]]['genuine'] = 0
            else:
                reviewers[line[2]]['count'] += 1
                if rating > 3:
                    reviewers[line[2]]['positive'] += 1
                else:
                    reviewers[line[2]]['negative'] += 1
                if line[4] == 'N':
                    reviewers[line[2]]['genuine'] += 1
                if line[0] not in reviewers[line[2]].keys():
                    reviewers[line[2]][line[0]] = int(line[8])
                else:
                    if int(line[8]) > int(reviewers[line[2]][line[0]]):
                        reviewers[line[2]][line[0]] = int(line[8])
    return reviewers


def main():
    content_file, meta_file = sys.argv[1], sys.argv[2]

    columns = [
        'reviewID',
        'reviewerID',
        'productID',
        'length',
        'avg_w_len',
        'c_letters',
        'c_words',
        'f_pronouns',
        'rating',
        'word_num_avg',
        'total_reviews',
        # 'rating_var',
        'max_rating',
        'positive_ratio',
        'negative_ratio',
        'trust_rating',
        'goodness_rating',
        'label'
    ]

    features = pd.DataFrame(
        columns=columns
    )

    count = 0
    reviewer_dict = create_reviewer_dict(meta_file)

    with open(content_file, 'r') as reviews, open(meta_file, 'r') as meta_data:
        rows = []
        logging.info('processing reviews now...')
        for review, meta in zip(reviews, meta_data):
            new_row = {}
            meta = meta.split(' ')
            review = re.sub(r'\W+', ' ', review)
            review = review.split(' ')
            new_row['reviewID'] = meta[1]
            new_row['reviewerID'] = meta[2]
            new_row['productID'] = meta[3]
            new_row['length'] = total_length(review)
            new_row['avg_w_len'] = avg_word_length(review)
            new_row['c_letters'] = capital_letters(review)
            new_row['c_words'] = capital_words(review)
            new_row['f_pronouns'] = count_first_pronouns(review)
            new_row['rating'] = int(meta[8])
            new_row['word_num_avg'] = None  # reviewer_dict[meta[2]][0]
            new_row['total_reviews'] = reviewer_dict[meta[2]]['count']
            # new_row['rating_var'] = None  # reviewer_dict[meta[2]][0]
            new_row['max_rating'] = reviewer_dict[meta[2]][meta[0]]
            new_row['positive_ratio'] = 0.0
            new_row['negative_ratio'] = 0.0
            new_row['trust_rating'] = 0.0
            new_row['goodness_rating'] = 0.0
            new_row['label'] = meta[4]
            rows.append(new_row)
            count += 1
            if count % 10000 == 0:
                logging.info('processed review # {}'.format(count))
        logging.info('processed {} reviews'.format(count))

    features = features.append(rows, ignore_index=True)
    features = features.set_index('reviewID')

    logging.info('processing reviewers now...')
    c = 0
    for idx in features.reviewerID:
        if 'avg' not in reviewer_dict[idx].keys():
            t = features[features['reviewerID'] == idx].length
            r = features[features['reviewerID'] == idx].rating
            reviewer_dict[idx]['avg'] = sum(t) / len(t)
            reviewer_dict[idx]['ratings'] = list(r)
            c += 1
            if c % 1000 == 0:
                logging.info('processed reviewer # {}'.format(c))
    logging.info('processed {} reviewrs'.format(c))

    for index, row in features.iterrows():
        v = reviewer_dict[row['reviewerID']]['avg']
        features.at[index, 'word_num_avg'] = v
        tr = row['total_reviews']
        pr = reviewer_dict[row['reviewerID']]['positive'] / tr
        nr = reviewer_dict[row['reviewerID']]['negative'] / tr
        rr = reviewer_dict[row['reviewerID']]['genuine'] / tr
        features.at[index, 'positive_ratio'] = pr
        features.at[index, 'negative_ratio'] = nr
        features.at[index, 'trust_rating'] = rr

    logging.info('computing product ratings...')
    products = {}
    with open(meta_file, 'r') as file:
        c = 0
        for line in file:
            line = line.split(' ')
            ur = features[features.index == line[1]]['trust_rating']
            if line[3] not in products.keys():
                products[line[3]] = {'count': 1}
                products[line[3]]['sum'] = float(int(line[8]) * ur)
            else:
                products[line[3]]['count'] += 1
                products[line[3]]['sum'] += float(int(line[8]) * ur)
            products[line[3]]['goodness'] = float(products[line[3]]['sum'] / products[line[3]]['count'])
            c += 1
            print('at product # {}'.format(c), end='\r')

    for index, row in features.iterrows():
        p = row['productID']
        features.at[index, 'goodness_rating'] = products[p]['goodness']

    logging.info('saving features to disk')
    features.to_csv('features.csv')


if __name__ == '__main__':
    main()
