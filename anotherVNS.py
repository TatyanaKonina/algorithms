from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import scipy.cluster.hierarchy as spc
import numpy as np
from scipy.cluster.vq import whiten
import copy

class generalVNS:
    def __init__(self,matrix,n,m):
        self.matrix = np.array(matrix)
        self.n = n
        self.m = m
        self.ge = -1
        self.clusters = None
        self.cellBorders = None

    def similarityParts(self,flag):
        if flag:
            A = copy.deepcopy(self.matrix.transpose())
        else:
            A = copy.deepcopy(self.matrix)
        A_sparse = sparse.csr_matrix(A)
        similarities = cosine_similarity(A_sparse)
        return similarities
    
    def defineCluster(self,flag,startNumClusters):
        simMat = self.similarityParts(flag)
        distance_matrix = spc.linkage(simMat, method = 'ward', metric = 'euclidean')
        cell_clusters = spc.fcluster(distance_matrix, startNumClusters, 'maxclust')
        if(not flag):
            cell_clusters = cell_clusters[]
        idx_sort = np.argsort(cell_clusters)
        sorted_cell_clusters = cell_clusters[idx_sort]
        return sorted_cell_clusters,idx_sort

    def SolutionForParts(self,startNumClusters):
        # simMat = self.similarityParts(1)
        # distance_matrix = spc.linkage(simMat, method = 'ward', metric = 'euclidean')
        # cell_clusters = spc.fcluster(distance_matrix, startNumClusters, 'maxclust')

        # idx_sort = np.argsort(cell_clusters)
        # sorted_cell_clusters = cell_clusters[idx_sort]
        sorted_cell_clusters,idx_sort = self.defineCluster(1,startNumClusters)
        
        _, cell_borders = np.unique(sorted_cell_clusters, return_index=True)
        self.matrix = self.matrix[..., idx_sort]
        # simMat = self.similarityParts(0)

        # distance_matrix2 = spc.linkage(simMat, method = 'ward', metric = 'euclidean')
        # cell_clusters2 = spc.fcluster(distance_matrix2, startNumClusters, 'maxclust')

        # idx_sort2 = np.argsort(cell_clusters2)
        # sorted_cell_clusters2 = cell_clusters2[idx_sort2]
        sorted_cell_clusters,idx_sort2 = self.defineCluster(0,startNumClusters)
        # sorted_cell_clusters = sorted_cell_clusters[::-1]
        _, cell_borders_machines = np.unique(sorted_cell_clusters, return_index=True)
        while cell_borders_machines.shape != cell_borders.shape:
            cell_borders_machines = np.append(cell_borders_machines, self.matrix.shape[0])
        
        self.matrix = self.matrix[idx_sort2,...]

        self.cellBorders = np.column_stack(( cell_borders,cell_borders_machines))

    
    def initialSol(self,startNumClusters):
        # simMat = self.similarityParts()
        cellBorders = self.SolutionForParts(startNumClusters)


    def __call__(self, startNumClusters):
        bestBorders,bestMatrix = self.initialSol(startNumClusters)