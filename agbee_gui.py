#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, time
from pygame.locals import *
import sys
 
class AgbeeGUI:
    def __init__(self):
        SCREEN_SIZE = (1440, 900)
 
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN)
        pygame.display.set_caption("Agbee GUI")	#windowタイトル
        self.font1 = pygame.font.SysFont("takaogothic", 80)	#フォント設定

    def fill(self):
        self.screen.fill((240,240,240))	#単色塗りつぶし

    def draw_text(self): 
        text1 = self.font1.render("Press Q key to quit.", True, (0,0,0))
        self.screen.blit(text1, (20,50))

        text2 = self.font1.render(u"日本語の表示", True, (0,100,0))
        self.screen.blit(text2, (20,150))

        self.weight = 123.4
        weight_t = self.font1.render(str(self.weight) + " Kg", True, (0,0,0))
        self.screen.blit(weight_t, (20,250))

if __name__ == "__main__":
    AG = AgbeeGUI()

    while True:
        AG.fill()
        AG.draw_text()
        pygame.display.update()		#画面更新
    
        time.sleep(1)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
                sys.exit()
