from cmu_graphics import *
from pathfinding import *
from objectClasses import *
from utils import *
import random
def onAppStart(app):
    resetApp(app)
def resetApp(app):
    app.cx = 200
    app.cy = 500
    app.dx = 0
    app.dy = 0
    app.friction = 0.9
    app.flagX = 100
    app.flagY = 100
    app.holeX = 100
    app.holeY = 120
    app.holeRadius = 20
    app.ballRadius = 8
    app.greenRadius = 80
    app.width, app.height = 500, 700
    app.rows = None
    app.cols = None
    app.widthMargin = 10
    app.headerMargin = 45
    app.footMargin = 10
    app.boardLeft = app.widthMargin
    app.boardTop = 75
    app.boardWidth = app.width - 2*app.widthMargin
    app.boardHeight = app.height - app.headerMargin - app.footMargin
    app.cellBorderWidth = 2
    app.waterNum = 2
    app.bunkerNum = 1
    app.holesCompleted = 0
    app.holeCompleted = False
    app.board = None
    app.stepsPerSecond = 10
    app.isBoardWon = False
    app.counter = 0
    app.startScreen = True
    app.aiming = False
    app.mouseLoc = 0
    app.mouseLocY = 0
    app.shoot = False
    app.stepsPerSecond = 7
    app.paused = False
    app.angle = 0
    app.mouseLoc
    app.score = 0
    app.par = 0
    app.toPar = 'even'
    app.flagCol = None
    app.flagRow = 0
    app.gameOver = False
    app.hideHole = False
    app.startScreen = True
    app.pressingPlay = False
    app.playX = 250
    app.playY = 500
    app.playWidth = 70
    app.playHeight = 50
    app.hint = False
    app.hasBeenDragged = None
    app.hideGreen = True
    app.levelUp = False
    app.pressingInformation = False
    holeGenerator(app)

def redrawAll(app):
    if app.startScreen:
        drawImage('golfStart.png', 250, 350, align='center')        
        if app.pressingPlay:
            drawImage('golfPressed.png', 250, 350, align='center')
        elif app.pressingInformation:
            drawImage('information.png', 250, 350, align='center')
            
    elif app.isBoardWon==False and app.gameOver==False:
        drawBoard(app)
        if app.hideGreen==False:
            drawFlag(app)
        drawBall(app)
        drawRect(0, 0, 500, 75, fill='pink')
        drawLabel(f'Score: {app.score}', 50, 20, size = 20, bold = True, font='cursive')
        drawLabel(f'Par: {app.par}', 50, 40, size = 20, bold = True, font='cursive')
        drawLabel(f'Max Score: {app.par+3}', 180, 40, size = 20, bold = True, font='cursive')
        drawLabel(f'Score to Par: {app.toPar}', 200, 20, size = 20, bold = True, font='cursive')
        drawLabel(f'Holes Completed: {app.holesCompleted}', 100, 60, size = 20, bold = True, font='cursive')

    if app.holeCompleted==True:
        drawRect(0, 0, 500, 700, fill = 'green', opacity = 50)
        drawLabel(f'Hole Completed, Press right arrow for the next hole', 250, 320, size = 18, align = 'center', bold = True)
    if app.levelUp==True:
        drawRect(0, 0, 500, 700, fill = 'yellow', opacity = 50)
        drawLabel(f'LEVEL UP', 250, 400, size = 50, align = 'center', bold = True)
    elif app.gameOver==True:
        gameOver(app)
    if app.aiming==True:
        drawArrow(app, app.mouseLoc, app.mouseLocY)
    if app.hint==True:
        drawPath(app)
    
def gameOver(app):
    drawRect(0, 0, 500, 700, fill = 'red', opacity = 50)
    drawLabel('GAME OVER', 250, 320, size = 50, align = 'center', bold = True)
    drawLabel(f'Number of holes completed: {app.holesCompleted}', 250, 360, size = 30, align = 'center', bold = True)
    drawLabel("Press 'r' to try again!", 250, 440, size = 30, align = 'center', bold = True)
    drawLabel(f'Score to Par:{app.toPar}', 250, 400, size = 30, align = 'center', bold = True)
def holeGenerator(app):
    app.levelUp = False
    app.hideHole = False
    app.score = 0
    app.hideGreen = True
    getDifficulty(app)
    board = Board(app.rows, app.cols)
    app.board = [[0]*board.cols for row in range(board.rows)]
    addObstacles(app)
    placeFlag(app)
    rows = board.rows
    cols = board.cols
    app.cx, app.cy = board.getCellCoordinates(rows-1, cols//2)
    app.isBoardWon = False
    djikstra(app)


def drawBall(app):
    if not app.holeCompleted or not app.levelUp:
        drawCircle(app.cx, app.cy, app.ballRadius, fill='white', border='black')

def placeFlag(app):
    for col in range(len(app.board[0])):
        flagChance = random.randint(0,6)
        if flagChance<3:
            if app.board[0][col]==0:
                app.flagCol = col
                break
     
def drawFlag(app):
    cellWidth, cellHeight = getCellSize(app)
    board = Board(app.rows, app.cols)
    cx, cy = board.getCellCoordinates(app.flagRow, app.flagCol)
    drawImage('flag.png', cx, cy, align='center', width=cellWidth, height=cellHeight)
    drawGreen(app, cx, cy)
    drawHole(app, cx, cy)

def drawHole(app, cx, cy):
    if not app.hideHole:
        drawOval(cx-5, cy+15, app.holeRadius,app.holeRadius//1.5, fill='white', border='brown')
     
def drawGreen(app, cx, cy):
    greenCenterX = cx
    greenCenterY = cy+20
    drawOval(greenCenterX, greenCenterY, app.greenRadius,app.greenRadius//2, fill='lightgreen')
    app.board[0][app.flagCol] = 3

def drawArrow(app, mouseX, mouseY):
    if app.arrowEnd!=None and app.aiming==True:
        x1, y1 = app.arrowEnd
        drawLine(app.cx, app.cy, x1, y1, dashes=True)
        drawRegularPolygon(app.cx, app.cy, 5, 3, rotateAngle = app.angle)
 
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth+1, cellHeight+1,
             fill= color)
def drawBoard(app):
    board = Board(app.rows, app.cols)
    for row in range(board.rows):
        for col in range(board.cols):
            color = 'green'
            drawCell(app, row, col, color)
            if app.board[row][col] == 1: #is bunker
                bunker = Bunker(app.rows, app.cols)
                board = Board(app.rows, app.cols)
                bunker.load(row, col)
                cx, cy = board.getCellCoordinates(row, col)
                cellWidth, cellHeight = getCellSize(app)
                bunker.draw(cx, cy, cellWidth, cellHeight)
            elif app.board[row][col] == 2: #is water
                water = Water(app.rows, app.cols)
                board = Board(app.rows, app.cols)
                water.load(row, col)
                cx, cy = board.getCellCoordinates(row, col)
                cellWidth, cellHeight = getCellSize(app)
                water.draw(cx, cy, cellWidth, cellHeight)
def drawPath(app):
    for i in range(len(app.path)-1):
        startRow, startCol = app.path[i]
        board = Board(app.rows, app.cols)
        startX, startY = board.getCellCoordinates(startRow, startCol)
        endRow, endCol = app.path[i+1]
        endX, endY = board.getCellCoordinates(endRow, endCol)
        drawLine(startX, startY, endX, endY, dashes=True)
def showHole(app):
    row, col = getCell(app, app.cx, app.cy)
    if row<3:
        app.hideGreen = False
def addObstacles(app):
    totalObstacles = 0
    for x in range(2, app.rows-2):
        totalNumberofObstaclesinRow = 0
        for y in range(app.cols): #going through each of the cells in the grass
            if totalObstacles<app.maxObstacles:
                obstacleList = ['bunker', 'water']
                whichObstacle = random.randint(0,1) #randomly deciding if the obstacle is a bunker or water
                if obstacleList[whichObstacle] == 'bunker': 
                    bunker = Bunker(app.rows, app.cols)
                    obstacleNum = bunker.number #1 is bunker
                elif obstacleList[whichObstacle] == 'water':
                    water = Water(app.rows, app.cols)
                    obstacleNum = water.number #2 is water 
                gettingObstacleChance = random.randint(0,6) 
                if gettingObstacleChance == 1: #1/5 chance of putting the obstacle down on the grass 
                    if totalNumberofObstaclesinRow == 3:  #check if the totalNumberofObstacles in a row is the maxNumofObstacles 
                        break
                    else:
                        totalNumberofObstaclesinRow += 1 
                        app.board[x][y] = obstacleNum
                        totalObstacles+=1

###Mouse press, release, and user interaction features
def onMousePress(app, mouseX, mouseY):
    app.arrowEnd = None
    app.mouseLoc = mouseX
    if app.startScreen and mouseY>500 and mouseY<600 and mouseX<400 and mouseX>200:
        app.startScreen = False
        app.hasBeenDragged = False
    elif touchingBall(app, mouseX, mouseY):
        app.aiming = True
    elif app.startScreen and mouseY>100 and mouseY<200 and mouseX<500 and mouseX>400:
        app.pressingInformation = True
def onMouseMove(app, mouseX, mouseY):
    if app.startScreen and mouseX<350 and mouseX>200 and mouseY<600 and mouseY>500:
        app.pressingPlay = True
    app.mouseLoc = mouseX
    app.mouseLocY = mouseY

def onMouseRelease(app, mouseX, mouseY):
    app.aiming = False
    if app.shoot == False:
        if mouseX<app.cx and mouseY>app.cy:
            app.dx = 0.25*abs(mouseX-app.cx)
            app.dy = -0.25*abs(mouseY-app.cy)
        elif mouseX>app.cx and mouseY>app.cy:
            app.dx = -0.25*abs(mouseX-app.cx)
            app.dy = -0.25*abs(mouseY-app.cy)
        elif mouseX<app.cx and mouseY<app.cy:
            app.dx = 0.25*abs(mouseX-app.cx)
            app.dy = 0.25*abs(mouseY-app.cy)
        elif mouseX>app.cx and mouseY<app.cy:
            app.dx = -0.25*abs(mouseX-app.cx)
            app.dy = 0.25*abs(mouseY-app.cy)
        if app.hasBeenDragged == False:
            app.dx = 0
            app.dy = 0
    app.shoot = True
    app.hint = False
    if app.hasBeenDragged == True:
        app.score+=1
        calculateToPar(app)
    
   
def onMouseDrag(app, mouseX, mouseY):
    app.hasBeenDragged = True
    app.arrowEnd = (mouseX, mouseY)
 
def onKeyPress(app, key):
    if app.holeCompleted and key=='right':
        holeGenerator(app)
        app.holeCompleted = False
    elif key=='r':
        resetApp(app)
    elif key=='h':
        djikstra(app)
        app.hint = True
        
def touchingBall(app, mouseX, mouseY):
    if abs(mouseX-app.cx)<app.ballRadius and abs(mouseY-app.cy)<app.ballRadius:
        return True
 
def takeStep(app):
    if app.startScreen==False:
        if app.hasBeenDragged ==True:
            app.cx+=app.dx
            app.cy+=app.dy
            row, col = getCell(app, app.cx, app.cy)
            if row>3:
                newRow = app.board.pop()
                app.board.insert(0, newRow)
            if app.hideGreen == False and abs(row-app.flagRow)>1:
                if app.dy<0 and app.flagRow>0:
                    app.flagRow+=1
                elif app.dy>0 and app.flagRow>0:
                    app.flagRow-=1
    if isMoveLegal(app)==False:
        #reverses the move, and creates a bouncing effect
        app.cx-=5*app.dx
        app.cy-=5*app.dy
    app.dx*=app.friction
    app.dy*=app.friction
    
def onStep(app):
    if app.shoot:
        if abs(app.dy)>1 or abs(app.dx)>1:
            takeStep(app)
            if not isMoveLegal(app):
                app.cx-=app.dx
                app.cy-=app.dy
            showHole(app)
        else:
            app.shoot = False
    board = Board(app.rows, app.cols)
    cx, cy = board.getCellCoordinates(app.flagRow, app.flagCol) #gets location of hole
    holeCompleted(app, cx, cy) #checks if the ball is in the hole on step
    ballOnGreen(app, cx, cy)
    isGameOver(app)
     
 
###checking if the ball is in the hole
def holeCompleted(app, cx, cy):
    if abs(app.cy-cy)<app.holeRadius and abs(app.cx-cx)<app.holeRadius and checkingBallVelocity(app):
        ballEnteringHole(app)
        app.shoot = False
        app.holesCompleted += 1
#animation for when the ball enters the hole
def ballEnteringHole(app):
    board = Board(app.rows,app.cols)
    cx, cy = board.getCellCoordinates(0, app.flagCol)
    app.cx = cx
    app.cy = cy+20
    app.hideHole = True
    app.holeCompleted = True
    if app.holesCompleted>0 and app.holesCompleted%3==0:
        app.levelUp = True
#the green has less friction than other surfaces, so the ball rolls faster
def ballOnGreen(app, cx, cy):
    greenCenterX = cx
    greenCenterY = cy+20
    if abs(app.cx-greenCenterX)<app.greenRadius*2 and abs(app.cy-greenCenterY)<app.greenRadius:
        app.friction = 0.95
def checkingBallVelocity(app):
    if app.dy<2: #if the dy value (size of increase in y) is less than 10, the ball is at a velocity that can go into the hole
        return True
    else:
        return False
def showNextHole(app):
    cellWidth, cellHeight = getCellSize(app)
    if abs(app.flagY-app.holeY)>cellHeight//2:
        app.isBoardWon = True

def isMoveLegal(app):
    topLeft = (app.cx - app.ballRadius/2, app.cy - app.ballRadius/2)
    topRight = (app.cx + app.ballRadius/2, app.cy - app.ballRadius/2)
    bottomLeft = (app.cx - app.ballRadius/2, app.cy + app.ballRadius/2)
    bottomRight = (app.cx + app.ballRadius/2, app.cy + app.ballRadius/2)
    for cornerX, cornerY in [topLeft, topRight, bottomLeft, bottomRight]:
        cornerRow, cornerCol = getCell(app, cornerX, cornerY)
        #is the ball in bounds
        if (cornerRow < 0 or app.rows <= cornerRow or
              cornerCol < 0 or app.cols <= cornerCol):
            return False
        # is the ball on an obstacle
        elif app.board[cornerRow][cornerCol]==2:
            app.shoot = False
            popBall(app)
            app.score+=1
            break
        elif app.board[cornerRow][cornerCol]==1:
            app.friction = 0.2
        elif app.board[cornerRow][cornerCol]==0:
            app.friction = 0.87
    return True
#if the user gets into the water, they gain a penalty stroke and are 'popped' out
def popBall(app):
    cellWidth, cellHeight = getCellSize(app)
    currRow, currCol = getCell(app, app.cx, app.cy)
    for dx, dy in [(0, -1), (1, 0), (-1, 0), (0, 1)]:
         newRow = currRow+dx
         newCol = currCol+dy
         if newRow>0 and newRow<app.rows and newCol>0 and newCol<app.cols:
            if app.board[newRow][newCol]==0:
                app.cx+=cellWidth*dy
                app.cy+=cellHeight*dx
                break

#difference between the player's score and the par is their score to par. This is Cumulative
def calculateToPar(app):
     if app.score>app.par:
        app.toPar = f'+{app.score-app.par}'
     elif app.score==app.par:
        app.toPar = f'even'
     elif app.score<app.par:
        app.toPar = f'-{app.par-app.score}'
#if the player is more than 3 strokes above par on a hole, they lose
def isGameOver(app):
    if app.score-app.par >= 4:
        app.gameOver = True
        app.holeCompleted = False
#every 3 holes the max number of obstacles increases, the board also gets bigger
def getDifficulty(app):
    if app.holesCompleted<3:
        app.maxObstacles = 12
        app.rows = random.randint(13, 15)
        app.cols = random.randint(6, 8)
        app.board = Board(app.rows, app.cols)
      
    elif app.holesCompleted%3==0:
        app.maxObstacles+=2
        app.rows = random.randint(15, 17)
        app.cols = random.randint(8, 10)
        app.board = Board(app.rows, app.cols)
  
#the number of nodes in app.path indicates the distance it would take the computer to pay the hole. 
#The larger the distance, the harder the hole, and the higher the par
def calculatePar(app):
    if len(app.path)<=20:
        app.par = 3
    elif len(app.path)>20 and len(app.path)<30:
        app.par = 4
    else:
        app.par = 5

def main():
    runApp()

main()

##citations:
#image citations: Flag - https://www.pngall.com/golf-png/
#djikstra algorithm - used the 112 pathfinding lecture video and guide on pathfinding (https://www.cs.cmu.edu/~112/notes/student-tp-guides/Pathfinding.pdf) to write the djikstra algorithm 
#used ideas from my hack 112 project crossy road