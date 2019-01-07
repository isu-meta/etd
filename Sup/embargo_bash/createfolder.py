import os
# Run on windows

infile = open('embargolist.txt', 'r')
lines = infile.readlines()
# First pass creates directories
li = []
for line in lines:
    clean_line = line.strip()
    X, Y = clean_line.split('.xml')
    F = X.replace("_DATA-out", "")
    date = str(Y).split('/')
    s = '{}-{}'
    target = s.format(date[2], date[0])
    li.append(target)

files2create = (set(li))
path = os.getcwd()

try:
    [os.mkdir("C:\\Users\\rwolfsla\\Desktop\\ETD_TEST\\embargo_store\\"+x) for x in files2create]
except Exception as e:
    print(e)
