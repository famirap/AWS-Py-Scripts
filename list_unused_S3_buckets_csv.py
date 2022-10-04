import csv

# Creating the list of buckets
with open(r'report.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        bucketlist = []
        for row in csvreader:
                if len(row) > 2:
                        if row[1] == 'GetObject':
                                bucketlist.append(row[3])
                        if row[1] == 'PutObject':
                                bucketlist.append(row[3])

# Deduping the list of buckets
dedupedlist = list(set(bucketlist))
dedupedlist.sort()
print(*dedupedlist, sep = "\n")