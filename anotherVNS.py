from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import numpy as np

class generalVNS:
    def __init__(self,matrix,n,m):
        self.matrix = matrix
        self.n = n
        self.m = m
        self.ge = -1
        self.clusters = None

    def similarityParts(self):
        A =  np.array(self.matrix)
        A = A.transpose()
        A_sparse = sparse.csr_matrix(A)
        similarities = cosine_similarity(A_sparse)
        return similarities
    
    def SolutionForParts(self,simMat,startNumClusters):
        pass
    
    def initialSol(self,startNumClusters):
        simMat = self.similarityParts()
        cellBorders = self.SolutionForParts(simMat, startNumClusters)


    def __call__(self, startNumClusters):
        bestBorders,bestMatrix = self.initialSol(startNumClusters)