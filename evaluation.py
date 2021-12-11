#Metrics to evaluate anonymization based on the metrics from:
#An Efficient Big Data Anonymization Algorithm Based on Chaos and Perturbation Techniques
#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7512893/
#Micah Reid
from sklearn.metrics import accuracy_score, f1_score
import pandas as pd
import numpy as np

def KL_divergence(p, q):
    #Kullback–Leibler divergence (KL divergence) is used to quantify the difference between two distributions
    #In privacy preserving, it is utilized for computing the distance between original and privacy preserved data sets.
    #The two distributions are K and P
    #KL divergence can be calculated as the negative sum of probability of each event in P multiplied
    #by the log of the probability of the event in Q over the probability of the event in P.
    #KL(P || Q) = – sum x in X P(x) * log(Q(x) / P(x))
	return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p))) #Source: https://machinelearningmastery.com/divergence-between-probability-distributions/


def probabalistic_anonymity(original, anonymized):
    #if r is a record in original and r' is a record in anonymized, and QI is quasi-identifier:
    #should take in only QI info
    #the probabalistic anonymity of anonymized dataset is 1/P(r(QI) | r'(QI))
    #where P(r(QI) | r'(QI)) is the probability that r(QI) for all r in original may be inferred given r'(QI)
    #we can take "inferred" to mean they are the same value, at least for now

    margin = .05
    #This will need to be rewritten to match the data we put in
    #maybe put into discrete categories based on margin later if necessary
    original = np.ravel(original)
    anonymized = np.ravel(anonymized)
    intersection = np.intersect1d(original, anonymized)
    inferred = len(intersection) / len(original) #then we can find the proportion that is "inferred"

    return 1/inferred

def classification_accuracy(original, anonymized):
    return accuracy_score(original, anonymized)


def f_measure(original, anonymized):
    return f1_score(original, anonymized)
