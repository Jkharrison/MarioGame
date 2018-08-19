#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import time
import math

from pygame.locals import *
from time import sleep




class Mario:
    def __init__(self, model):
        #Member variables for mario
        self.height = 95
        self.width = 60
        self.x = 10
        self.y = 600 - self.height
        self.image = pygame.image.load("mario1.png")
        self.onTube = False
        self.frameCount = 0
        self.vertVelocity = -10.0
        self.rect = self.image.get_rect()
        self.model = model
        self.frame = 0
        self.prev_x = 0
        self.prev_y = 0

    def update(self):

        #Checks with all the tubes for collisions
        #self.rememberPos()
        if(self.isCollidingWithOne() or self.isCollidingWithTwo()):
            #print("Collision occuring")
            self.getOutOfTube()
        #Incresing the amount of gravity each update call
        self.vertVelocity += 8.2

        self.y += self.vertVelocity

        #Making sure mario does not fall underneath the ground.
        if(self.y + self.height >= 600):
            self.vertVelocity = 0
            self.y = 600 - self.height
            self.frameCount = 0
        else:
            self.frameCount += 1

        #self.frame += 1
        #Iterates through all of the picutres.
        if(self.frame > 4):
            self.frame = 0
        if(self.frame < 0):
            self.frame = 4
        if(self.frame == 0):
            self.image = pygame.image.load("mario1.png")
        if(self.frame == 1):
            self.image = pygame.image.load("mario2.png")
        if(self.frame == 2):
            self.image = pygame.image.load("mario3.png")
        if(self.frame == 3):
            self.image = pygame.image.load("mario4.png")
        if(self.frame == 4):
            self.image = pygame.image.load("mario5.png")



    #Model Setter for when something is added to the model, i.e Fireball, Tube, Gumba.
    def setModel(self, model):
        self.model = model


    def jump(self):
        #print("Finding thyself")
        self.vertVelocity -= 20
        '''

        if(self.onTube or self.y == (600 - self.height)):
            self.vertVelocity -= 20
        else:
            print("Cannot jump because not on the ground or tube")
        '''
        #This is called each time the update methods runs through.
    def rememberPos(self):
        self.prev_x = self.x
        self.prev_y = self.y

    def isCollidingWithOne(self):

        t = self.model.tube1
        if(self.x + self.width < t.x):
            return False
        if(self.x > t.x + t.width):
            return False
        if(self.y + self.height < t.y):
            return False
        if(self.y > t.y + t.height):
            return False
        return True

    def isCollidingWithTwo(self):
        t = self.model.tube2
        if(self.x + self.width < t.x):
            return False
        if(self.x > t.x + t.width):
            return False
        if(self.y + self.height < t.y):
            return False
        if(self.y > t.y + t.height):
            return False
        return True

        #Actions to get out of tube.
    def getOutOfTube(self):
        tubes = []
        tubes.append(self.model.tube1)
        tubes.append(self.model.tube2)
        #print("length of tubes in get out method: " + str(len(tubes)))
        for i in range(len(tubes)):

            if(self.x + self.width > tubes[i].x  and self.x + self.width < tubes[i].x + tubes[i].width and self.prev_x < tubes[i].x):
                    #Left side of tube
                self.x = tubes[i].x - self.width - 1
                self.y = self.y
                self.onTube = False
            elif(self.x <= tubes[i].x + tubes[i].width and self.x + self.width >= tubes[i].x and self.prev_x > tubes[i].x):
                #Right side of tube
                self.x = tubes[i].x + 1
                self.onTube = False
            elif(self.y + self.height > tubes[i].y and self.x  <= tubes[i].x + tubes[i].width and self.y + self.height <= tubes[i].x
            + tubes[i].height and self.prev_y < tubes[i].y):
                    #Above the tube
                self.frameCount = 0
                self.onTube = True
                self.vertVelocity = 0
                keys = pygame.key.get_pressed()
                if(keys[K_SPACE]):
                    print('should be jumping')
                    self.jump()
                self.y = tubes[i].y - self.height - 1

class Gumba:
    def __init__(self, x, y, model):
        self.height = 118
        self.width = 99
        self.x = x
        self.y = y - self.height
        self.image = pygame.image.load("gumba.png")
        self.onFire = False
        self.rect = self.image.get_rect()
        self.model = model
        self.runRight = True
        self.frame = 0
    def update(self):
        #print("Gumba boolean is: " + str(self.runRight))
        if(self.runRight == True):
            self.x += 5
        elif(self.runRight == False):
            self.x -= 5
        if(self.isColliding()):
            #print("Collision happening")
            if(self.runRight == True):
                self.runRight == False
            elif(self.runRight == False):
                self.runRight == True
            #Some local variables definied to reduce amount of code per line.
        operation = self.x - self.model.tube1.x
        operation1 = self.x - self.model.tube2.x
        difference = math.fabs(operation)
        difference1 = math.fabs(operation1)
        #if(self.x + self.width == self.model.tube2.x or self.x - self.width == self.model.tube1.x):
        if(difference < self.width - self.model.tube1.width or difference1 < self.width):
            #print("Collision here")
            if(self.runRight == True):
                #print("This should be happening")
                self.runRight = False
            elif(self.runRight == False):
                self.runRight = True
        if(self.isCollidingWithFire()):
            self.image = pygame.image.load("gumba_fire.png")
            self.onFire = True
        if(self.onFire == True):
            self.frame += 1
    def setModel(self, model):
        self.model = model

    def isColliding(self):
        if(self.x + self.width < self.model.tube1.x):
            return False
        if(self.x > self.model.tube1.x + self.model.tube1.width):
            return False
        if(self.x + self.width < self.model.tube2.x):
            return False
        if(self.x > self.model.tube2.x + self.model.tube2.width):
            return False
        return True
    def isCollidingWithFire(self):
        for i in range(len(self.model.fireballs)):
            fireball = self.model.fireballs[i]
            if(self.x + self.width < fireball.x):
                return False
            if(self.x > fireball.x + self.model.fireballs[i].width):
                return False
            if(self.y + self.height < fireball.y):
                return False
            if(self.y > fireball.y + self.model.fireballs[i].height):
                return False
            return True

class Tube:
    def __init__(self, x, y):
        self.height = 400
        self.width = 55
        self.x = x
        self.y = y - self.height
        self.image = pygame.image.load("tube.png")
        self.rect = self.image.get_rect()

class Fireball:
    def __init__(self, x, y):
        self.height = 47
        self.width = 47
        self.x = x
        self.y = y - self.height
        self.image = pygame.image.load("fireball.png")
        self.rect = self.image.get_rect()
        self.vertVelocity = -12.0
        self.remove = False
    def update(self):
        self.vertVelocity += 2.2
        self.y += self.vertVelocity
        self.x += 5
        if(self.y > (600 - self.height)):
            self.y = 600 - self.height
            self.vertVelocity = -20.0
        if(self.x > 1000):
            self.remove = True


class Model:
    def __init__(self):
        self.dest_x = 0
        self.dest_y = 0
        self.mario = Mario(self)
        self.gumba = Gumba(400, 600, self)
        self.tube1 = Tube(200, 800)
        self.tube2 = Tube(600, 800)
        self.mario.setModel(self)
        self.gumba.setModel(self)
        self.fireballs = []
        #self.fireballs.append(Fireball(300, 200)) This was a test fireball
        self.fireballImage = pygame.image.load("fireball.png")

    def update(self):
        #print("Updating Model")
        self.mario.update()
        self.gumba.update()
        for i in range(len(self.fireballs)):
            self.fireballs[i].update()

    def set_dest(self, pos):
        self.dest_x = pos[0]
        self.dest_y = pos[1]


class View:

    def __init__(self, model):
        screen_size = (1200, 600)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.model = model

    def update(self):
        self.screen.fill([240, 128, 128])
        self.screen.blit(self.model.mario.image, self.model.mario.rect.move(self.model.mario.x, self.model.mario.y))
        if(self.model.gumba.frame < 20):
            #Only Draw the Gumba if he has not been on fire for more than 20 frames or not on fire at all.
            self.screen.blit(self.model.gumba.image, self.model.gumba.rect.move(self.model.gumba.x, self.model.gumba.y))
        self.screen.blit(self.model.tube1.image, self.model.tube1.rect.move(self.model.tube1.x, self.model.tube1.y))
        self.screen.blit(self.model.tube2.image, self.model.tube2.rect.move(self.model.tube2.x, self.model.tube2.y))
        for i in range(len(self.model.fireballs)):
            if(self.model.fireballs[i].remove == False):
                self.screen.blit(self.model.fireballImage, self.model.fireballs[i].rect.move(self.model.fireballs[i].x, self.model.fireballs[i].y))

        pygame.display.flip()

#Logic for the input from the user. 
class Controller:

    def __init__(self, model):
        self.model = model
        self.keep_going = True

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.model.set_dest(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.model.mario.frame -= 1
            self.model.mario.x -= 5
        if keys[K_RIGHT]:
            self.model.mario.frame += 1
            self.model.mario.x += 5
        if keys[K_SPACE]:
            if(self.model.mario.frameCount < 5):
                self.model.mario.jump()

        if keys[K_LCTRL or K_RCTRL]:
            self.model.fireballs.append(Fireball(self.model.mario.x + 2, self.model.mario.y + (self.model.mario.height / 2)))
            self.model.mario.setModel(self.model)
            self.model.gumba.setModel(self.model)


print ('Use the arrow keys to move. Press Esc to quit.')
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.01)
print ('Goodbye')
