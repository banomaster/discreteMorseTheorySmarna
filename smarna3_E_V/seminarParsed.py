
TriFromEdg = dict()
VerUsed = set()
EdgUsed = set()

with open("smarna_edg_arrows.txt") as f:
    index = 0
    for line in f:
      line = line.strip()[1:-1]
      lineSplit = line.split(':')
      edge = tuple(map(int,(lineSplit[0])[1:-1].split(',')))
      minT = lineSplit[1].strip()
      if minT != "None":
        print edge
        print index
        triangle = tuple(map(int,(minT)[1:-1].split(',')))
        TriFromEdg[minT]=edge
        EdgUsed.add(edge)

      index += 1

print TriFromEdg