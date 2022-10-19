

readDir = "./软件著作权0.txt"
writeDir = "./new_file.txt"
outfile = open(writeDir, "w",encoding='utf8')
f = open(readDir, "r",encoding='utf8')

lines_seen = set()  # Build an unordered collection of unique elements.

for line in f:
    line = line.strip('\n')
    if line not in lines_seen:
        outfile.write(line + '\n')
        lines_seen.add(line)