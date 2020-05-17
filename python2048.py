import pygame
from pygame.locals import *
from random import *

BOARD_SIZE = int(input("enter integer-"))
x= int(input("win on--"))

pygame.init()

SURFACE = pygame.display.set_mode((400,500),0,32)
pygame.display.set_caption("2048-Daniyal")

myfont = pygame.font.SysFont("monospace",20)
scorefont = pygame.font.SysFont("monospace",30)

tileMatrix = [[0 for i in range(0,BOARD_SIZE)] for j in range(0,BOARD_SIZE)]
undoMat = []

def main(fromLoaded = False):
    
    if not fromLoaded:
        placeRandomTile()
    printMatrix()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if checkIfCanGo() == True:
                if event.type == KEYDOWN:
                    if isArrow(event.key):
                        rotations = getRotations(event.key)
                        addToUndo()
                        for i in range(0,rotations):
                            rotateMatrixClockwise()

                        if canMove():
                            moveTiles()
                            mergeTiles()
                            placeRandomTile()

                        for j in range(0,(4-rotations)%4):
                            rotateMatrixClockwise()
                            
                        printMatrix()
                    global BOARD_SIZE
                    for i in range(0,BOARD_SIZE):
                        for j in range(0,BOARD_SIZE):
                            if tileMatrix[i][j]==x:
                                win()
                    
            else: 
                printGameOver()
             
            if event.type == KEYDOWN:
                if event.key == pygame.K_r:
                 
                    reset()
                if 50<event.key and 56 > event.key:
                    
                    BOARD_SIZE = event.key - 48
                    reset()
                if event.key == pygame.K_s:
                   
                    saveGameState()
                elif event.key == pygame.K_l:
                    loadGameState()
                    
                elif event.key == pygame.K_u:
                    undo() 
                
        pygame.display.update()

def canMove():
    for i in range(0,BOARD_SIZE):
        for j in range(1,BOARD_SIZE):
            if tileMatrix[i][j-1] == 0 and tileMatrix[i][j] > 0:
                return True 
            elif (tileMatrix[i][j-1] == tileMatrix[i][j]) and tileMatrix[i][j-1] != 0:
                return True
    return False
 
def moveTiles():
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE-1):
            
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0:
                for k in range(j,BOARD_SIZE-1):
                    tileMatrix[i][k] = tileMatrix[i][k+1]
                tileMatrix[i][BOARD_SIZE-1] = 0

def mergeTiles():

    for i in range(0,BOARD_SIZE):
        for k in range(0,BOARD_SIZE-1):
            if tileMatrix[i][k] == tileMatrix[i][k+1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k]*2
                tileMatrix[i][k+1] = 0 
                moveTiles()

def placeRandomTile():
    c = 0
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE):
            if tileMatrix[i][j] == 0:
                c += 1 
    
    k = floor(random())
    print("click")

    while tileMatrix[floor(k/BOARD_SIZE)][k%BOARD_SIZE] != 0:
        k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    tileMatrix[floor(k/BOARD_SIZE)][k%BOARD_SIZE] = 2

def floor(n):
     return int(n - (n % 1 ))  
BLACK=(0,0,0)
RED=(255,0,0)
ORANGE=(255,152,0)
DEEP_ORANGE=(255,87,34)
BROWN=(121,85,72)
GREEN=(0,128,0)
L_GREEN=(139,195,74)
TEAL=(0,150,136)
BLUE=(33,150,136)
PURPLE=(156,39,176)
PINK=(234,30,99)
DEEP_PURPLE=(103,58,183)

color_dict = {
    0:BLACK,2:RED,4:GREEN,8:PURPLE,16:DEEP_PURPLE,32:DEEP_ORANGE,64:TEAL,128:L_GREEN,256:PINK,512:ORANGE,1024:BLACK,2048:BROWN,4096:RED
}

def getColor(i):
    return color_dict[i]
def printMatrix():

        SURFACE.fill(BLACK)
        global BOARD_SIZE
        global x
        for i in range(0,BOARD_SIZE):
            for j in range(0,BOARD_SIZE):
                pygame.draw.rect(SURFACE,getColor(tileMatrix[i][j]),(i*(400/BOARD_SIZE),j*(400/BOARD_SIZE)+100,400/BOARD_SIZE,400/BOARD_SIZE))
                label = myfont.render(str(tileMatrix[i][j]),1,(255,255,255))
                label2=scorefont.render("winning score:"+ str(x) ,1,(255,255,255))
                SURFACE.blit(label,(i*(400/BOARD_SIZE)+30,j*(400/BOARD_SIZE)+130))
                SURFACE.blit(label2,(10,20))

def checkIfCanGo():
    for i in range(0,BOARD_SIZE ** 2): 
        if tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE] == 0:
            return True
    
    for i in range(0,BOARD_SIZE):
        for j in range(0,BOARD_SIZE-1):
            if tileMatrix[i][j] == tileMatrix[i][j+1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j+1][i]:
                return True
    return False

def convertToLinearMatrix():

    mat = []
    for i in range(0,BOARD_SIZE ** 2):
        mat.append(tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE])
        
    return  mat
def addToUndo():
    undoMat.append(convertToLinearMatrix())   
def rotateMatrixClockwise():
    for i in range(0,int(BOARD_SIZE/2)):
        for k in range(i,BOARD_SIZE- i- 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

            tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
            tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
            tileMatrix[i][k] = temp4

def printGameOver():
    SURFACE.fill(BLACK)
    label = scorefont.render("you lose!",1,(255,255,255))
    label3 = myfont.render("press 'R' to play again!! ",1,(255,255,255))
    SURFACE.blit(label,(50,100))
    SURFACE.blit(label3,(50,300))

def reset():
    global tileMatrix  
    SURFACE.fill(BLACK)
    tileMatrix = [[0 for i in range(0,BOARD_SIZE)] for j in range(0,BOARD_SIZE) ]
    main()

def saveGameState():
    f = open("savedata","w")
    line1 = " ".join([str(tileMatrix[floor(x/BOARD_SIZE)][x%BOARD_SIZE]) for x in range(0,BOARD_SIZE ** 2)])
    f.write(line1+"\n")
    f.write(str(BOARD_SIZE)+"\n")
    f.close()

def win():
    SURFACE.fill(RED)
    label1 = scorefont.render("you win!",1,(255,255,255))
    label2 = myfont.render("press 'R' to play again!! ",1,(255,255,255))
    SURFACE.blit(label1,(50,100))
    SURFACE.blit(label2,(50,300))
        
def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()

        for i in range(0,BOARD_SIZE ** 2):
            tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE] =  int(mat[i])       
        printMatrix()

def loadGameState():
    global BOARD_SIZE
    global tileMatrix

    f = open("savedata","r")
    mat = (f.readline()).split(' ',BOARD_SIZE ** 2)
    BOARD_SIZE = int(f.readline())
    
    for i in range(0,BOARD_SIZE ** 2):
        tileMatrix[floor(i/BOARD_SIZE)][i%BOARD_SIZE] = int(mat[i]) 

    f.close()
    main(True)

def isArrow(k):
    return (k == pygame.K_w or k == pygame.K_s or k == pygame.K_a or k == pygame.K_d)

def getRotations(k):
    if k == pygame.K_w:
        return 0
    elif k == pygame.K_s:
        return 2 
    elif k == pygame.K_a:
        return 1
    elif k == pygame.K_d:
        return 3
main()


  