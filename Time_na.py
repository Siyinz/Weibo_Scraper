import csv
def time_na(inputfile,outputfile):

    with open(inputfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lines = list(csv_reader)
        time = []
        line = []
        
        for i, row in enumerate(lines):
            if row[0] != "NA":
                time.append(row[0])
            else:
                row[0]=time[i-1]
                time.append(row[0])
            line.append(row)
        
        writer = csv.writer(open(outputfile, 'w'))
        writer.writerows(line) 

inputfile = '/Users/siyinzheng/Desktop/weibo/黑卫兵/黑卫兵2019-2020.csv'
outputfile = '/Users/siyinzheng/Desktop/weibo/黑卫兵/黑卫兵2019-2020_time.csv'
time_na(inputfile,outputfile)