from read_data import build_matrix
from anotherVNS import generalVNS 
import copy

if __name__ == '__main__':
    n,m,initialMatrix = build_matrix("data.txt")
    matrix = copy.deepcopy(initialMatrix)
    ann_sim_method = generalVNS(matrix,n,m)
    ann_sim_method(2)