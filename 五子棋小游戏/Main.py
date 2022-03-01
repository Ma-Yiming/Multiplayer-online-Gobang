# ==============================================================================
#
#         项目:  五子棋  
#         版本:  2.5
#         日期:  2021//1/16
#         作者:  马艺鸣
#         功能:  双人对战
#
# ==============================================================================

import pygame
from pygame.locals import *
from Text import *
from Map import *
from Game import *
from Mytk import *
import sys
import time
import os


game=Game()
#悔棋的上下左右对应范围
Back_L = 790
Back_R = 890
Back_U = 369
Back_D = 431

running=True
#控制事件
while running:
    for event in pygame.event.get():
        mouse_x,mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.clickwhere() == 0:
                running = False
            if Back_L < mouse_x and mouse_x < Back_R \
                   and Back_U < mouse_y and mouse_y < Back_D\
                   and game.Play == 1 and len(game.map1.steps)>0:
                game.Back()
            
pygame.quit()
sys.exit()
