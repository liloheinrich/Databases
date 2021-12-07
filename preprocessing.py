import csv

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

        print(final_list)
        return final_list