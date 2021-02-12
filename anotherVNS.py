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
        while(not len(check)):
            cell_clusters =np.array( [ randint(1,startNumClusters) for x in range(self.m) ])
            _,check = np.unique(cell_clusters, return_index=True)
        # cell_clusters =np.array( [ randint(1,startNumClusters) for x in range(self.m) ])
        
        idx_sort = np.argsort(cell_clusters)
        sorted_cell_clusters = cell_clusters[idx_sort]
        _, cell_borders = np.unique(sorted_cell_clusters, return_index=True)
        self.matrix = self.matrix[..., idx_sort]
        return cell_borders
     
    def randomMachine(self,startNumClusters,cell_borders):
        ell_clusters = []
        _,check = np.unique(cell_clusters, return_index=True)
        while(not len(check)):
            cell_clusters =np.array( [ randint(1,startNumClusters) for x in range(self.m) ])
            _,check = np.unique(cell_clusters, return_index=True)
        idx_sort = np.argsort(cell_clusters)
        sorted_cell_clusters = cell_clusters[idx_sort]
        _, cell_borders_machines = np.unique(sorted_cell_clusters, return_index=True)
        self.matrix = self.matrix[idx_sort, ...]
        self.cell_borders = np.column_stack((cell_borders_machines, cell_borders))

    
    def SolutionForParts(self,startNumClusters):
        cell_borders = self.randomParts(startNumClusters,1)
        self.randomMachine(startNumClusters,cell_borders)
        

    def initialSol(self,startNumClusters):
        cellBorders = self.SolutionForParts(startNumClusters)


    def __call__(self, startNumClusters):
        bestBorders,bestMatrix = self.initialSol(startNumClusters)