"""
1. Make sure you have cleveland_clean.txt
2. Follow instructions in cleveland_mysql.txt in MySQL, replacing the path to 
cleveland_clean.txt with your own in the final command 
3. Then, run this script; if k-anonymized already exists, use the function 
drop_anonymized() followed by create_anonymized at the beginning of the main 
function
"""

import pymysql
import re

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
    """
    Execute query, return output.
    """
    cursorObject.execute(query)
    output = cursorObject.fetchall()
    return output

def drop_anonymized():
    """
    Drop table k-anonymized.
    """
    cursorObject.execute("DROP TABLE `k-anonymized`;")

def create_anonymized():
    """
    Create table k-anonymized from table original, which contains unaltered 
    data.
    """
    cursorObject.execute("CREATE TABLE `k-anonymized` AS SELECT * FROM original;")

def find_k():
    """
    Determine k-anonymity of data. Functionality is limited to data formatted 
    in the same way as the Cleveland dataset.
    """
    query = "SELECT generalized_age, sex, dm, COUNT(*) as count FROM `k-anonymized` GROUP BY generalized_age, sex, dm ORDER BY count ASC;"
    k = execute(query)[0]["count"]
    return k

def anonymize(qi, target):
    """
    Anonymize data through selective suppression and generalization.
    """
    for item in qi:
        field = item[1]

        # detemine if field is to be generalized or suppressed
        if item[0] == 'generalize':
            find_min = "SELECT MIN({}) AS min FROM {}".format(field, "`k-anonymized`")
            find_max = "SELECT MAX({}) AS max FROM {}".format(field, "`k-anonymized`")
            column_min = execute(find_min)[0]["min"]
            column_max = execute(find_max)[0]["max"]
            increment = item[2]

            all_entries = execute("SELECT {} FROM `k-anonymized`;".format(field))
            l = []
            for i in all_entries:
                l.append(i[field])
                
            # determine range of ages in dataset
            ranges = list(bucket(range(column_min-1, column_max+1), increment))
            l_ranges = []
            for i in l:
                for j in ranges:
                    if i in j:
                        l_ranges.append(j)

            # create an empty column for generalized data
            create_generalized = "ALTER TABLE `k-anonymized` ADD COLUMN generalized_age TEXT;"
            cursorObject.execute(create_generalized)

            # ensure consecutive id values
            create_i = "SELECT @i:=0;"
            cursorObject.execute(create_i)
            ensure_consecutive_ids = "UPDATE `k-anonymized` SET id = @i:=@i+1;"
            cursorObject.execute(ensure_consecutive_ids)

            id_counter = 1
            for i in l_ranges:
                # format age range in acceptable manner (janky but foolproof)
                string = str(i)
                ints = re.findall('\d+', string)
                first_int = int(ints[0])
                second_int = int(ints[1])
                generalize = "UPDATE `k-anonymized` SET generalized_age = '{} < {} < {}' WHERE id = {};".format(first_int, field, second_int, id_counter)
                cursorObject.execute(generalize)
                id_counter += 1
            
            # drop the ungeneralized column from table
            drop_ungeneralized = "ALTER TABLE `k-anonymized` DROP COLUMN {};".format(field)
            cursorObject.execute(drop_ungeneralized)

            # update k
            k_current = find_k()
            print("Generalize {}; k = {}".format(field, k_current))

        else:
            # suppress by replacing all values in column with -9
            suppress = "UPDATE `k-anonymized` SET {} = -9".format(field)
            cursorObject.execute(suppress)

            # update k
            k_current = find_k()
            print("Suppress {}; k = {}".format(field, k_current))

        # determine if target k value has been reached
        k_current = find_k()
        if k_current >= target:
            return k_current

def bucket(lst, n):
    """
    Create list of ranges between age minimum and maximum.
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        

if __name__ == "__main__":
    """
    Driver code.
    """
    # ideal k value
    k_target = 3

    # format: ('type', 'field', bucketing increment (if type = generalize))
    QI = [
        ('generalize', 'age', 30), # age
        ('suppress', 'sex'), # sex
        ('suppress', 'dm') # diabetes history
    ]

    # ensure unaltered table
    drop_anonymized()
    create_anonymized()

    # determine if anonymization resulted in target k value
    final = anonymize(QI, k_target)
    if final < k_target:
        print("Failed to anonymize to k = {}; k = {}".format(k_target, final))
    else:
        print("Success; k = {}".format(final))
    