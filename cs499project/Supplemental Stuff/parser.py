import csv
import sys

f = open(sys.argv[1], 'rt') ##this takes the first argument to be the file to parse
##an example call to this would be "python parser.py file.csv"

try:
    reader = csv.reader(f, skipinitialspace=True) ##create a csv reader

    rownum = 0 ##start with row number 0 (first row)
    colnum = 0 ##start with column number 0 (first column)
    
    for row in reader: ##for every row in the file (reader)
        
        for col in row: ##for every column in the row
            
            print col  ##This prints the column
            colnum += 1 ##go to the next column
            
        print "\n" ##after printing an entire column, print a new line to separate them
        rownum += 1 ##go to the next row
        
finally:
    f.close() ##close the file when done
