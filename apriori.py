import sys
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

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
        for itemset in k_itemsets:
            _subsets = map(frozenset, [x for x in subsets(itemset)])
            for cause in _subsets:
                effect = itemset.difference(cause)
                if len(effect) > 0:
                    confidence = getSupport(itemset)/getSupport(cause)
                    if confidence >= minConfidence:
                        associationRules.append(((tuple(cause), tuple(effect)), confidence))

    return supportedItems, associationRules

#Print supported itemsets & association rules
#
def print_results(supportedItems, associationRules):
    #supportedItems: list of tuples of the form ((itemset), support) with min support
    #
    for item, support in sorted(supportedItems, key=lambda (item, support): support):
        print "item: %s , %.3f" % (str(item), support)
    print "\n------------------------ RULES:"
    
    #associationRules: list of tuples in the form (((if), (then)), confidence)
    #
    for rule, confidence in sorted(associationRules, key=lambda (rule, confidence): confidence):
        pre, post = rule
        print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence)


def get_transaction_generator(fname):
        f = open(fname, 'rU')
        for line in f:
            line = line.strip().rstrip(',')                         # Remove trailing comma
            transaction = frozenset(line.split(','))
            yield transaction

def parseOptions():
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')
    return optparser.parse_args()

if __name__ == "__main__":
    (options, args) = parseOptions()    
    infileGen = None
    if options.input is not None:
        infileGen = get_transaction_generator(options.input)
    else:
        print 'No input file specified\n'
        sys.exit(0)
    minSupport = options.minS
    minConfidence = options.minC

    itemSet, transactionList = get_items_and_transactions(infileGen)
    supportedItems, associationRules = apriori(itemSet, transactionList, minSupport, minConfidence)
    print_results(supportedItems, associationRules)
