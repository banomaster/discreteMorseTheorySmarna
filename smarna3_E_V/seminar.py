import numpy as np
from scipy.spatial import Delaunay
import operator
import sys
import copy 
import random
import itertools
import matplotlib.pyplot as plt
import math

f = open("smarna.txt")
pointValue = dict()
indPoint = []
indHight = []

centralPointParameters = dict()

ind = 0
for l in f:

    l=l[:-1]
    l = str.split(l,"  ")
    l=[float(e) for e in l]

    if abs(l[0] % 1 - 0.17) < 0.00001  or abs(l[1] % 1 - 0.15) < 0.00001:
        continue

    
    p = (l[0] / 10000.0, l[1] / 10000.0)

    pointValue[p]=l[2]
    indPoint.append(p)
    indHight.append(l[2])
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

    cofaces[(t[0],)] = cofaces[(t[0],)] + [e0, e1] if (t[0],) in cofaces else [e0, e1]
    cofaces[(t[1],)] = cofaces[(t[1],)] + [e0, e2] if (t[1],) in cofaces else [e0, e2]
    cofaces[(t[2],)] = cofaces[(t[2],)] + [e1, e2] if (t[2],) in cofaces else [e1, e2]

    def getCentralVertex(simplex):

        avgLat, avgLon, avgHeight = (0,0,0)
        for p in simplex:
            (lat, lon) = indPoint[p]
            height = indHight[p]

            avgLat += lat
            avgLon += lon
            avgHeight += height

        d = len(simplex)
        return avgLat / d, avgLon / d, avgHeight / d


    if (t[0],) not in centralPointParameters:
        centralPointParameters[(t[0],)] = getCentralVertex((t[0],))
    if (t[1],) not in centralPointParameters:
        centralPointParameters[(t[1],)] = getCentralVertex((t[1],))
    if (t[2],) not in centralPointParameters:
        centralPointParameters[(t[2],)] = getCentralVertex((t[2],))
    if e0 not in centralPointParameters:
        centralPointParameters[e0] = getCentralVertex(e0)
    if e1 not in centralPointParameters:
        centralPointParameters[e1] = getCentralVertex(e1)
    if e2 not in centralPointParameters:
        centralPointParameters[e2] = getCentralVertex(e2)
    if t not in centralPointParameters:
        centralPointParameters[t] = getCentralVertex(t)



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
    
    vertexToEdgeDict[(v,)] = minE
    f1.write(str(pair)+"\n")
f1.close()



#GRADIENT V -> E
print("END gradient")

print "START vector field + paths"

VF = []

index = 0
for t in TriFromEdg:
    e = TriFromEdg[t]
    VF.append((e, t))

for e in EdgFromVer:
    v = EdgFromVer[e]
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

    paths = set([tuple(path) for path in paths])
    return paths

def vertexToEdgePaths():
    verticesToCheck = set(vertexToEdgeDict.keys())
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

        edge = vertexToEdgeDict[vertex]

        if len(currentPath) == 0:
            startVertex = vertex

        if edge != None:
            currentPath.append((vertex, edge))
            (v1,v2) = edge
            vertex = (v2,) if vertex == (v1,) else (v1,)
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

    paths = set([tuple(path) for path in paths])
    return paths

def dim(s):
    return len(s) - 1

# from a list of maximal simplices construct a list of all simplices
def allsc(X):
    A = set(X)
    for s in X:
        n = len(s)
        for i in range(1, n):
            for p in itertools.combinations(s, i):
                A.add(p)
    A = list(A)
    A.sort(key=len)
    return A

# get the boundary of s
def boundary(s):

    if len(s) == 1:
        return []
    B = set()
    for b in itertools.combinations(s, len(s) - 1):
        B.add(b)
    return B

# returns an open star of a given simplex s, S can be a list of all simplices
# or a list of maximal simplices
def star(s, S):

    A = allsc(S)
    st = [s]
    for a in A:
        B = boundary(a)
        B = allsc(B)
        if s in B:
            st.append(a)
    return st

# find the Euler characteristic of a simplex using the list of its critical cells
def euler(Crit):

    chi = {}
    for c in Crit:
        dim = len(c) - 1
        if dim in chi:
            chi[dim] += 1
        else:
            chi[dim] = 1

    x = 0
    for c in chi:
        if c % 2 == 0:
            x += chi[c]
        else:
            x -= chi[c]

    return x

def path_flip(alpha, beta, my_path, Crit, V, Paths):

    Q = my_path.keys()
    q = Q[0]
    k = len(q)

    pair = q[0]
    first, second = pair
    if len(first) == 1:
        oldPaths = set()
    elif len(first) == 2:
        oldPaths = computePathsFromTriangle((first,second))
        oldPaths = set([tuple(path) for path in oldPaths])

    # remove old pairs from the arrow dicts
    for pair in q:
        first, second = pair
        if len(first) == 1:
            del vertexToEdgeDict[first]
        elif len(first) == 2:
            del EdgToTri[first]

    # revese the path q
    qbar = [(alpha, q[k - 1][1])]
    for i in range(k - 1, 0, -1):
        qbar.append((q[i][0], q[i - 1][1]))
    qbar.append((q[0][0], beta))

    # add new pairs to the arrow dicts
    for pair in qbar:
        first, second = pair
        if len(first) == 1:
            vertexToEdgeDict[first] = second
        elif len(first) == 2:
            EdgToTri[first] = second

    pair = qbar[0]
    first, second = pair
    if len(first) == 1:
        newPaths = set()
    elif len(first) == 2:
        newPaths = computePathsFromTriangle((first,second))
        newPaths = set([tuple(path) for path in newPaths])

    # remove old paths and add new paths
    for oldPath in oldPaths:
        Paths.remove(oldPath)
    for newPath in newPaths:
        Paths.add(newPath)

    Crit.remove(alpha)
    Crit.remove(beta)

    return Crit, V, Paths

def cancel(X, s, Crit, V, Paths, seed, cofaces = None, centralPointParameters = None):

    # create a graded list (dictionary) of critical simplices

    GradCrit = {}

    for c in Crit:
        d = dim(c)
        if d not in GradCrit:
            GradCrit[d] = [c]
        else:
            GradCrit[d].append(c)

    # for each critical simplex find all faces and cofaces
    S = allsc(X)
    FaceCrit = {}
    CofaceCrit = {}
    if cofaces == None:
        for c in Crit:
            FaceCrit[c] = list(boundary(c))
            CofaceCrit[c] = []
            n = dim(c)

            for sx in S:
                if dim(sx) == n + 1 and c in boundary(sx):
                    CofaceCrit[c].append(sx)
    else:
        for c in Crit:
            FaceCrit[c] = list(boundary(c))
            CofaceCrit[c] = cofaces[c]

    # build a list of pairs of critical simplices
    # with neighbouring dimensions (candidates for cancelling)
    # only consider pairs not contained in the star of s

    dims = GradCrit.keys()
    dims.sort()
    pairs_to_cancel = set()
    St = star(s, X)
    if 0 in GradCrit and len(GradCrit[0]) == 1:
        dims.remove(0)
    for d in dims:
        if d + 1 in dims:
            A = GradCrit[d]
            B = GradCrit[d + 1]

            print "Generating canceling pairs for dim: " + str(d)

            if centralPointParameters != None:
                new_pairs = []
                for a in A:
                    latA, lonA, heightA = centralPointParameters[a]
                    for b in B:

                        latB, lonB, heightB = centralPointParameters[b]

                        distance = (latA - latB)**2 + (lonA - lonB)**2
                        heightDiff = abs(heightA - heightB)
 
                        if distance < 0.0001 and heightDiff < 10 and (a not in boundary(b)):
                            new_pairs.append((a,b))
            else:
                new_pairs = [(a,b) for a in A for b in B if (a not in boundary(b))]

            print("New pairs for canceling: " + str(len(new_pairs)))

            print "Stopped generating canceling pairs"
            for pair in new_pairs:
                pairs_to_cancel.add(pair)

    random.seed(seed)

    # while there are pairs to cancel left, choose one at random

    while len(pairs_to_cancel) != 0:
        if len(pairs_to_cancel) % 10 == 0:
            print "pairs to cancel left: " + str(len(pairs_to_cancel))

        m = len(pairs_to_cancel)
        pair = pairs_to_cancel.pop()

        # dim(alpha) = d, dim(beta) = d+1

        alpha = pair[0]
        beta = pair[1]

        # look at all faces and cofaces

        B = FaceCrit[beta]
        A = CofaceCrit[alpha]

        my_path = {}
        unique = True

        for b in B:
            for a in A:
                for p in Paths:
                    # if there is a path starting at b and ending in a, remember it

                    p0 = [arrow[0] for arrow in p]  # starts of arrows
                    p1 = [arrow[1] for arrow in p]  # ends of arrows
                    if b in p0 and a in p1:
                        print "if b in p0 and a in p1"
                        ib = p0.index(b)
                        ia = p1.index(a)
                        if ib <= ia:
                            print "ib <= ia"
                            q = tuple(p[ib:ia + 1])
                            Q = my_path.keys()
                            if Q != [] and q not in Q:
                                print "unique false 1"
                                unique = False
                            if q in Q:
                                my_path[q].append((p, ib, ia, b, a))
                            elif my_path == {}:
                                my_path[q] = [(p, ib, ia, b, a)]
                            else:
                                print "unique false 2"
                                unique = False

                            # if there is more than one pair, the pair cannot be cancelled, so skip it

                            if not unique:
                                break  # for p in Paths
                if not unique:
                    break  # for a in A
            if not unique:
                break  # for b in B
        if my_path == {}:
            unique = False

        # pairs_to_cancel.remove(pair)

        if unique:
            print("is unique!!!")
            Crit, V, Paths = path_flip(alpha, beta, my_path, Crit, V, Paths)
            toRemove = []
            for p in pairs_to_cancel:
                if p[0] == alpha or p[1] == beta:
                    toRemove.append(p)
            for p in toRemove:
                pairs_to_cancel.remove(p)

    # while ends here

    printout(Crit, V, Paths)

    return Crit, V, Paths

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

Crit = VerCriTuple + EdgCriTuple + list(TriCri)
X = [tuple(t) for t in T]
s = (3, 4)

print "Generate paths"

paths = computeMaxPathsEdgeTriangle()
paths = paths.union(vertexToEdgePaths())

print "Start canceling"

Crit, V, Paths = cancel(X, s, Crit, VF, paths, "aloha", cofaces, centralPointParameters)

euler(Crit)

f1 = open("after_smarna_critical.txt","w")
for c in Crit:
    f1.write(str(c)+"\n")
f1.close()


print "Done."
