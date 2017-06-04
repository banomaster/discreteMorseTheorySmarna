import numpy as np
from scipy.spatial import Delaunay
import operator
import sys
import copy 

sys.path.insert(0, '../cancellingalgorithm')
from fibrewiseDMTnoplot import cancel, euler

f = open("smarna.txt")
pointValue = dict()
indPoint = dict()
indHight = dict()

ind = 0
for l in f:

    l=l[:-1]
    l = str.split(l,"  ")
    l=[float(e) for e in l]

    if abs(l[0] % 1 - 0.17) < 0.00001  or abs(l[1] % 1 - 0.15) < 0.00001:
        continue

    
    p = (l[0], l[1])


    pointValue[p]=l[2]
    indPoint[ind]=p
    indHight[ind]=l[2]
    ind+=1
f.close()



V = pointValue.keys()
#TUKAJ SI NASTAVIS MANJ TOCK ZA TESTIRANJE
V = list(V)#[:10]
#V= [(0, 0), (3, 9), (5, -1), (9, 4), (7, -5)]
#print (V)
print("START Delauney")
T = Delaunay(V)
T = T.simplices

print("END Delauney")



print("START write T")
Eind = set()
vertexEdge = dict()
edgeTriangle = dict()
triangleEdges = dict()
f1 = open("smarna_tri.txt","w")
cofaces = {}
for t in T:
    t.sort()
    #print(t)
    t=tuple(t)
    f1.write(str(t)+"\n")

    e0=(t[0], t[1])
    e1=(t[0], t[2])
    e2=(t[1], t[2])
    vertexEdge[t[0]] = (vertexEdge.get(t[0], set())).union(set([e0,e1]))
    vertexEdge[t[1]] = (vertexEdge.get(t[1], set())).union(set([e0,e2]))
    vertexEdge[t[2]] = (vertexEdge.get(t[2], set())).union(set([e1,e2]))
    edgeTriangle[e0] = (edgeTriangle.get(e0, set())).union(set([t]))
    edgeTriangle[e1] = (edgeTriangle.get(e1, set())).union(set([t]))
    edgeTriangle[e2] = (edgeTriangle.get(e2, set())).union(set([t]))

    triangleEdges[t] = [e0, e1, e2]

    Eind.add(e0)
    Eind.add(e1)
    Eind.add(e2)

    cofaces[e0] = cofaces[e0] + [t] if e0 in cofaces else [t]
    cofaces[e1] = cofaces[e1] + [t] if e1 in cofaces else [t]
    cofaces[e2] = cofaces[e2] + [t] if e2 in cofaces else [t]

    cofaces[t] = []

    cofaces[(t[0],)] = cofaces[t[0]] + [e0, e1] if t[0] in cofaces else [e0, e1]
    cofaces[(t[1],)] = cofaces[t[1]] + [e0, e2] if t[1] in cofaces else [e0, e2]
    cofaces[(t[2],)] = cofaces[t[2]] + [e1, e2] if t[2] in cofaces else [e1, e2]



#print(vertexEdge)
f1.close()
print("END write T")
print("START write E, V < E, E < T")

f1 = open("smarna_edg.txt","w")
for e in Eind:
    f1.write(str(e) + "\n")
f1.close()


f1 = open("smarna_ver_edg.txt","w")
for v in vertexEdge:
    f1.write(str(v) + " : " + str(vertexEdge[v])+"\n")
f1.close()

f1 = open("smarna_edg_tri.txt","w")
for e in edgeTriangle:
    f1.write(str(e) + " : " + str(edgeTriangle[e])+"\n")
f1.close()

print("END write E, V < E, E < T")
print("START gradient")

#GRADIENT E -> T
TriFromEdg = dict()
EdgToTri = dict()
VerUsed = set()
EdgUsed = set()
f1 = open("smarna_edg_arrows.txt","w")
for e in edgeTriangle:
    triangles=list(edgeTriangle[e])
    min=indHight[e[0]] if indHight[e[0]] < indHight[e[1]] else indHight[e[1]]
    minT = None
    eS=set(e)
    for t in triangles:
        if TriFromEdg.get(t,None) == None:
            p=set(t).difference(eS).pop()
            if indHight[p] < min:
                min = indHight[p]
                minT = t
    pair={e:minT}
    if minT != None:
        TriFromEdg[minT]=e
        EdgUsed.add(e)
    EdgToTri[e] = minT
    f1.write(str(pair) + "\n")
f1.close()
#GRADIENT E -> T

# with open("smarna_edg_arrows.txt") as f:
#     for line in f:
        

#GRADIEN V -> E
EdgFromVer = dict()
vertexToEdgeDict = dict()
f1 = open("smarna_ver_arrows.txt","w")
vLen=len(vertexEdge.keys())
for v in vertexEdge:
    edges=list(vertexEdge[v])
    min=indHight[v]
    minE = None
    for e in edges:
        if not e not in EdgUsed:
            if e[0] != v and indHight[e[0]] < min:
                min = indHight[e[0]]
                minE = e
            if e[1] != v and indHight[e[1]] < min:
                min = indHight[e[1]]
                minE = e
    pair={v : minE}
    if minE != None:
        EdgFromVer[minE] = v
        EdgUsed.add(minE)
        VerUsed.add(v)
    
    vertexToEdgeDict[v] = minE
    f1.write(str(pair)+"\n")
f1.close()



#GRADIENT V -> E
print("END gradient")

print "START vector field + paths"

VF = []

index = 0
for e in TriFromEdg:
    t = TriFromEdg[e]
    if t != None:
        VF.append((e, t))

for v in EdgFromVer:
    e = EdgFromVer[v]
    if e !=  None:
        VF.append((v, e))

Paths = []
pathsFromEdge = {}
toVisit = {}

def computePathsFromTriangle((e, t)):
    paths = []
    possibleNewEdges = copy.copy(triangleEdges[t])
    possibleNewEdges.remove(e)

    for possibleEdge in possibleNewEdges:
        if possibleEdge not in toVisit:
            # smo ze vidili
            if possibleEdge in pathsFromEdge:
                # obstajajo poti iz tega edge - izbrisi jih in jih prikljuci trenutni poti
                paths += pathsFromEdge[possibleEdge]
                del pathsFromEdge[possibleEdge]
            continue
        
        del toVisit[possibleEdge]
        if EdgToTri[possibleEdge] == None:
            continue
        
        newPaths = computePathsFromTriangle((possibleEdge, EdgToTri[possibleEdge]))
        paths += newPaths
    
    if len(paths) == 0:
        # zacni novo pot
        return [[(e, t)]]
    else:
        # dodaj vektor na vse najdene poti
        for path in paths:
            path.insert(0,(e, t))

        return paths
    

def computeMaxPathsEdgeTriangle():
    n = len(EdgToTri)
    toVisit = copy.copy(EdgToTri)

    while len(toVisit) != 0:

        startEdge, triangle = toVisit.popitem()
        
        if triangle == None:
            continue
    
        pathsFromEdge[startEdge] = computePathsFromTriangle((startEdge, triangle))
    
    paths = []
    for edge in pathsFromEdge:
        paths += pathsFromEdge[edge]

    return paths

def vertexToEdgePaths(vertexToEdgeArrows):
    verticesToCheck = set(vertexToEdgeArrows.keys())
    pathStartFromVertex = dict()
    currentPath = []
    startVertex = None
    vertex = None

    while len(verticesToCheck) > 0:

        if vertex == None:
            vertex = verticesToCheck.pop()

        if vertex in pathStartFromVertex:
            concatPath = pathStartFromVertex[vertex]
            if concatPath != None:
                pathStartFromVertex[vertex] = None
                pathStartFromVertex[startVertex] = currentPath + concatPath
                startVertex = None
                edge = None
                currentPath = []
                vertex = None
                continue

        edge = vertexToEdgeArrows[vertex]

        if len(currentPath) == 0:
            startVertex = vertex

        if edge != None:
            currentPath.append((vertex, edge))
            (v1,v2) = edge
            vertex = v2 if vertex == v1 else v1
            if vertex in verticesToCheck:
                verticesToCheck.remove(vertex)

        else:  
            if startVertex != None and len(currentPath) > 0:
                pathStartFromVertex[startVertex] = currentPath
            startVertex = None
            edge = None
            currentPath = []
            vertex = None


    paths = []
    for vertex in pathStartFromVertex:
        path = pathStartFromVertex[vertex]
        if path != None:
            paths.append(path)
    return paths

def vertexToEdgePaths(vertexToEdgeArrows):
    verticesToCheck = set(vertexToEdgeArrows.keys())
    pathStartFromVertex = dict()
    currentPath = []
    startVertex = None
    vertex = None

    while len(verticesToCheck) > 0:

        if vertex == None:
            vertex = verticesToCheck.pop()

        if vertex in pathStartFromVertex:
            concatPath = pathStartFromVertex[vertex]
            if concatPath != None:
                pathStartFromVertex[vertex] = None
                pathStartFromVertex[startVertex] = currentPath + concatPath
                startVertex = None
                edge = None
                currentPath = []
                vertex = None
                continue

        edge = vertexToEdgeArrows[vertex]

        if len(currentPath) == 0:
            startVertex = vertex

        if edge != None:
            currentPath.append(((vertex,), edge))
            (v1,v2) = edge
            vertex = v2 if vertex == v1 else v1
            if vertex in verticesToCheck:
                verticesToCheck.remove(vertex)

        else:  
            if startVertex != None and len(currentPath) > 0:
                pathStartFromVertex[startVertex] = currentPath
            startVertex = None
            edge = None
            currentPath = []
            vertex = None


    paths = []
    for vertex in pathStartFromVertex:
        path = pathStartFromVertex[vertex]
        if path != None:
            paths.append(path)
    return paths

paths = computeMaxPathsEdgeTriangle()
paths += vertexToEdgePaths(vertexToEdgeDict)


print "END vector field + paths"


print("START critical")
VerCri = set(vertexEdge.keys()).difference(VerUsed)
VerCriTuple = []
f1 = open("smarna_ver_critical.txt","w")
for v in VerCri:
    VerCriTuple.append((v,))
    f1.write(str(v)+"\n")
f1.close()

EdgCri=set(edgeTriangle.keys()).difference(EdgUsed)
EdgCriTuple = []
f1 = open("smarna_edg_critical.txt","w")
for e in EdgCri:
    eS = set(e)
    if not len(VerCri.intersection(eS)):
        EdgCriTuple.append(tuple(e))
        f1.write(str(e)+"\n")
f1.close()


maxHeight = 0
maxIndex = 0
#Vsi trikotniki, od katerih odstranimo tiste na katere kaze kak edge
TriCri=set([tuple(t) for t in T]).difference(TriFromEdg.keys())
f1 = open("smarna_tri_critical.txt","w")
for t in TriCri:
    for v in t:
        if indHight[v] > maxHeight:
            maxHeight = indHight[v]
            maxIndex = v 

    f1.write(str(t)+"\n")
f1.close()


print("END critical")
#IZRIS 2D
# import matplotlib.pyplot as plt
# V=np.array([list(v) for v in V])
# plt.triplot(V[:,0], V[:,1], T.copy())
# plt.plot(V[:,0], V[:,1], '.')
# plt.savefig("smarna_tri")

Crit = VerCriTuple + EdgCriTuple + list(TriCri)
X = [tuple(t) for t in T]
s = (3, 4)


Crit, V, Paths = cancel(X, s, Crit, VF, Paths, "aloha", cofaces)

euler(Crit)

f1 = open("after_smarna_critical.txt","w")
for c in Crit:
    f1.write(str(c)+"\n")
f1.close()


print "Done."
