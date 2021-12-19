"""
1. Make sure you have cleveland_clean.txt
2. Follow instructions in cleveland_mysql.txt in MySQL, replacing the path to 
cleveland_clean.txt with your own in the final command 
3. Then, run this script; if k-anonymized already exists, use the function 
drop_anonymized() followed by create_anonymized at the beginning of the main 
function
"""

import pymysql

# Create a connection object
dbServerName = "127.0.0.1"
dbUser = "user" # replace with your MySQL username
dbPassword = "pass" # replace with your MySQL password
dbName = "cleveland"
charSet = "utf8mb4"
cursorType = pymysql.cursors.DictCursor

connectionObject = pymysql.connect(
    host=dbServerName, 
    user=dbUser, 
    password=dbPassword, 
    db=dbName, 
    charset=charSet, 
    cursorclass=cursorType, 
    local_infile=True)
cursorObject = connectionObject.cursor()

def execute(query):
    cursorObject.execute(query)
    output = cursorObject.fetchall()
    return output

def drop_anonymized():
    cursorObject.execute("DROP TABLE `k-anonymized`;")

def create_anonymized():
    cursorObject.execute("CREATE TABLE `k-anonymized` AS SELECT * FROM original;")

def find_k(qi):
    # TODO: find current k value
    print("hi")

def anonymize(qi, target):
    for item in qi:
        if item[0] == 'generalize':
            # TODO: maybe use sklearn's hierarchical clustering? or Lilo's code
            find_min = "SELECT MIN({}) FROM {}".format(item[1], "`k-anonymized`")
            find_max = "SELECT MAX({}) FROM {}".format(item[1], "`k-anonymized`")
            column_min = execute(find_min)
            column_max = execute(find_max)
            column_inc = item[2]
            change_datatype = "ALTER TABLE `k-anonymized` MODIFY COLUMN {} VARCHAR(20);".format(item[1])
            cursorObject.execute(change_datatype)
            # TODO: replace each value in column with age cluster
            k_current = find_k(qi)
            print("Generalize {}; k = {}".format(item[1], k_current))

        else:
            # replace all values in column with -9
            suppress = "UPDATE `k-anonymized` SET {} = -9".format(item[1])
            cursorObject.execute(suppress)
            k_current = find_k(qi)
            print("Suppress {}; k = {}".format(item[1], k_current))

        k_current = find_k(qi)
        if k_current >= target:
            print("k = {}".format(k_current))
            return k_current

    # if k is never greater than or equal to k_target, return k
    k_current = find_k(qi)
    return k_current

if __name__ == "__main__":
    # format: ('type', 'field')
    k_target = 3
    QI = [
        ('generalize', 'age', 10), # age
        ('suppress', 'sex'), # sex
        ('suppress', 'smoke'), # smoker status
        ('suppress', 'dm') # diabetes history
    ]
    result = anonymize(QI, k_target)

    if result < k_target:
        print("Failed to anonymize to k = {}; k = {}".format(k_target, result))
    else:
        print("Success; k = {}".format(result))
