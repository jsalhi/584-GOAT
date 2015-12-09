import random
import sys

how_many_numbers = 10
min_range = 0
max_range = 29

rand_indices = [random.randint(min_range, max_range) for _ in range(how_many_numbers)]

if len(sys.argv) < 3:
    sys.exit("Must pass in input then output file")

all_queries = []
with open(sys.argv[1]) as f:
    for query in f:
        all_queries.append(query.strip())

random_queries = []
for ri in rand_indices:
    random_queries.append(all_queries[ri])

with open(sys.argv[2], 'w') as output_file:
    for query in random_queries:
        output_file.write(query+'\n')
