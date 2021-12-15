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
import numpy as np

class Anonymizer():
    def __init__(self, data, k=3):
        # load in the data (d) and attribute / column names (q)
        # q contains the "quasi-identifier attributes QI (QI1, QI2, ..., QIq)" and "sensitive attribute SA"
        # d contains the actual dataset, with rows as each patient record. columns should correspond to q identifiers.
        (self.q, self.d) = format_data(data)
        # print(self.d[0:10])

        self.qs = [2,3,12]

        print("Columns that are quasi-identifiers: ", [self.q[i] for i in self.qs])
        print("Shape of original data (d):", len(self.d), len(self.d[0]))
        print()

        self.k = k

    def anonymize(self):
        """
        Takes in a dataset, computes the number of crucial unique values, designates 
        new attribute values for them, and replaces them in the records / data.
        """
        self.calculate_k()
        self.bucket_ages(col_number=2)
        self.calculate_k()

        # self.count_values()
        # self.create_recordplace()
        # self.calculate_new_values()
        # self.assign_new_values()

    def calculate_k(self):
        """
        Calculates the minimum number of occurences of the tuples of quasi-identifiers (k-value).
        """
        ts = dict()
        for i in range(len(self.d)):
            t = tuple([self.d[i][j] for j in self.qs])
            if ts.get(t) == None:
                ts[t] = 1
            else:
                ts[t] = ts[t] + 1
        # print("Unique tuples found:", ts)

        self.tss = dict(sorted(ts.items(), key=lambda item: item[1]))
        print("Unique tuples found, sorted:", self.tss)
        print()

        keys = list(self.tss.keys())
        values = list(self.tss.values())
        print("k =", values[0])
        print()


    def bucket_ages(self, col_number, bucket_size=10):
        """
        Buckets age values by given bucket size, starting at the minimum age found in the 
        data at the age column `col_number`.
        """
        b = int(min(np.array(self.d)[:,col_number]))
        for i in range(len(self.d)):
            lower_bound = int((self.d[i][col_number] - b) / bucket_size) * bucket_size + b
            self.d[i][col_number] = lower_bound
        # print("Show first column of data after age-bucketing:", self.d[0])
        # print()

        print("Age buckets: ", end="")
        for i in range(7):
            print(bucket_size*(i-1)+b, "to", bucket_size*i+b, end=", ")
        print(bucket_size*(6)+b, "to", bucket_size*7+b)
        print()

    def count_values(self):
        """
        Counts unique tuples of QIs specified by q.
            d_col is the colunmwise array of data (the transpose)
            nu is the number of unique values for each attribute / column
            uv is an array of tuples of (number of unique values, 
                number of records containing that value) for each attribute / column
        """
        self.d_col = [[] for i in self.d] # will contain columns of d as rows (aka. transposed)
        self.nu = [0 for i in range(len(self.q))] # empty array to be filled with number of unique values for each column / q[i]
        self.uv = [[] for i in range(len(self.q))] # empty array to be filled with the unique values and number of records containing them for each column / q[i] 
        
        for i in range(len(self.q)):
            self.d_col = [row[i] for row in self.d]
            counter = Counter(self.d_col)
            print("counter.items()", counter.items())
            print()

            self.nu[i] = len(counter.items())
            for c in counter.items():
                self.uv[i].append(c)

            # sorts the unique values in terms of number of uses
            self.uv[i].sort(key=lambda x:x[1])

        print("number of unique values for each attribute (nu):", self.nu)
        print("tuple of (number of unique values, number of records containing that value) for each attribute (uv):")
        for k in self.uv:
            print("\t", k)
        print()


    def create_recordplace(self):
        """
        Creates recordplaces, which keeps track of the places in the records / data 
            where each unique values from each column / attribute is found.
        """
        self.record_place = [[[None for k in range(len(self.d))] for j in range(self.nu[i])] for i in range(len(self.q))] # record_place_i = null_set (the size d * nu[i] for each q[i])
        
        for i in range (len(self.q)):
            for j in range(self.nu[i]):
                for k in range (len(self.d)):
                    # print("d[k][i]", self.d[k][i], " == uv[i][j]", self.uv[i][j][0])
                    if self.d[k][i] == self.uv[i][j][0]: # if k-th record value in q[i] == j-th value in sorted_u[i][j]:
                        self.record_place[i][j][k] = j
                    else:
                        continue

        print("record_place")
        for i in range(len(self.record_place)):
            print("\t", self.record_place[i])
        print()


    def calculate_new_values(self):
        """
        This is where the new attribute values are calculated for the parts of 
        the data that need to be replaced. Still in progress. 
        TODO: finish calculate_new_values()

        Theoretically computes the number of crucial unique values and designates 
        new attribute values for them.
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
        print()

        x_rounded_modified = [[round(5*x_rounded[i][j]) for j in range(len(x_rounded[i]))] for i in range(len(x_rounded))]
        print("x_rounded_modified")
        for xr in x_rounded_modified:
            print("\t", xr)
        print()

    def assign_new_values(self):
        """
        This is where the actual changes to anonymize the dataset should happen.
        Still in progress. TODO: finish assign_new_values()

        Theoretically replaces records containing the crucial unique values with 
        new attribute values designated by calculate_new_values().
        """

        for i in range(len(self.q)):
            for j in range(self.r[i]):
                # print(i, j)
                for k in range(len(self.d)):
                    print("self.d[k][i], self.uv[j][0]", self.d[k][i], self.uv[i][j][0])
                    if self.d[k][i] == self.uv[i][j][0]:
                        print("HERE")
                        # what to replace it with?
                        # self.d[k][i] = self.x[]
        
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

anonymizer = Anonymizer(data, k=3)
anonymizer.anonymize()