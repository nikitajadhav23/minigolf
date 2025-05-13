from utils import *
def djikstra(app):
     visited = {} #keeps track of the nodes we visit
     parentMap = {}
     distanceMap = {}  #maps the node to its distance from the source
     sourceRow, sourceCol = getCell(app, app.cx, app.cy)
     source = (sourceRow, sourceCol)
     target = (0, app.flagCol)
     for row in range(len(app.board)):
         for col in range(len(app.board[0])):
             distanceMap[(row, col)] = 100000
             visited[(row,col)] = False
     distanceMap[source] = 0
     curr = source
     while curr!=target:
        currRow, currCol = curr
        neighbors = []
        for dx, dy in [(1,0),(1, 1), (1,-1),(0, -1), (0,1),(-1, 0), (-1, 1), (-1, -1)]:
            if currRow+dx>=0 and currRow+dx<app.rows and currCol+dy>=0 and currCol+dy<app.cols and visited[(currRow+dx, currCol+dy)]==False:
                neighbors.append((currRow+dx, currCol+dy))
        minCost = 100000
        for neighbor in neighbors:
            currCost = 0
            row, col = neighbor
            if neighbor == (currRow+1, currCol+1) or neighbor == (currRow+1,currCol-1) or neighbor == (currRow-1, currCol+1) or neighbor == (currRow-1, currCol-1):
                currCost = 1+ app.board[row][col]*10
            elif neighbor == (currRow, currCol+1) or neighbor==(currRow, currCol-1):

                currCost = 0.5+ app.board[row][col]*10
            else:
                currCost = app.board[row][col]*10
            
            if currCost<distanceMap[neighbor]:
                distanceMap[neighbor] = currCost
                parentMap[neighbor] = curr
        visited[curr] = True
        curr = findNextNode(visited, distanceMap)
    
     app.path = extractPath(parentMap, target, source)
     calculatePar(app)

def findNextNode(visited, distanceMap):
     minimum = 10000000
     for node in distanceMap:
         if visited[node]==False:
            if distanceMap[node]<minimum:
                minimum = distanceMap[node]
                nextNode = node
     return nextNode if nextNode!=None else 0
def extractPath(parentMap, target, source):
     path = []
     curr = target
     while curr!=source:
        path.append(curr)
        curr = parentMap[curr]
     path.append(source)
     return path
 
def calculatePar(app):
    if len(app.path)<=4:
        app.par = 3
    elif len(app.path)>4 and len(app.path)<6:
        app.par = 4
    else:
        app.par = 5
