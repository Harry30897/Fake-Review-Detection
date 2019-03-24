
userid_file_name = sys.argv[1]


def total_number_of_reviews():
    with open(userid_file_name, 'r') as ufile:
        total_count = {}
        for line in ufile:
            line = line.split(" ")
            if line[2] not in total_count.keys():
                total_count[line[2]] = 1  
            else: 
                total_count[line[2]] += 1
        print(total_count)


def maximum_rating():
    with open(userid_file_name, 'r') as ufile:
        max_rating = {}
        for line in ufile:
            line = line.split(" ")
            if line[2] not in max_rating.keys():
                max_rating[line[2]] = {line[0]:line[8]}  
            else: 
                if line[0] not in max_rating[line[2]].keys():
                    max_rating[line[2]][line[0]] = line[8]
                else:
                    if line[8] > max_rating[line[2]][line[0]]:
                        max_rating[line[2]][line[0]] = line[8]
        print(max_rating)        