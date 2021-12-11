# Algorithm 1: Efficient Privacy Preserving Algorithm
# Input: Original input data set D, quasi-identifier attributes QI (QI1, QI2, ..., QIq), and sensitive attribute SA 
# Output: Privacy preserved data set Dp 
# Initial assignments: c = 0, lambda_value = 3.99, iteration = 400


import math
from collections import Counter


########## SETUP CODE VARS ############

lambda_value = 3.99
# iteration = 400
iteration = 10

d = [['Sherry', 'Li', 1, .8, 9], ['Zoe', 'Li', 2, 0.8, 7], ['Hello', 'Li', 3, 7.2, 8], ['Hello', 'World', 4, 6.8, 6]] # TODO: load here the original input data set
q = ['firstname', 'lastname', 'id', 'status', 'something'] # TODO: load here the "quasi-identifier attributes QI (QI1, QI2, ..., QIq)" and "sensitive attribute SA". must be same length as d

d_col = [[] for i in d] # will contain columns of d as rows (aka. transposed)
dp = [[None for j in d[0]] for i in d] # place to hold modified anonymized dataset, same size as d
r = [None for i in range(len(q))] # will contain 
nu = [0 for i in range(len(q))] # empty array to be filled with number of unique values for each q[i]
uv = [[] for i in range(len(q))] # empty array to be filled with the unique values and number of records containing them for each q[i] 


########## CREATE d_col, nu, uv ############

for i in range(len(q)):
    d_col = [row[i] for row in d]
    print("i", i, "d_col", d_col)
    counter = Counter(d_col)
    print(counter.items())
    print()

    nu[i] = len(counter.items())
    for c in counter.items():
        uv[i].append(c)

print("nu", nu)
print("uv", uv)


########## RECORD PLACE ############

record_place = [[[None for k in range(len(d))] for j in range(nu[i])] for i in range(len(q))] # record_place_i = null_set (the size d * nu[i] for each q[i])
record_place2 = [[None for k in range(len(d))] for i in range(len(q))] # record_place_i = null_set (the size d * nu[i] for each q[i])
print("record_place", record_place)

# print("len(record_place)", len(record_place))
# print("len(record_place[0])", len(record_place[0]))
# print("len(record_place[0][0])", len(record_place[0][0]))

print("len(q)", len(q))
print("len(d)", len(d))
print("len(d[0])", len(d[0]))


for i in range (len(q)):
    for j in range(nu[i]):
        for k in range (len(d)):
            # print("i", i, "j", j, "k", k)
            print("d[k][i]", d[k][i], " == uv[i][j]", uv[i][j][0])
            # print()

            if d[k][i] == uv[i][j][0]: # if k-th record value in q[i] == j-th value in sorted_u[i][j]:

                record_place[i][j][k] = j
                record_place2[i][k] = j
                print()
            else:
                continue

print("record_place")
for i in range(len(record_place)):
    print("\t", record_place[i])
print()

print("record_place2")
for i in range(len(record_place2)):
    print("\t", record_place2[i])
print()


########## ANONYMIZE using x ??? ############

print("len(r)", len(r))
for i in range(len(q)):
    r[i] = round(math.log(nu[i], 2))
print("r", r)

x = [[0.1] for i in range(len(q))]
print("x", x)

for i in range(len(q)):
    for j in range(iteration): # TODO: figure out if -1 here good or not
        # print("i", i, "j", j)
        x[i].append(lambda_value * x[i][j] * (1 - x[i][j]))

x_rounded = [[round(x[i][j], 3) for j in range(len(x[0]))] for i in range(len(x))]
print("x_rounded")
for xr in x_rounded:
    print("\t", xr)

print("d", d)
print("dp", dp)

# r[i]
# uv[i][j]
# x[i][j]

# Determine the new attribute values for the first r[i] value in sorted unique values u[i][j] based on the record places x[i][j] for qi in q[i]

# Replace the chosen record values in d with the determined new values



# Return Dp