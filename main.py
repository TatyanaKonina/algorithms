from read_data import build_matrix
from gnvs import generalVNS



if __name__ == '__main__':
    n,m,matrix = build_matrix("data7.txt")
    generalVNS(matrix,n,m)
    # generalVNS.GVNS(40,150)
1 2 4 5 4 1 1 4 1 5 4 3 5 4 2 5 4 1 5 2 
1 2 2 4 2 1 1 2 1 5 5 3 4 4 4 1 3 4 1 2