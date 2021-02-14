from read_data import build_matrix
from gnvs import generalVNS



if __name__ == '__main__':
    n,m,matrix = build_matrix("data.txt")
    generalVNS(matrix,n,m)
