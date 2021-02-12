from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import scipy.cluster.hierarchy as spc
import numpy as np
from scipy.cluster.vq import whiten
import copy
from random import randint

class generalVNS:
    def __init__(self,matrix,n,m):
        self.matrix = np.array(matrix)
        self.n = n
        self.m = m
        self.ge = -1
        self.clusters = None
        self.cellBorders = None

    
    def randomParts(self,startNumClusters,part):
        cell_clusters = []
        _,check = np.unique(cell_clusters, return_index=True)
        while(len(check) <= 1):
            cell_clusters =np.array( [ randint(1,startNumClusters) for x in range(self.m) ])
            _,check = np.unique(cell_clusters, return_index=True)
        idx_sort = np.argsort(cell_clusters)
        sorted_cell_clusters = cell_clusters[idx_sort]
        _, cell_borders = np.unique(sorted_cell_clusters, return_index=True)
        self.matrix = self.matrix[..., idx_sort]
        return cell_borders
     
    def randomMachine(self,startNumClusters,cell_borders):
        cell_clusters = []
        _,check = np.unique(cell_clusters, return_index=True)
        while(len(check)<=1):
            cell_clusters =np.array( [ randint(1,startNumClusters) for x in range(self.n) ])
            _,check = np.unique(cell_clusters, return_index=True)
        idx_sort = np.argsort(cell_clusters)
        sorted_cell_clusters = cell_clusters[idx_sort]
        _, cell_borders_machines = np.unique(sorted_cell_clusters, return_index=True)
        self.matrix = self.matrix[idx_sort, ...]
        self.cellBorders = np.column_stack((cell_borders_machines, cell_borders))

    def groupingEfficacy(self,matrix = None,cellBorders=None):
        if matrix == None:
            matrix = self.matrix
        if cellBorders == None:
            cellBorders = self.cellBorders
        allOnes = np.count_nonzero(matrix)
        oneIn = 0
        zeroIn = 0
        for j in range(len(cellBorders)):
            if j == len(cellBorders) - 1:
                lowBorder = cellBorders[j]
                highBorder = [None, None]
            else:
                lowBorder = cellBorders[j]
                highBorder = cellBorders[j + 1]
            cell = matrix[lowBorder[0]:highBorder[0], lowBorder[1]:highBorder[1]]
            for i in range(len(cell)):
                oneIn += sum(cell[i])
                zeroIn += len(cell[i]) - sum(cell[i])
        # oneOut = allOnes - oneIn
        return (oneIn )/(allOnes - zeroIn)



    def SolutionForParts(self,startNumClusters):
        cell_borders = self.randomParts(startNumClusters,1)
        self.randomMachine(startNumClusters,cell_borders)
        self.ge = self.groupingEfficacy()
        

    def initialSol(self,startNumClusters):
        cellBorders = self.SolutionForParts(startNumClusters)


    def __call__(self, startNumClusters):
        bestBorders,bestMatrix = self.initialSol(startNumClusters)