import pygame
from pygame import Rect
import cv2
from random import randint

from Food import Food

class Player():
    def __init__(self, pos, gameDisplay, cx, cy):
        self.pos = pos
        self.vel = (1,0)
        self.nvel = (1,0)
        self.gameDisplay = gameDisplay
        self.body = []
        self.timeBetweenMoves = 20
        self.moveTimer = self.timeBetweenMoves
        self.growCount = 0
        self.dead = False
        self.cx = cx
        self.cy = cy
        self.updateControls = 10
        
        for i in range(1,5):
            self.body.insert(0, (pos[0]-i, pos[1]))

        self.cascPath = "haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(self.cascPath)

        self.video_capture = cv2.VideoCapture(0)

        self.food = self.newFood()
        
    def update(self):
        if self.dead:
            return
        
        self.moveTimer -= 1
        if self.moveTimer < 0:
            self.move()

        self.updateControls -= 1
        if self.updateControls <= 0:
            self.updateFaceControls()
            self.updateControls = 5
        
    def move(self):
        self.vel = self.nvel
         
        if self.growCount <= 0:
            del self.body[0]
            self.body.append(self.pos)
        else:
            self.growCount -= 1
            self.body.append(self.pos)

        self.pos = (self.pos[0]+self.vel[0], self.pos[1]+self.vel[1])
        self.moveTimer = self.timeBetweenMoves        

        self.checkCollision()

    def draw(self):
        self.drawCell(self.pos)
        for cell in self.body:
            self.drawCell(cell)

        self.food.draw()

    def drawCell(self, pos):
        color = 0xFFFFFF
        if self.dead:
            color = 0xFF0000
        pygame.draw.rect(self.gameDisplay, color, (pos[0]*20+2, pos[1]*20+2, 16, 16))

    def newFood(self):
        while True:
            x = randint(1, self.cx-2)
            y = randint(1, self.cy-2)

            fpos = (x,y)
            valid = self.pos != fpos
            for b in self.body:
                if b == fpos:
                    valid = False

            if valid:
                return Food(fpos, self.gameDisplay)
            
            
            

    def checkCollision(self):
        if self.pos[0] < 0 or self.pos[0] >= self.cx or self.pos[1] < 0 or self.pos[1] >= self.cy:
            self.dead = True
        
        for b in self.body:
            if self.pos == b:
                self.dead = True

        if self.pos == self.food.pos:
            self.growCount += 4
            self.food = self.newFood()


    def updateFaceControls(self):
        worked, frame = self.video_capture.read()
        cv2.line(frame, (0,0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 1)
        cv2.line(frame, (frame.shape[1],0), (0, frame.shape[0]), (0, 0, 255), 1)

    
        if worked == False:
            print("Error fetching next video frame")
            return

        grayImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        hits = self.cascade.detectMultiScale(grayImage, scaleFactor=1.3, minNeighbors=5, minSize=(10,10))

        if len(hits) < 1:
            frame = cv2.flip(frame, 1)
            cv2.namedWindow("Result")
            cv2.moveWindow("Result", 1000, 0)
            cv2.imshow("Result", frame)
            return
        
        havg = 0
        hi = 0
        for i, (x, y, w, h) in enumerate(hits):
            avg = w + h
            if avg > havg:
                havg = avg
                hi = i

        x, y, w, h = hits[hi]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        mx, my = int(x+w/2), int(y+h/2)
        imx, imy = frame.shape[1]/2, frame.shape[0]/2

        cv2.line(frame, (mx, my), (mx, my), (255, 0, 0), 5)

        frame = cv2.flip(frame, 1)
        cv2.namedWindow("Result")
        cv2.moveWindow("Result", 1000, 0)
        cv2.imshow("Result", frame)


        

        u = (imy-my)/imy
        d = (my-imy)/imy
        r = (imx-mx)/imx
        l = (mx-imx)/imx

        val = max(u, d, l, r)
        if u == val:
            self.up()
        elif d == val:
            self.down()
        elif r == val:
            self.right()
        elif l == val:
            self.left()
        
    def up(self):
        print("u")
        if self.vel != (0, 1):
            self.nvel = (0,-1)

    def down(self):
        print("d")
        if self.vel != (0, -1):
            self.nvel = (0, 1)

    def left(self):
        print("l")
        if self.vel != (1, 0):
            self.nvel = (-1, 0)

    def right(self):
        print("r")
        if self.vel != (-1, 0):
            self.nvel = (1, 0)
