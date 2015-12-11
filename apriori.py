import sys
from itertools import chain, combinations
from collections import defaultdict
#from optparse import OptionParser
import argparse

#Returns items t
#itemsets = set of all items
#transactions = list of all sets of transactions
#itemsetFreqs = frequency of each itemset in transaction list
#
def get_supported_items(itemsets, transactions, minSup, itemsetFreqs):
        minSupSet = set()
        nTransactions = len(transactions)
        theseFreaks = defaultdict(int)

        for itemset in itemsets:
                for transaction in transactions:
                        if itemset.issubset(transaction):
                                itemsetFreqs[itemset] += 1
                                theseFreaks[itemset] += 1

        for itemset, freq in theseFreaks.items():
                if float(freq)/nTransactions >= minSup:
                        minSupSet.add(itemset)

        return minSupSet

#Return all k-element itemsets that are a subset of items
#
def get_k_subset(items, k):
        return set([i.union(j) for i in items for j in items if len(i.union(j)) == k])


#Based on a generator expression that yields frozensets of transactions,
#return the corresponding itemset and list of transactions
#
def get_items_and_transactions(lineGen):
    transactionList = []
    itemSet = set()
    for line in lineGen:
        transaction = frozenset(line)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList

#APRIORI algorithm
#
def apriori(itemSet, transactionList, minSupport, minConfidence):
    itemsetFreqs = defaultdict(int)

    #Maps size to itemset, itemsets must have sup > minSup
    #
    L = dict()
    Ci = get_supported_items(itemSet, transactionList, minSupport, itemsetFreqs)
    Li = Ci

    k = 2
    while(Li != set([])):
        L[k-1] = Li
        Li = get_k_subset(Li, k)

        Ci = get_supported_items(Li, transactionList, minSupport, itemsetFreqs)
        Li = Ci

        k = k + 1

    def getSupport(item):
            return float(itemsetFreqs[item])/len(transactionList)
    supportedItems = []
    for key, itemsets in L.items():
        supportedItems.extend([(tuple(itemset), getSupport(itemset)) for itemset in itemsets])

    #Get non-empty subsets of array itemset
    #
    def subsets(itemset):
        return chain(*[combinations(itemset, i + 1) for i in range(len(itemset))])

    associationRules = []
    for key, k_itemsets in L.items()[1:]:
        #k_itemsets = k-itemsets in L[key]
        #
        for itemset in k_itemsets:
            #Subsets of elements in k_itemset
            #
            _subsets = map(frozenset, [x for x in subsets(itemset)])
            for cause in _subsets:
                #Remove antecedent from association rule
                #
                effect = itemset.difference(cause)
                #Retrieve non-trivial associations
                #
                if len(effect) > 0:
                    confidence = getSupport(itemset)/getSupport(cause)
                    if confidence >= minConfidence:
                        associationRules.append(((tuple(cause), tuple(effect)), confidence))

    return supportedItems, associationRules

#Returns a generator that outputs a frozenset() representing each transaction
#
#files = list of files to read in from to generate transactions
#
def get_transaction_gen_from_files(filenames, window_size):
    import algorithm
    algorithm.init_hard_coded_complex_to_simple_map()

    for filename in filenames:
        n_lines = 0
        cur_transaction = []
        with open(filename, 'rU') as f:
            for line in f:
                complex_query = line.strip().rstrip(',')
                cur_transaction.append(algorithm.complex_to_simple_map[complex_query])

                n_lines += 1
                if n_lines >= window_size:
                    yield frozenset(cur_transaction)
                    _ = cur_transaction.pop(0)

        while len(cur_transaction) >= 2:
            yield frozenset(cur_transaction)
            _ = cur_transaction.pop(0)


def parse_options():
    optparser = argparse.ArgumentParser()
    optparser.add_argument('-l', '--fileList',
                        dest='fileList',
                        help='Filenames containing APRIORI training data',
                        nargs='+',
                        default=None)
    optparser.add_argument('-s', '--minSupport',
                         dest='minS',
                         help='Min support value',
                         default=0.15,
                         type=float)
    optparser.add_argument('-c', '--minConfidence',
                         dest='minC',
                         help='Min confidence value',
                         default=0.6,
                         type=float)
    optparser.add_argument('-w', '--windowSize',
                         dest='windowSize',
                         help='Window size for apriori',
                         default=3,
                         type=int)
    return optparser.parse_args()

#Output to file & association rules
#
def write_results(outfile_name, associationRules):
    with open(outfile_name, 'w') as f:
        for rule, confidence in associationRules:
            cause, effect = rule
            if len(cause) > 1:
                continue

            wholeset = set(cause + effect)
            rule_size = len(wholeset)

            f.write(str(rule_size) + "\n")
            f.write(str(cause[0]) + "\n")
            for associated_element in set(effect):
                f.write(str(associated_element) + "\n")

if __name__ == "__main__":
    options = parse_options()
    infile_gen = None
    if options.fileList is None:
        print "No input file(s) specified. Exiting"
        sys.exit(0)

    if options.fileList is not None:
        print options.fileList
        infile_gen = get_transaction_gen_from_files(options.fileList, options.windowSize)

    min_support = options.minS
    min_confidence = options.minC

    item_set, transaction_list = get_items_and_transactions(infile_gen)
    supported_items, association_rules = apriori(item_set, transaction_list, min_support, min_confidence)

    write_results("../apriori_out.txt", association_rules)
