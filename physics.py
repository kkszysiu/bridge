#!/usr/bin/python
"""
This file is part of the 'Physics' Project
Physics is a 2D Physics Playground for Kids (supporting Box2D2)
Physics Copyright (C) 2008, Alex Levenson, Brian Jordan
Elements Copyright (C) 2008, The Elements Team, <elements@linuxuser.at>

Wiki:   http://wiki.laptop.org/wiki/Physics
IRC:    #olpc-physics on irc.freenode.org

Code:   http://dev.laptop.org/git?p=activities/physics
        git clone git://dev.laptop.org/activities/physics

License:  GPLv3 http://gplv3.fsf.org/
"""

import sys
import math
import pygame
from pygame.locals import *
from pygame.color import *
import olpcgames
import elements
from elements import Elements
import tools
from bridge import Bridge
from helpers import *
from gettext import gettext as _

class PhysicsGame:
    def __init__(self,screen):
        self.screen = screen
        # get everything set up
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18) # font object
        #self.canvas = olpcgames.canvas
        self.joystickobject = None 
        self.debug = True

        # create the name --> instance map for components
        self.toolList = {}
        for c in tools.allTools:
             self.toolList[c.name] = c(self)
        self.currentTool = self.toolList[tools.allTools[0].name]
        
        # set up the world (instance of Elements)
        self.world = elements.Elements(self.screen.get_size())
        self.world.renderer.set_surface(self.screen)
        
        # set up static environment
        #self.world.add.ground()
        self.world.run_physics = False

        self.bridge = Bridge(self)
        self.bridge.create_world()
        
    def run(self):
        self.running = True
        t = pygame.time.get_ticks()
        while self.running:
            if (pygame.time.get_ticks() - t) > 1500:
#                bridge.create_train(self)
                t = pygame.time.get_ticks()
                
            for event in pygame.event.get():
                self.currentTool.handleEvents(event)
            # Clear Display
            self.screen.fill((80,160,240)) #255 for white

            # Update & Draw World
            self.world.update()
            self.world.draw()
            if self.world.run_physics:
                self.bridge.for_each_frame()

            #draw toolbar for tools
            tb_x = 0
            for c in tools.allTools:
                tb_icon_name = c.name+'_icon'
                tb_icon_name = pygame.image.load("activity-bridge.png").convert_alpha()
                self.screen.blit(tb_icon_name, (tb_x, 0))
                #print tb_icon.get_rect()
                tb_x = tb_x+50

            event = pygame.event.poll()
            keyinput = pygame.key.get_pressed()

            if keyinput[pygame.K_ESCAPE]:
                raise SystemExit
            elif event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print 'mouse pressed'
#                for c in tools.allTools:
#                    tb_icon_name = c.name+'_icon'
#
#                    print tb_icon_name
#                    srect = tb_icon_name.get_rect()
#                    print srect.collidepoint(event.pos)
            
            # draw output from tools
            self.currentTool.draw()

            #Print all the text on the screen
            text = self.font.render(_("Total Cost: %d") % self.bridge.cost, True, (0,0,0))
            textpos = text.get_rect(top=57)
            self.screen.blit(text,textpos)
            ratio = self.bridge.stress*100/self.bridge.capacity
            text = self.font.render(_("Stress: %d%%") % ratio, True, (0,0,0))
            textpos = text.get_rect(top=75)
            self.screen.blit(text,textpos)

            if self.bridge.train_off_screen:
                text = self.font.render(_("Train fell off the screen, press R to try again!"), True, (0,0,0))
            elif self.bridge.level_completed:
                text = self.font.render(_("Level completed, well done!!  Press T to send another train."), True, (0,0,0))
            else:
                text = self.font.render(_("Press the Spacebar to start/pause."), True, (0,0,0))
            textpos = text.get_rect(top=93)
            self.screen.blit(text,textpos)

            # Flip Display
            pygame.display.flip()  
            
            # Try to stay at 30 FPS
            self.clock.tick(30) # originally 50    

    def setTool(self,tool):
        self.currentTool.cancel()
        self.currentTool = self.toolList[tool] 

def main():
    toolbarheight = 75
    tabheight = 45
    pygame.init()
    pygame.display.init()
    x,y  = pygame.display.list_modes()[0]
    screen = pygame.display.set_mode((x,y-toolbarheight-tabheight))
    # create an instance of the game
    game = PhysicsGame(screen) 
    # start the main loop
    game.run()

# make sure that main get's called
if __name__ == '__main__':
    main()

