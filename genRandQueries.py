import random

how_many_numbers = 10
min_range = 0
max_range = 29

rand_indices = [random.randint(min_range, max_range) for _ in range(how_many_numbers)]

all_queries = []
with open('AllQueries.txt') as f:
    for query in f:
        all_queries.append(query.strip())

random_queries = []
for ri in rand_indices:
    random_queries.append(all_queries[ri])
