class Node:
    def __init__(self, test = None):
        self.test = test    
        self.branch = {}


def entropy(examples):
    sum = 0
    for example in set(examples):
        p = examples.count(example)/len(examples)
        sum += -p*log2(p)
    return sum


def gain(examples, attribute):
    return entropy(examples[10]) - Remainder(examples, attribute)


def Remainder(examples, attribute):
    sum = 0
    for k in set(examples[attribute]): 
        sum += (examples[attribute].count(k)/len(examples[attribute]))*entropy([j for i,j in zip(examples[attribute], examples[10]) if i == k]) 
    return sum

def imp_attribute(examples, attributes):
    max = -999999
    for attribute in attributes:
        if max<gain(examples, attribute):
            max = gain(examples,attribute)
            max_attribute = attribute
    return max_attribute

def plurality_value(data):
    max = -999999
    for each in set(data[10]):
        if max<data[10].count(each):
            max = data[10].count(each)
            value = each 
    return value

def has_same_classification(examples):
    if len(set(examples[10])) == 1:
        return True

def learn_decision_tree(examples, attributes, parent_examples):
    if len(examples) == 0:
        return plurality_value(parent_examples)
    
    if has_same_classification(examples):
        return examples[10][0]
    
    if len(attributes) == 0:
        return plurality_value(examples)

    A = imp_attribute(examples, attributes)
    tree = Node(A)
    attributes.remove(A)
    for each in set(examples[A]):
        indexes = [i for i in range(len(examples[A])) if examples[A][i] == each]
        exs = {}
        for j in examples:
            exs[j] = [examples[j][i] for i in range(len(examples[j])) if i in indexes]
        subtree = learn_decision_tree(exs, attributes, examples)
        # add a branch to tree with label (A = v) and subtree "subtree"
        tree.branch[each] = subtree
    return tree

def display(t, attr_names, indent = 0):
    print('-'*5*(indent),"|",attr_names[t.test],"|")
    for each in t.branch:
        if t.branch[each]== 'Yes' or t.branch[each]== 'No':
            print('-'*4*(indent+1),each,'=>', t.branch[each])
        else:
            print('-'*4*(indent+1),each,)
            display(t.branch[each], attr_names, indent+1)

import pandas as pd
from math import log2
df = pd.read_csv('https://raw.githubusercontent.com/aimacode/aima-data/master/restaurant.csv', header = None)
examples = {}
attributes = [i for i in range(0,10)]
for attribute in attributes:
    examples[attribute] = df[attribute].apply(lambda e: e.strip()).to_list()
examples[10] = df[10].apply(lambda e: e.strip()).to_list()
attr_names = {0:'Alternate',  1:'Bar', 2:'Fri/Sat', 3:'Hungry', 4:'Patrons', 5:'Price', 6:'Raining', 7:'Reservation', 8:'Type', 9:'WaitEstimate', 10:'Wait'}

t = learn_decision_tree( examples, attributes, parent_examples= [])
display(t, attr_names)