

import copy
class generalVNS():
    def __init__(self,matrix,n,m,ge = -1,numberOfClusters = 0,cluster = []):
        self.n = n
        self.m = m
        self.matrix = matrix
        self.ge = ge
        self.numberOfClusters = numberOfClusters
        self.cluster = cluster
        self.GVNS(40,150)
    
    def GVNS(self,kmax,lmax):
        for i in range(1,kmax + 1):
            clusters = self.shaking(i)
            if(clusters):
                bestClusters = self.vnd(clusters,lmax) 
                if(bestClusters == None ):
                    pass
                ge = self.groupingEfficacy(bestClusters)
                if(ge  > self.ge):
                    self.ge = ge
                    self.cluster = bestClusters
                    self.numberOfClusters = i
                    i = 1
                


    def shaking(self,amountOfParts):
        sizeOfRow = self.n
        sizeOfColumn = self.m
        if(amountOfParts <= min(sizeOfRow,sizeOfColumn)):
            clusters = []
            partSize = int(sizeOfRow / (amountOfParts))

            for i in range(amountOfParts):
                start = int(i * partSize + 1)
                if (i != amountOfParts - 1):
                    end = i * partSize + partSize
                    clusters.append(self.getClusterMatrix(start,end,end))
                else:
                    clusters.append(self.getClusterMatrix(start,self.n,self.m))
            return clusters
        return None

    def getClusterMatrix(self,startIndex,endRowIndex,endColumnIndex):
        sequenceNumber = []
        d = {}
        cluster =[]
        for i in range (startIndex,endColumnIndex + 1):
            sequenceNumber.append(i)
        for i in range(startIndex,endRowIndex + 1):
            print(sequenceNumber)
            d[i] = sequenceNumber
        cluster.append(d)

        return cluster


    def vnd(self,clusters,lmax):
        if(clusters != None and len(clusters) <= 1):
            return clusters
        else:
            groupingEfficacy = -1
            bestAddingRowCluster = clusters

            for l in range(lmax):
                iteratedCluster = copy.deepcopy(bestAddingRowCluster)
                rowGe,rowResultCluster = self.getBestRowCluster(iteratedCluster)
                columnGe,columnResultCluster = self.getBestColumnCluster(iteratedCluster)
                maxGe = max(rowGe,columnGe)
                if maxGe > groupingEfficacy:
                    groupingEfficacy = maxGe
                    bestAddingRowCluster = rowResultcluster if maxGe == rowGe else columnResultCluster
                    l = 0
            return bestAddingRowCluster

    def getBestRowCluster(self,iteratedCluster):
        cluster = copy.deepcopy(iteratedCluster)
        rowChangedClusters = []
        for i in range (1,self.n):
            rowChangedClusters,rowGe = self.addRow(iteratedCluster,i)
            if rowGe > self.ge:
                self.ge = rowGe
                self.cluster = rowChangedClusters
        return rowGe,rowChangedClusters

    def getBestColumnCluster(self,iteratedCluster):
        cluster = copy.deepcopy(iteratedCluster)
        clusterGe = self.groupingEfficacy(cluster)
        columnChangedClusters = []
        for i in range (1,self.m):
            columnChangedClusters = self.addColumn(iteratedCluster,i)
            columnGe = groupingEfficacy(rowChangedClusters)
            if columnGe > clusterGe:
                self.ge = columnGe
                self.cluster = columnChangedClusters
        return columnGe,columnChangedClusters

    def addRow(self,clusters,rowIndex):
        ge = self.groupingEfficacy(clusters)
        bestCluster = clusters
        indexOfMatrix = 0
        for i in range(len(clusters)):
                if rowIndex in clusters[i][0]:
                    indexOfMatrix = i
                    break
        
        for i in range(len(clusters)):
            if i != indexOfMatrix:
                copyClusters = copy.deepcopy(clusters)
                del copyClusters[indexOfMatrix][0][rowIndex]
                cluster = copyClusters[i]
                # d = {}
                # d
                # print(list(clusters[i][0].values())[0])
                cluster[0][rowIndex] = list(clusters[i][0].values())[0]
                tempGe = self.groupingEfficacy(copyClusters)
                if(tempGe > ge):
                    ge = tempGe
                    bestCluster = copyClusters
        return bestCluster,ge
    def addColumn(self,clusters,columnIndex):
        ge = self.groupingEfficacy(clusters)
        bestCluster = clusters
        
        indexOfMatrix = []
        
        for i in range(len(clusters)):
            pass
        return bestCluster


    def groupingEfficacy(self,clusters):
        totalNumberOne = 0
        for i in range(self.n):
            totalNumberOne += sum(self.matrix[i])
        numberOneInsideCluster = 0
        numberZeroInsideCluster = 0
        for i in range(len(clusters)):
            print(clusters[i])
            for key in clusters[i][0]:
                for j in clusters[i][0][key]:
                    if(self.matrix[key - 1][j - 1] == 1):
                        numberOneInsideCluster+=1
                    else:
                        numberZeroInsideCluster+=1
        return numberOneInsideCluster / (totalNumberOne + numberZeroInsideCluster)

