import sys

meta_file = sys.argv[1]
user = {}
product = {}

def user_trust_rating():
	with open(meta_file, 'r') as mfile:
		for line in mfile:
			line = line.split(" ")
			if line[2] not in user.keys():
				user[line[2]] = { 'count': 1}
				if line[4] == 'N':
					user[line[2]] = {'tcount' : 1 }
			else:
				user[line[2]]['count'] += 1
				if line[4] == 'N':
					user[line[2]]['tcount'] += 1 
			user[line[2]]['trust_rating'] = user[line[2]]['tcount']/user[line[2]]['count'] 
			print(user[line[2]]['trust_rating'])
			break

def goodness_of_restaurant():
	with open(meta_file, 'r') as mfile:
		for line in mfile:
			line = line.split(" ")
			if line[3] not in product.keys():
				product[line[3]]['summison'] = line[8]*user[line[2]]['trust_rating']
			else:
				product[line[3]]['summison'] += line[8]*user[line[2]]['trust_rating']
			product[line[3]]['goodness'] = product[line[3]]['summison']/100 		
			break

	 			
	 				



