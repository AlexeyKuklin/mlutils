def read_dump(file_name):
    return map(str.strip, open(file_name, 'r').readlines())

def parse(file_name):
    dump = read_dump(file_name)
    trees = []
    cur_tree = None
    for line in dump:
       if line[:7] == 'booster': 
           cur_tree = {}
           trees.append(cur_tree)
       else:
           l = line.split(':')
           t = l[1]       
           if t[:4] == 'leaf':
               z = t[5:].split(',')
               z[1] = z[1][6:]
               v = ['leaf', z[0]]
           else:
              t = t.split(' ')
              z = t[1].split(',')
              v = [t[0][1:-1], z[0][4:], z[1][3:], z[2][8:]]
           cur_tree[l[0]] = v

    return trees

def recurse(t, n):
    v = t[n]
    if v[0] == 'leaf':
        print 'return '+v[1]
    else:
        m = ''
        if v[3] == v[1]:
            m = ' or '+ v[0].split('<')[0] + ' is null' 
        print 'case when ' + v[0] +  m + ' then'
        recurse(t, v[1])
        print 'else ' 
        recurse(t, v[2])
        print 'end'

trees = parse('dump.txt')
t = trees[0]
s = []
recurse(t, '0') 
