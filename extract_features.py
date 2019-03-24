import sys
import csv
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
    file_name = sys.argv[1]
    df = pd.DataFrame(
        columns=['Content', 'Length', 'C_Letters', 'C_Words', 'F_Pronouns']
    )
    with open(file_name, 'r') as file:
        for line in csv.reader(file, dialect='excel-tab'):
            new_row = {}
            new_row['Content'] = line[3]
            new_row['Length'] = total_length(line[3])
            new_row['C_Letters'] = capital_letters(line[3])
            new_row['C_Words'] = capital_words(line[3])
            new_row['F_Pronouns'] = count_first_pronouns([line[3]])
            df.append(new_row, ignore_index=True)
    df.to_csv('features.csv')


if __name__ == '__main__':
    main()
