# dataset: https://archive.ics.uci.edu/ml/datasets/Heart+Disease

"""
column_headers: list of headers for csv, q in algorithm
format_data: formats cleveland.csv into list of lists each containing row of 
csv (d in algorithm), outputs tuple: (q, d)
"""

import csv

column_headers = [
    'id', 
    'ccf',
    'age',
    'sex',
    'painloc',
    'painexer',
    'relrest',
    'pncaden',
    'cp',
    'trestbps',
    'htn',
    'chol',
    'smoke',
    'cigs',
    'years',
    'fbs',
    'dm',
    'famhist',
    'restecg',
    'ekgmo',
    'ekgday',
    'ekgyr',
    'dig',
    'prop',
    'nitr',
    'pro',
    'diuretic',
    'proto',
    'thaldur',
    'thaltime',
    'met',
    'thalach',
    'thalrest',
    'tpeakbps',
    'tpeakbpd',
    'dummy',
    'trestbpd',
    'exang',
    'xhypo',
    'oldpeak',
    'slope',
    'rldv5',
    'rldv5e',
    'ca',
    'restckm',
    'exerckm',
    'restef',
    'restwm',
    'exeref',
    'exerwm',
    'thal',
    'thalsev',
    'thalpul',
    'earlobe',
    'cmo',
    'cday',
    'cyr',
    'num',
    'lmt',
    'ladprox',
    'laddist',
    'diag',
    'cxmain',
    'ramus',
    'om1',
    'om2',
    'rcaprox',
    'rcadist',
    'lvx1',
    'lvx2',
    'lvx3',
    'lvx4',
    'lvf',
    'cathef',
    'junk',
    'name'
]

def format_data(data):
    """
    Quick and dirty way of properly formatting this specific messy data.
    """
    with open('cleveland.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        l = []
        sl = []
        for row in csvreader:
            if row[-1] != 'name':
                sl.append(row)
            else: 
                sl.append(row)
                l.append(sl)
                sl = []

        new_list = []
        for ls in l:
            flat_list = [item for sublist in ls for item in sublist]
            new_list.append(flat_list)

        final_list = []
        for ls in new_list:
            sublist = []
            for item in ls:
                if item != 'name':
                    sublist.append(int(float(item)))
                else:
                    sublist.append(item)
                    final_list.append(sublist)
                    sublist = []

        # print(final_list)
        return (column_headers, final_list)

if __name__ == "__main__":
    data = format_data("cleveland.csv")