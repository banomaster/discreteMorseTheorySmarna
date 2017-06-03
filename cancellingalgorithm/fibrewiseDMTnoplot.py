import random
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.backends.backend_pdf import PdfPages

S1 = [(1, 2), (1, 5), (2, 3), (3, 4), (4, 5)]

# balls
B2 = [(1, 2, 3)]

# spheres
S1 = [(1, 2), (1, 4), (2, 3), (3, 4)]
S2 = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
S1VS1 = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]

# torus
T = [(1, 2, 4), (2, 4, 6), (2, 3, 6), (3, 6, 8), (1, 3, 8),
     (1, 4, 8), (4, 5, 6), (5, 6, 7), (6, 7, 8), (7, 8, 9),
     (4, 8, 9), (4, 5, 9), (1, 5, 7), (1, 2, 7), (2, 7, 9),
     (2, 3, 9), (3, 5, 9), (1, 3, 5)]

# Klein bottle
K = [(1, 2, 4), (2, 4, 6), (2, 3, 6), (3, 6, 8),
     (1, 3, 8), (1, 5, 8), (4, 5, 6), (5, 6, 7),
     (6, 7, 8), (7, 8, 9), (5, 8, 9), (4, 5, 9),
     (1, 5, 7), (1, 2, 7), (2, 7, 9), (2, 3, 9),
     (3, 4, 9), (1, 3, 4)]

# cylinder
C = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (1, 5, 6), (1, 2, 6)]

# Moebius band
M = [(1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (2, 5, 6), (1, 2, 6)]

# dunce hat (contractible, not collapsible)
D = [(1, 2, 5), (1, 5, 6), (1, 6, 7), (1, 2, 7), (1, 4, 9), (1, 9, 10), (1, 10, 11), (1, 4, 11),
     (1, 2, 13), (1, 13, 14), (1, 14, 15), (1, 4, 15),
     (2, 3, 5), (2, 3, 7), (3, 4, 9), (3, 4, 11), (2, 3, 13), (3, 4, 15),
     (3, 7, 8), (3, 8, 9), (3, 11, 12), (3, 12, 13), (3, 15, 16), (3, 5, 16),
     (5, 6, 17), (5, 16, 17), (6, 7, 17), (7, 8, 17), (8, 9, 17), (9, 10, 17), (10, 11, 17), (11, 12, 17),
     (12, 13, 17), (13, 14, 17), (14, 15, 17), (15, 16, 17)]

# projective plane
RP2 = [(1, 3, 5), (1, 2, 6), (1, 5, 6), (1, 2, 4), (1, 3, 4),
       (2, 3, 5), (2, 3, 6), (2, 4, 5), (3, 4, 6), (4, 5, 6)]

# hypercubes
Q4 = [( 1,  4, 14, 15), ( 1,  6, 12, 15), ( 1,  7, 12, 14), ( 1,  8, 10, 15), ( 1,  8, 11, 14), ( 1,  8, 12, 13),
     ( 2,  3, 13, 16), ( 2,  5, 11, 16), ( 2,  7,  9, 16), ( 2,  7, 11, 14), ( 2,  7, 12, 13), ( 2,  8, 11, 13),
     ( 3,  5, 10, 16), ( 3,  6,  9, 16), ( 3,  6, 10, 15), ( 3,  6, 12, 13), ( 3,  8, 10, 13), ( 4,  5,  9, 16),
     ( 4,  5, 10, 15), ( 4,  5, 11, 14), ( 4,  6,  9, 15), ( 4,  7,  9, 14), ( 5,  8, 10, 11), ( 6,  7,  9, 12),
     ( 1,  4,  6, 10, 15), ( 1,  4,  7, 11, 14), ( 1,  6,  7, 12, 13), ( 1,  8, 10, 11, 13), ( 1,  8, 12, 14, 15),
     ( 2,  3,  5,  9, 16), ( 2,  3,  8, 12, 13), ( 2,  5,  8, 11, 14), ( 2,  7,  9, 12, 14), ( 2,  7, 11, 13, 16),
     ( 3,  5,  8, 10, 15), ( 3,  6,  9, 12, 15), ( 3,  6, 10, 13, 16), ( 4,  5,  9, 14, 15), ( 4,  5, 10, 11, 16),
     ( 4,  6,  7,  9, 16), ( 1,  4,  6,  7, 10, 11, 13, 16), ( 2,  3,  5,  8,  9, 12, 14, 15)]

# ====================================================================================================================


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


# construct a product of two copies of X
def pr(X):

    A = []
    All = allsc(X)
    for a in All:
        for b in All:
            A.append((a, b))
    A.sort(key=dim)
    return A


# given a cube in the product, find its dimension
def dimcub(s, t):

    return len(s) + len(t) - 2


# returns the dimension of a given simplex
def dim(s):

    return len(s) - 1


# construct the cubical diagonal
def ddiag(X):

    A = []
    All = allsc(X)
    for a in All:
        A.append((a, a))
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


# ====================================================================================================================


# test if adding an arrow to the vector field creates a closed loop
def makes_loop(alpha, beta, Paths):

    p = dim(alpha)
    B = boundary(beta)
    for A in Paths:
        if dim(A[0][0]) == p:
            is_face_of = []
            is_coface_of = []
            for i in range(len(A)):
                if alpha in boundary(A[i][1]):
                    is_face_of.append(i)
                if A[i][0] in B:
                    is_coface_of.append(i)
            if is_face_of != [] and is_coface_of != [] and is_face_of[0] > is_coface_of[0]:
                return True
    return False


# ====================================================================================================================


# update the list of maximal paths after adding an arrow from alpha to beta
def path_update(alpha, beta, Paths):

    P = [path for path in Paths]
    p = dim(alpha)
    Bbeta = boundary(beta)
    is_face_of = []
    is_coface_of = []

    # go through all paths and check if the given pair fits in somewhere

    for A in Paths:
        if dim(A[0][0]) == p:
            j = Paths.index(A)
            for i in range(len(A)):
                if alpha in boundary(A[i][1]):
                    is_face_of.append((j, i))
                if A[i][0] in Bbeta:
                    is_coface_of.append((j, i))

    # if it did not, add the pair as the start of a new path

    if is_face_of == [] and is_coface_of == []:
        P.append([(alpha, beta)])

    if is_face_of == [] and is_coface_of != []:
        for m in range(len(is_coface_of)):
            (j, i) = is_coface_of[m]
            A = Paths[j]
            new_path = [(alpha, beta)]
            new_path += A[i:]
            if new_path not in P:
                P.append(new_path)
            if i == 0:
                P.remove(A)

    if is_face_of != [] and is_coface_of == []:
        for m in range(len(is_face_of)):
            (j, i) = is_face_of[m]
            A = Paths[j]
            new_path = A[:i + 1]
            new_path.append((alpha, beta))
            if new_path not in P:
                P.append(new_path)
            if i == len(A) - 1:
                P.remove(A)

    if is_face_of != [] and is_coface_of != []:
        for m in range(len(is_face_of)):
            (j, i) = is_face_of[m]
            for o in range(len(is_coface_of)):
                (k, l) = is_coface_of[o]
                A = Paths[j]
                B = Paths[k]
                new_path = A[:i + 1]
                new_path.append((alpha, beta))
                new_path += B[l:]
                if new_path not in P:
                    P.append(new_path)
                if i == len(A) - 1 and A in P:
                    P.remove(A)
                if l == 0 and B in P:
                    P.remove(B)

    return P


# ====================================================================================================================


# to print the results
# any of the variables can be set to "N/A"
def printout(Crit, Field, Paths, new=False):

    if Field != "N/A":
        if new:
            print "Vector field: "
        else:
            print "Updated vector field: "
        for v in Field:
            print v
        print ""

    if Paths != "N/A":
        if new:
            print "Paths: "
        else:
            print "Updated paths: "
        for p in Paths:
            print p
        print ""

    if Crit != "N/A":
        if new:
            print "Critical simplices: "
        else:
            print "Critical simplices after cancelling: "
        print Crit

    print ""


# ====================================================================================================================


def path_flip(alpha, beta, my_path, Crit, V):

    Q = my_path.keys()
    q = Q[0]
    k = len(q)

    # revese the path q
    qbar = [(alpha, q[k - 1][1])]
    for i in range(k - 1, 0, -1):
        qbar.append((q[i][0], q[i - 1][1]))
    qbar.append((q[0][0], beta))

    # keep a list of newly added arrows for plotting purposes

    NewV = []

    # remove old pairs from the vector field

    for pair in q:
        V.remove(pair)

    # add new pairs to the vector field

    for pair in qbar:
        V.append(pair)
        NewV.append(pair)

    # rebuild a list of maximal paths
    Paths = []
    for pair in V:
        a = pair[0]
        b = pair[1]
        Paths = path_update(a, b, Paths)

    for p in Paths:
        for pair in p:
            for e in pair:
                if e in Crit:
                    Crit.remove(e)

    # printout("N/A", "N/A", Paths)

    return Crit, V, Paths


# ====================================================================================================================


# construct a DGVF on X which is critical on the open star of s
def DGVF(X, s, seed, Priority):

    random.seed(seed)
    S = allsc(X)
    St = star(s, X)

    # all simplices in the star should be critical and will not be paired up

    Crit = St
    for c in Crit:
        S.remove(c)

    V = []
    Paths = []
    AllPairs = {}

    # create a list of all possible pairs, denoting priority (1 = has priority, 0 = already covered)

    for beta in S:
        for alpha in boundary(beta):
            if alpha not in Crit:
                if alpha in Priority or beta in Priority:
                    AllPairs[(alpha, beta)] = 1
                else:
                    AllPairs[(alpha, beta)] = 0

    # while there are any pairs left

    while AllPairs != {}:

        # choose one remaining pair at random

        PriorityPairs = [pair for pair in AllPairs if (AllPairs[pair] == 1)]
        OtherPairs = [pair for pair in AllPairs if (AllPairs[pair] == 0)]

        if PriorityPairs:
            n = len(PriorityPairs)
            i = random.randint(0, n - 1)
            (alpha, beta) = PriorityPairs[i]
        else:
            n = len(OtherPairs)
            i = random.randint(0, n - 1)
            (alpha, beta) = OtherPairs[i]

        # if it makes a loop, remove it and try again

        if makes_loop(alpha, beta, Paths):
            del AllPairs[(alpha, beta)]

        # else, add it to the vector field and
        # remove all pairs that have a simplex in common from the list of possible pairs and
        # update the list of maximal paths

        else:
            R = set()
            for pair in AllPairs:
                if alpha == pair[0] or alpha == pair[1]:
                    R.add(pair)

            for pair in AllPairs:
                if beta == pair[0] or beta == pair[1]:
                    R.add(pair)

            for pair in R:
                del AllPairs[pair]

        V.append((alpha, beta))
        Paths = path_update(alpha, beta, Paths)

    # add all simplices that did not get paired up to the list of critical simplices
    NotCrit = set()
    for v in V:
        NotCrit.add(v[0])
        NotCrit.add(v[1])
    for sx in S:
        if sx not in NotCrit:
            Crit.append(sx)

    printout(Crit, V, Paths, new = True)

    return Crit, V, Paths


# ====================================================================================================================


# given a vector field, try cancelling pairs of critical simplices to
# obtain a vector field with fewer critical cells
def cancel(X, s, Crit, V, Paths, seed):

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
    for c in Crit:
        FaceCrit[c] = list(boundary(c))
        CofaceCrit[c] = []
        n = dim(c)
        for sx in S:
            if dim(sx) == n + 1 and c in boundary(sx):
                CofaceCrit[c].append(sx)

    # build a list of pairs of critical simplices
    # with neighbouring dimensions (candidates for cancelling)
    # only consider pairs not contained in the star of s

    dims = GradCrit.keys()
    dims.sort()
    pairs_to_cancel = []
    St = star(s, X)
    if 0 in GradCrit and len(GradCrit[0]) == 1:
        dims.remove(0)
    for d in dims:
        if d + 1 in dims:
            A = GradCrit[d]
            B = GradCrit[d + 1]
            new_pairs = [(a, b) for a in A for b in B if ((a not in St and b not in St) and (a not in boundary(b)))]
            for pair in new_pairs:
                pairs_to_cancel.append(pair)

    random.seed(seed)

    # while there are pairs to cancel left, choose one at random

    while pairs_to_cancel:

        m = len(pairs_to_cancel)
        i = random.randint(0, m - 1)
        pair = pairs_to_cancel[i]

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
                        ib = p0.index(b)
                        ia = p1.index(a)
                        if ib <= ia:
                            q = tuple(p[ib:ia + 1])
                            Q = my_path.keys()
                            if Q != [] and q not in Q:
                                unique = False
                            if q in Q:
                                my_path[q].append((p, ib, ia, b, a))
                            elif my_path == {}:
                                my_path[q] = [(p, ib, ia, b, a)]
                            else:
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

        pairs_to_cancel.remove(pair)

        if unique:
            Crit, V, Paths = path_flip(alpha, beta, my_path, Crit, V)
            toRemove = []
            for p in pairs_to_cancel:
                if p[0] == alpha or p[1] == beta:
                    toRemove.append(p)
            for p in toRemove:
                pairs_to_cancel.remove(p)

    # while ends here

    printout(Crit, V, Paths)

    return Crit, V, Paths


# ====================================================================================================================


# key to sorting paths by dimension
def path_dim(a):
    return len(a[0][0])


# ====================================================================================================================


# for saving outputs
myplot = {}
pp = PdfPages('morse.pdf')
txtfile = open('morse.txt', 'w')

# choose the space here
X = D
name = "Q4"
# s = ( 2,  3,  5,  8,  9, 12, 14, 15)
s = (3, 4)

Crit, V, Paths = DGVF(X, s, name, {})
Crit, V, Paths = cancel(X, s, V, Crit, Paths, name)
euler(Crit)

print "Done."