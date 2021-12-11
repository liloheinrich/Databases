""" 
Based on https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7512893/?fbclid=IwAR1IshjcFfvWX-oRNi3RcC8eKz3N6e9gxl5pPJe2oX6gYWAeVsrb8sfqHGw
Algorithm 1: Efficient Privacy Preserving Algorithm
Input: Original input data set D, quasi-identifier attributes QI (QI1, QI2, ..., QIq), and sensitive attribute SA 
Output: Privacy preserved data set Dp 
Initial assignments: c = 0, lambda_value = 3.99, iteration = 400
"""

import math
from collections import Counter
from preprocessing import format_data
import pandas as pd

class Anonymizer():
    def __init__(self, data, lambda_value, iterations):
        self.lambda_value = lambda_value
        self.iterations = iterations

        # load in the data (d) and attribute / column names (q)
        # q contains the "quasi-identifier attributes QI (QI1, QI2, ..., QIq)" and "sensitive attribute SA"
        # d contains the actual dataset, with rows as each patient record. columns should correspond to q identifiers.
        (self.q, self.d) = format_data(data)

        # use mini dataset for testing purposes
        self.d = self.d[0:10][0:5]
        self.q = self.q[0:5]

        print("# rows, # cols in original data (d):", len(self.d), len(self.d[0]))
        print("first row of original data (d):", self.d[0])
        print("# rows, names in attribute names (q):", len(self.q), self.q)
        print()

        self.d_col = [[] for i in self.d] # will contain columns of d as rows (aka. transposed)
        self.dp = [[None for j in self.d[0]] for i in self.d] # place to hold modified anonymized dataset, same size as d
        self.r = [None for i in range(len(self.q))] # will contain the number of crucial unique values for each column / q[i] 
        self.nu = [0 for i in range(len(self.q))] # empty array to be filled with number of unique values for each column / q[i]
        self.uv = [[] for i in range(len(self.q))] # empty array to be filled with the unique values and number of records containing them for each column / q[i] 
        self.x = [[0.1] for i in range(len(self.q))] # TODO: describe purpose of x

    def anonymize(self):
        """
        Takes in a dataset, computes the number of crucial unique values, designates 
        new attribute values for them, and replaces them in the records / data.
        """
        self.count_values()
        self.create_recordplace()
        self.assign_new_values()


    def count_values(self):
        """
        Creates d_col, nu, and uv. 
            d_col is the colunmwise array of data (the transpose)
            nu is the number of unique values for each attribute / column
            uv is an array of tuples of (number of unique values, 
                number of records containing that value) for each attribute / column
        """
        for i in range(len(self.q)):
            self.d_col = [row[i] for row in self.d]
            counter = Counter(self.d_col)
            # print("counter.items()", counter.items())
            # print()

            self.nu[i] = len(counter.items())
            for c in counter.items():
                self.uv[i].append(c)

        print("number of unique values for each attribute (nu):", self.nu)
        print("tuple of (number of unique values, number of records containing that value) for each attribute (uv):", self.uv)
        print()
        

    def create_recordplace(self):
        """
        Creates recordplaces, which keeps track of the places in the records / data 
            where each unique values from each column / attribute is found.
        """
        self.record_place = [[[None for k in range(len(self.d))] for j in range(self.nu[i])] for i in range(len(self.q))] # record_place_i = null_set (the size d * nu[i] for each q[i])
        self.record_place2 = [[None for k in range(len(self.d))] for i in range(len(self.q))] # record_place_i = null_set (the size d * nu[i] for each q[i])
        
        for i in range (len(self.q)):
            for j in range(self.nu[i]):
                for k in range (len(self.d)):
                    # print("d[k][i]", self.d[k][i], " == uv[i][j]", self.uv[i][j][0])
                    if self.d[k][i] == self.uv[i][j][0]: # if k-th record value in q[i] == j-th value in sorted_u[i][j]:
                        self.record_place[i][j][k] = j
                        self.record_place2[i][k] = j
                    else:
                        continue

        print("record_place")
        for i in range(len(self.record_place)):
            print("\t", self.record_place[i])
        print()

        print("record_place2")
        for i in range(len(self.record_place2)):
            print("\t", self.record_place2[i])
        print()


    def assign_new_values(self):
        """
        This is where the actual changes to anonymize the dataset should happen.
        Still in progress. TODO: finish assign_new_values()

        Theoretically computes the number of crucial unique values, designates 
        new attribute values for them, and replaces them in the records / data.
        """

        # r is an array that corresponds to the data columns / attributes. it will contain the number 
        # of crucial unique values, computed as round(log2(number of unique values in that column)).
        for i in range(len(self.q)):
            self.r[i] = round(math.log(self.nu[i], 2))
        print("number of crucial values per row (r):", self.r)

        for i in range(len(self.q)):
            for j in range(self.iterations): # TODO: figure out if -1 here good or not
                # print("i", i, "j", j)
                self.x[i].append(lambda_value * self.x[i][j] * (1 - self.x[i][j]))

        x_rounded = [[round(self.x[i][j], 3) for j in range(len(self.x[0]))] for i in range(len(self.x))]
        print("x_rounded")
        for xr in x_rounded:
            print("\t", xr)

        print("original data row 0 (d[0]):", self.d[0])
        print("anonymized data row 0 (dp[0]):", self.dp[0])

        # r[i]
        # uv[i][j]
        # x[i][j]

        # Determine the new attribute values for the first r[i] value in sorted unique values u[i][j] based on the record places x[i][j] for qi in q[i]
        # Replace the chosen record values in d with the determined new values
        # Return Dp


lambda_value = 3.99
# iterations = 400
iterations = 10
data = 'cleveland.csv'

anonymizer = Anonymizer(data, lambda_value, iterations)
anonymizer.anonymize()