
def build_matrix(input):
    with open(input) as f:
        matrix=[]
        n,m = f.readline().split()
        # myDict = [ {int(line.split()[0]):list(map(int,line.split()))[1:] } for line in f]
        # myLict = [ dict  ]
        myList =  [ list(map(int,line.split()))[1:] for line in f ]
        for i in range(int(n)):
            matrix.append([1 if j + 1 in myList[i] else 0 for j in range(int(m))])
    return int(n),int(m),matrix

