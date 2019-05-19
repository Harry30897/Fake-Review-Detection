import sys

meta_file = sys.argv[1]
user = {}


def product_count():
    product = {}
    with open(meta_file, 'r') as mfile:
        for line in mfile:
            line = line.split(" ")
            if line[3] not in product.keys():
                product[line[3]] = {'count' : 1}
            else:
                product[line[3]]['count'] += 1
    return product

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



"""def user_trust_rating():
    with open(meta_file, 'r') as mfile:
        for line in mfile:
            line = line.split(" ")
            if line[2] not in user.keys():
                user[line[2]] = {'count': 1}
                if line[4] == 'N':
                    user[line[2]]['tcount'] = 1
            else:
                user[line[2]]['count'] += 1
                if line[4] == 'N':
                    user[line[2]]['tcount'] += 1
            print(user)        
            user[line[2]]['trust_rating'] = user[line[2]]['tcount'] / user[line[2]]['count']
            print(user[line[2]]['trust_rating'])
            break"""



def goodness_of_restaurant():
    with open(meta_file, 'r') as mfile:
        for line in mfile:
            line = line.split(" ")
            if line[3] not in product.keys():
                product[line[3]]['summison'] = line[8] * reviewer_dict[row[line[2]]]['genuine'] / row['total_reviews']
            else:
                product[line[3]]['summison'] += line[8] * reviewer_dict[row[line[2]]]['genuine'] / row['total_reviews']
            product[line[3]]['goodness'] = product[line[3]]['summison'] / product[line[3]]['count']
            break
user_trust_rating()
goodness_of_restaurant()



