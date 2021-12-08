# Algorithm 1: Efficient Privacy Preserving Algorithm
# Input: Original input data set D, quasi-identifier attributes QI (QI1, QI2, ..., QIq), and sensitive attribute SA 
# Output: Privacy preserved data set Dp 
# Initial assignments: c = 0, lambda_value = 3.99, iteration = 400


import math
from collections import Counter


########## SETUP CODE VARS ############

c = 0
lambda_value = 3.99
# iteration = 400
iteration = 10

d = [['Sherry', 'Li', 1, .8], ['Zoe', 'Li', 2, 0.8], ['Hello', 'Li', 3, 7.2], ['Hell', 'Son', 4, 6.8]] # TODO: load here the original input data set
q = ['firstname', 'lastname', 'id', 'status'] # TODO: load here the "quasi-identifier attributes QI (QI1, QI2, ..., QIq)" and "sensitive attribute SA". must be same length as d

d_col = [[] for i in d] # will contain columns of d as rows (aka. transposed)
rr = [None for i in range(len(q))] # will contain 
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

record_place = [[[None for r in range(len(d))] for c in range(nu[i])] for i in range(len(q))] # record_place_i = null_set (the size d * nu[i] for each q[i])
print("record_place", record_place)

# print("len(record_place)", len(record_place))
# print("len(record_place[0])", len(record_place[0]))
# print("len(record_place[0][0])", len(record_place[0][0]))

for i in range (len(q)):
    for j in range(nu[i]):
        for k in range (len(d)):
            print("i", i, "j", j, "k", k)
            print("d[i][k]", d[i][k], " == uv[i][j]", uv[i][j][0])
            print()

            if d[i][k] == uv[i][j][0]: # if k-th record value in q[i] == j-th value in sorted_u[i][j]:
                c += 1

                # print("i", i, "c", c, "j", j)
                # print("record_place[i]", record_place[i])
                # print("record_place[i][c]", record_place[i][c])
                # print("record_place[i][c][j]", record_place[i][c][j])
                record_place[i][c][j] = j # something about a set
            else:
                continue
        c = 0

print("record_place", record_place)
print()


########## ANONYMIZE using x ??? ############


print("len(rr)", len(rr))
for i in range(len(q)):
    rr[i] = round(math.log(nu[i], 2))
print("rr", rr)

x = [[0.1] for i in range(len(q))]
print("x", x)

for i in range(len(q)):
    for j in range(iteration-1): # TODO: figure out if -1 here good or not
        # print("i", i, "j", j)
        x[i].append(lambda_value * x[i][j] * (1 - x[i][j]))

x_rounded = [[round(x[i][j], 3) for j in range(len(x[0]))] for i in range(len(x))]
print("x_rounded")
for xrr in x_rounded:
    print("\t", xrr)

print("d", d)


# r[i]
# uv[i][j]
# x[i][j]

# Determine the new attribute values for the first r[i] value in sorted unique values u[i][j] based on the record places x[i][j] for qi in q[i]

# Replace the chosen record values in d with the determined new values

# Return Dp