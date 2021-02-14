

import copy
class generalVNS():
    def __init__(self,matrix,n,m,ge = -1,clustersNum = 0,cluster = []):
        self.n = n
        self.m = m
        self.matrix = matrix
        self.ge = ge
        self.clustersNum = clustersNum
        self.cluster = cluster
        self.vnsIter = 50
        self.changeInClusterIter = 200
        self.GVNS()
    
    def GVNS(self):
        for i in range(1,self.vnsIter + 1):
            if i == 1:
                clusters = self.shaking(partsNum = 2)
            else:
                clusters = self.shaking(i)
            if(clusters):
                groupingEfficacy = -1
                bestClusters = clusters
                for l in range(self.changeInClusterIter):
                    currentCluster = copy.deepcopy(bestClusters)
                    rowGe,rowResultCluster = self.buildRowCluster(currentCluster)
                    columnGe,columnResultCluster = self.buildColumnCluster(currentCluster)
                    maxGe = max(rowGe,columnGe)
                    if maxGe > groupingEfficacy:
                        groupingEfficacy = maxGe
                        if maxGe == rowGe :
                            bestClusters = copy.deepcopy(rowResultCluster)
                        else:
                            bestClusters = copy.deepcopy(columnResultCluster)    
                        l = 0
                ge = self.groupingEfficacy(bestClusters)
                if(ge  > self.ge):
                    self.ge = ge
                    self.cluster = bestClusters
                    self.clustersNum = i
                    self.printRes()
                    i = 1
        print(self.ge,self.cluster,self.clustersNum)

    def printRes(self):
        machines = []
        parts= []
        for i in range(self.n):
            for j in range(len(self.cluster)):
                # print(self.cluster[j][0].keys())
                if i + 1 in self.cluster[j][0].keys():
                    machines.append(j + 1)
            # list(.values())[0]
        for i in range(self.m):
            for j in range(len(self.cluster)):
                if i + 1 in list(self.cluster[j][0].values())[0]:
                    parts.append(j + 1)
        print(' '.join(str(item) for item in machines))
        print(' '.join(str(item) for item in parts))
        print(self.ge)
        # print(machines,parts,self.ge)
            
    def shaking(self,partsNum):
        if(partsNum <= min(self.n,self.m)):
            clusters = []
            partSize = int(self.n / (partsNum))
            for i in range(partsNum):
                start = int(i * partSize + 1)
                if (i != partsNum - 1):
                    rowIndex,columnIndex = i * partSize + partSize,i * partSize + partSize
                else:
                    rowIndex,columnIndex = self.n,self.m
                part,cluster = [],[]
                d = {}
                for j in range (start,columnIndex + 1):
                    part.append(j)
                for j in range(start,rowIndex + 1):
                    d[j] = part
                    cluster.append(d)
                clusters.append(cluster)
            return(clusters)
        return None

    def buildRowCluster(self,currentCluster):
        ge = -1
        cluster = copy.deepcopy(currentCluster)
        rowClusters = []
        for i in range (1,self.n + 1):
            rowClusters,rowGe = self.changeRows(currentCluster,i)
            if rowGe > ge:
                ge = rowGe
                cluster = copy.deepcopy(rowClusters)
        return ge,cluster

    def buildColumnCluster(self,currentCluster):
        ge = -1
        cluster = copy.deepcopy(currentCluster)
        clusterGe = self.groupingEfficacy(cluster)
        columnClusters = []
        for i in range (1,self.m + 1):
            columnClusters,columnGe = self.changeColumns(currentCluster,i)
            if columnGe > ge:
                ge = columnGe
                cluster = copy.deepcopy(columnClusters)
        return ge,cluster

    def changeRows(self,clusters,rowIndex):
        ge = self.groupingEfficacy(clusters)
        bestCluster = clusters
        clusterInd = 0
        for i in range(len(clusters)):
                if rowIndex in clusters[i][0]:
                    clusterInd = i
                    break
        if(len(clusters[clusterInd][0]) > 1):
            for i in range(len(clusters)):
                if i != clusterInd:
                    copyClusters = copy.deepcopy(clusters)
                    del copyClusters[clusterInd][0][rowIndex]
                    cluster = copyClusters[i]
                    cluster[0][rowIndex] = list(clusters[i][0].values())[0]
                    tempGe = self.groupingEfficacy(copyClusters)
                    if(tempGe > ge):
                        ge = tempGe
                        bestCluster = copyClusters
        return bestCluster,ge

    def changeColumns(self,clusters,columnIndex):
        ge = self.groupingEfficacy(clusters)
        bestCluster = clusters
        
        clusterInd = 0
        for i in range(len(clusters)):
            if columnIndex in list(clusters[i][0].values())[0]:
                clusterInd = i
                break
        if(len(list(clusters[clusterInd][0].values())[0]) > 1):
            for i in range(len(clusters)):
                if i != clusterInd:
                    copyClusters = copy.deepcopy(clusters)
                    for j in list(copyClusters[clusterInd][0].keys()):
                        if(columnIndex in copyClusters[clusterInd][0][j]):
                            copyClusters[clusterInd][0][j].remove(columnIndex)
                    for j in list(copyClusters[i][0].keys()):
                        if not columnIndex in copyClusters[i][0][j]:
                            copyClusters[i][0][j].append(columnIndex)
                    tempGe = self.groupingEfficacy(copyClusters)
                    if(tempGe > ge):
                        ge = tempGe
                        bestCluster = copyClusters
        return bestCluster,ge

    def groupingEfficacy(self,clusters):
        totalOne = 0
        for i in range(self.n):
            totalOne += sum(self.matrix[i])
        oneInsideCluster = 0
        zeroInsideCluster = 0
        for i in range(len(clusters)):
            for key in clusters[i][0]:
              
                for j in clusters[i][0][key]:
                    if(self.matrix[key - 1][j - 1] == 1):
                        oneInsideCluster+=1
                    else:
                        zeroInsideCluster+=1
        return oneInsideCluster / (totalOne + zeroInsideCluster)

