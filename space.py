import pygame, sys
from pygame.locals import *
import random
import time

pygame.init()

FPS=50

fpsClock=pygame.time.Clock()

WIN=pygame.display.set_mode((800,600))

pygame.display.set_caption("SPACE")

playerImg=pygame.image.load("player.png")

playerX=370

playerY=480
alienImg=[]
for i in range(6):
    alienImg.append(pygame.image.load("alien.png"))
alienX=[]
for i in range(6):
    alienX.append(random.randint(0,736))
alienY=[]
for i in range(6):
    alienY.append(random.randint(50,200))
changeX=[]
for i in range(6):
    changeX.append(3)


score=0

bgImg=pygame.image.load("background.png")

bulletImg=pygame.image.load("bullet.png")

fontObj=pygame.font.Font("freesansbold.ttf",32)

pygame.mixer.music.load("bg.mp3")

shoot=pygame.mixer.Sound("gun.mp3")

collide=pygame.mixer.Sound("collision.wav")

overgame=pygame.mixer.Sound("over.mp3")

pygame.mixer.music.play(-1,0.0)

bulletState="ready"

bulletY=480

bulletX=386

m=1


def fire_bullet(x,y):
    WIN.blit(bulletImg,(x,y))
    global bulletState
    bulletState="fire"
    global bulletX
    bulletX=x

def over():
    fontObj=pygame.font.Font("./beauti_font.otf",64)

    fontSurf=fontObj.render("GAME OVER",True,(255,255,255))

    fontRect=fontSurf.get_rect()

    fontRect.center=(400,300)

    WIN.blit(fontSurf,fontRect)

def collision(ax,ay,bx,by):
    distance=[]
    for i in range(6): 
        distance.append(((bx-ax[i])**2+(by-ay[i])**2)**(1/2))
        if(distance[i]<=64):
            collide.play()
            return [True,i]
    else:
        return [False,0]
        
while True:
    WIN.blit(bgImg,(0,0))
    fontSurf=fontObj.render(f"Score : {score}",True,(255,255,255))
    WIN.blit(fontSurf,(0,0))
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()   
            sys.exit()
        if event.type==KEYDOWN:
            if event.key==K_SPACE:
                shoot.play()
                fire_bullet(playerX+16,bulletY)

    pressed=pygame.key.get_pressed()
    if pressed[K_LEFT]:
        playerX-=5
    if pressed[K_RIGHT]:
        playerX+=5
    
    if playerX<=0:
        playerX=0
    if playerX>=736:
        playerX=736


    for i in range(6):
        alienX[i]+=changeX[i]

    for i in range(6):
        if alienY[i]>=420:
            for j in range(6):
                alienY[j]=2000
            over()
            if(m==1):
                m=2
                pygame.mixer.music.stop()
                overgame.play()
                time.sleep(0.4)
                overgame.stop()
                pygame.mixer.music.play()
                break
        if alienX[i]<=0:
            changeX[i]=3
            alienY[i]+=40
        if alienX[i]>=736:
            changeX[i]=-3
            alienY[i]+=40
    
    isCollision=collision(alienX,alienY,bulletX,bulletY)
    if(isCollision[0]):
        score+=1
        bulletState="ready"
        bulletY=480
        bulletX=386
        alienX[isCollision[1]]=random.randint(0,736)
        alienY[isCollision[1]]=random.randint(50,200)

    if bulletState == "fire":
            fire_bullet(bulletX,bulletY)
            bulletY-=10
            if bulletY<=(-32):
                bulletState="ready"
                bulletY=480
                bulletX=386


    WIN.blit(playerImg,(playerX,playerY))
    for i in range(6):
        WIN.blit(alienImg[i],(alienX[i],alienY[i]))
    pygame.display.update()
    fpsClock.tick(FPS)