from subprocessing import bash_command
# run on linux (because of subprocess)
infile = open('embargolist.txt', 'r')
lines = infile.readlines()

for line in lines:
    clean_line = line.strip()
    X, Y = clean_line.split('.xml')
    F = X.replace("_DATA-out", "")
    date = str(Y).split('/')
    s = '{}-{}'
    target = s.format(date[2], date[0])
    source = 'mv /mnt/d/Users/rwolfsla/Desktop/process/ETD_TEST/Embargo/*/{}* /mnt/d/Users/rwolfsla/Desktop/process/ETD_TEST/test/{}'.format(F,target)
    bash_command(source)

