from cmu_graphics import *
from utils import *
class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.width, self.height = 500, 700
        self.widthMargin = 10
        self.headerMargin = 45
        self.footMargin = 10
        self.boardLeft = self.widthMargin
        self.boardTop = 75
        self.boardWidth = self.width - 2*self.widthMargin
        self.boardHeight = self.height - self.headerMargin - self.footMargin
        self.cellBorderWidth = 2
    def getCellCoordinates(self, row, col):
        cellWidth, cellHeight = getCellSize(self)
        cellLeft, cellTop = getCellLeftTop(self, row, col)
        cx = cellLeft + cellWidth/2
        cy = cellTop + cellHeight/2
        return (cx, cy)
    def getCellSize(self):
        cellWidth = self.boardWidth / self.cols
        cellHeight = self.boardHeight / self.rows
        return (cellWidth, cellHeight)
    def getCell(self, x, y):
        cellWidth, cellHeight = getCellSize(self)
        col = int((x - self.boardLeft) // cellWidth)
        row = int((y - self.boardTop) // cellHeight)
        return (row, col)
     
class Water:
    def __init__(self, rows, cols):
        self.number = 2
        self.rows = rows
        self.cols = cols
    def load(self, row, col):
        board = Board(self.rows, self.cols)
        cx, cy = board.getCellCoordinates(row, col)
        
    def draw(self, cx, cy, cellWidth, cellHeight):
        drawImage('Water.png', cx, cy, align='center', width=cellWidth, height=cellHeight)

class Bunker:
    def __init__(self, rows, cols):
        self.number = 1
        self.rows = rows
        self.cols = cols
    def load(self, row, col):
        board = Board(self.rows, self.cols)
        cx, cy = board.getCellCoordinates(row, col)
    def draw(self, cx, cy, cellWidth, cellHeight):
        drawImage('bunker.png', cx, cy, align='center', width=cellWidth, height=cellHeight)
# class Tree:
#     def __init__(self, rows, cols):
#         self.number = 3
#         self.rows = rows
#         self.cols = cols
#     def draw(self, cx, cy, cellWidth, cellHeight):