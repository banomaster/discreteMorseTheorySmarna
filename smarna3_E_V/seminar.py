import numpy as np
from scipy.spatial import Delaunay

f = open("smarna.txt")
pointValue = dict()
indPoint = dict()
indHight = dict()

ind = 0

for l in f:
     l=l[:-1]
     l = str.split(l,"  ")
     l=[np.float64(e) for e in l]
     p=(l[0],l[1])
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
f1 = open("smarna_tri.txt","w")
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
    Eind.add(e0)
    Eind.add(e1)
    Eind.add(e2)

#print(vertexEdge)
#print(edgeTriangle)
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
    f1.write(str(pair) + "\n")
f1.close()
#GRADIENT E -> T

# with open("smarna_edg_arrows.txt") as f:
#     for line in f:
        

#GRADIEN V -> E
EdgFromVer = dict()
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

    f1.write(str(pair)+"\n")
f1.close()



#GRADIENT V -> E
print("END gradient")


print("START critical")
VerCri = set(vertexEdge.keys()).difference(VerUsed)
f1 = open("smarna_ver_critical.txt","w")
for v in VerCri:
    f1.write(str(v)+"\n")
f1.close()

EdgCri=set(edgeTriangle.keys()).difference(EdgUsed)
f1 = open("smarna_edg_critical.txt","w")
for e in EdgCri:
    eS = set(e)
    if not len(VerCri.intersection(eS)):
        f1.write(str(e)+"\n")
f1.close()

#Vsi trikotniki, od katerih odstranimo tiste na katere kaze kak edge
TriCri=set([tuple(t) for t in T]).difference(TriFromEdg.keys())
f1 = open("smarna_tri_critical.txt","w")
for t in TriCri:
    f1.write(str(t)+"\n")
f1.close()






print("END critical")
#IZRIS 2D
import matplotlib.pyplot as plt
V=np.array([list(v) for v in V])
plt.triplot(V[:,0], V[:,1], T.copy())
plt.plot(V[:,0], V[:,1], '.')
plt.savefig("smarna_tri")


