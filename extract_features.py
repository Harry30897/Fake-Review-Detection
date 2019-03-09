import sys
import csv


filename = sys.argv[1]
with open(filename, 'r') as file:
    for line in csv.reader(file, dialect='excel-tab'):
        print(line)
        break
