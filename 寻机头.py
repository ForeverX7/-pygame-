# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 13:42:56 2021

@author: 小七
"""

import pygame
import random
import sys
from pygame.locals import *

#设置最大递归深度
sys.setrecursionlimit(10000)

#相关颜色RGB三元组表示
WHITE=(255,255,255)#白色
BLACK=(0,0,0)#黑色
RED=(255,0,0)#红色
BLUE=(0,0,255)#蓝色
YELLOW=(255,255,0)#黄色
PURPLE=(160,32,240)#紫色
#提示字体颜色
TEXTCOLOR=WHITE
#结果字体颜色
JGCOLOR=PURPLE
#边界颜色
BJCOLOR=YELLOW
#背景颜色
BGCOLOR=BLACK
#空白区域颜色
KBCOLOR=WHITE
#机身颜色
JSCOLOR=BLUE
#机头颜色
JTCOLOR=RED
#形状1的模板
SHAPE1=[['..1..',
         '..0..',
         '00000',
         '..0..',
         '.000.'],
        ['.000.', 
         '..0..',
         '00000',
         '..0..',
         '..1..'],
        ['..0..',
         '..0.0',
         '10000',
         '..0.0',
         '..0..'],
        ['..0..', 
         '0.0..',
         '00001',
         '0.0..',
         '..0..']]
#形状2的模板 
SHAPE2=[['..1..',
         '.000.',
         '0.0.0',
         '..0..',
         '.000.'],
        ['.000.',
         '..0..',
         '0.0.0',
         '.000.',
         '..1..'],
        ['..0..',
         '.0..0',
         '10000',
         '.0..0',
         '..0..'],
        ['..0..',
         '0..0.',
         '00001',
         '0..0.',
         '..0..']]

#PIECES储存所有不同的模板。每个模板都拥有一个形状所有可能的旋转。
PIECES={
        '1':SHAPE1,
        '2':SHAPE2,
       }

def main():
     
    pygame.init()
    #创建窗口  
    screen=pygame.display.set_mode((10*85,10*30))
    #字体
    FONT1=pygame.font.SysFont('华文琥珀',50)
    FONT2=pygame.font.SysFont('华文行楷',30)
    FONT3=pygame.font.SysFont('华文行楷',20)
    #设置窗口标题  
    pygame.display.set_caption('寻机头')
    
    #画格子和边界
    screen.fill(BGCOLOR)
    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen,BJCOLOR,[i*30,j*30,29,29],1)
            
    pygame.draw.line(screen,BJCOLOR,(10*35,0),(10*35,10*30),3)
    pygame.display.flip()            
        
    #给出本局机型
    textsurface=FONT2.render(u'本局机型：',True,TEXTCOLOR)
    screen.blit(textsurface,(360,10))
    for i in range(5):
        for j in range(5):
            if PIECES['1'][2][i][j]=='.':
                pygame.draw.rect(screen,KBCOLOR,[360+i*20,60+j*20,19,19],0)
            elif PIECES['1'][2][i][j]=='0':
                pygame.draw.rect(screen,JSCOLOR,[360+i*20,60+j*20,19,19],0)
            elif PIECES['1'][2][i][j]=='1':
                pygame.draw.rect(screen,JTCOLOR,[360+i*20,60+j*20,19,19],0)
    for i in range(5):
        for j in range(5):
            if PIECES['2'][2][i][j]=='.':
                pygame.draw.rect(screen,KBCOLOR,[500+i*20,60+j*20,19,19],0)
            elif PIECES['2'][2][i][j]=='0':
                pygame.draw.rect(screen,JSCOLOR,[500+i*20,60+j*20,19,19],0)
            elif PIECES['2'][2][i][j]=='1':
                pygame.draw.rect(screen,JTCOLOR,[500+i*20,60+j*20,19,19],0)
    pygame.display.update()       
    
    #给出文字提示
    textsurface=FONT3.render(u'请在规定步数内从左侧棋盘中翻出两个飞机的机头',True,TEXTCOLOR)
    screen.blit(textsurface,(360,200))
    pygame.display.update()   
    
    #设置用来存放正确答案的答案板和一个与之相同的二维数组用于记录该格子是否被点击过
    GZ1=[[0]*10 for i in range(10)]
    flag=[[0]*10 for i in range(10)]
    
    #f飞机1随机旋转并随机放置
    s='1'
    new_piece(s, GZ1)
    
    #飞机2随机旋转并随机放置且不与1重叠
    s='2'
    new_piece(s,GZ1)
    
    num=0
    jt_num=0
    
    #显示剩余步数
    textsurface=FONT3.render(u'剩余步数：',True,TEXTCOLOR)
    screen.blit(textsurface,(360,250))
    textsurface=FONT3.render(str(15-num),True,TEXTCOLOR)
    screen.blit(textsurface,(470,250))
    pygame.display.update()
        
    #主循环
    while True:
        
        #退出事件
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            
        #点击鼠标事件
            elif event.type==MOUSEBUTTONDOWN:
                if event.button==1:
                    #获取鼠标点击时的坐标，并映射到数组的x,y
                    x,y=event.pos[0]//30,event.pos[1]//30
                    #点击区域为为点击过的空白格
                    if GZ1[x][y]==0 and flag[x][y]!=1:
                        if(num<15 and jt_num<2):
                            num+=1
                            #标记该格为已点击
                            flag[x][y]=1
                            draw_kb(screen,x,y)
                            #动态显示剩余步数
                            pygame.draw.rect(screen, BGCOLOR,[470,250,20,20],0)
                            textsurface=FONT3.render(str(15-num),True,TEXTCOLOR)
                            screen.blit(textsurface,(470,250))
                            pygame.display.update() 
                    #点击区域为为点击过的机身
                    if GZ1[x][y]==1 and flag[x][y]!=1:
                        if(num<15 and jt_num<2):
                            num+=1
                            #标记该格为已点击
                            flag[x][y]=1
                            draw_js(screen,x,y)
                            #动态显示剩余步数
                            pygame.draw.rect(screen, BGCOLOR,[470,250,20,20],0)
                            textsurface=FONT3.render(str(15-num),True,TEXTCOLOR)
                            screen.blit(textsurface,(470,250))
                            pygame.display.update() 
                    #点击区域为为点击过的机头
                    if GZ1[x][y]==2 and flag[x][y]!=1:
                        if(num<15 and jt_num<2):
                            num+=1
                            #标记该格为已点击
                            flag[x][y]=1
                            draw_jt(screen,x,y)
                            #动态显示剩余步数
                            pygame.draw.rect(screen, BGCOLOR,[470,250,20,20],0)
                            textsurface=FONT3.render(str(15-num),True,TEXTCOLOR)
                            screen.blit(textsurface,(470,250))
                            pygame.display.update() 
                            jt_num+=1
                    
                    if jt_num==2 and num<=15:
                        textsurface=FONT1.render(u'胜利',True,JGCOLOR)
                        screen.blit(textsurface,(100,125))
                        pygame.display.update()
                        
                    if jt_num<2 and num==15:
                        textsurface=FONT1.render(u'失败',True,JGCOLOR)
                        screen.blit(textsurface,(100,125))
                        pygame.display.update()
   
                            
#翻开空白格
def draw_kb(screen,i,j):
    pygame.draw.rect(screen,KBCOLOR,[i*30,j*30,29,29],0)
    pygame.display.flip()

#翻开机头    
def draw_jt(screen,i,j):
    pygame.draw.rect(screen,JTCOLOR,[i*30,j*30,29,29],0)
    pygame.display.flip()

#翻开机身
def draw_js(screen,i,j):
    pygame.draw.rect(screen,JSCOLOR,[i*30,j*30,29,29],0)
    pygame.display.flip()

#随机生成并放置飞机
def new_piece(s,GZ):
    shape=s
    newPiece={#shape：随机形状
              'shape':shape,
              #rotation：随机旋转
              'rotation':random.randint(0,len(PIECES[shape])-1),
              #'x'代表5×5模板左上角方格的横坐标。
              'x':random.randint(0,5),
              #'y'代表5×5模板左上角方格的纵坐标。
              'y':random.randint(0,5),
              }
    
    #将随机生成的飞机形状转换成二维数组插入到随机生成的相应位置
    a=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    m=0
    
    nps=newPiece['shape']
    npr=newPiece['rotation']
    npx=newPiece['x']
    npy=newPiece['y']
    for i in range(5):
        for j in range(5):
            if PIECES[nps][npr][i][j]=='.':
                a[m]=0
                m+=1
            elif PIECES[nps][npr][i][j]=='0':
                a[m]=1
                m+=1
            elif PIECES[nps][npr][i][j]=='1':
                a[m]=2
                m+=1
                
    m=0
    flag=1
    break_flag=1
    b=[-1]*25
    for x in range(npx,npx+5):
        for y in range(npy,npy+5):
            
            #飞机的机身或机头有重叠
            if a[m]!=0 and GZ[x][y]!=0:
                #递归标志置零
                flag=0
                #下一层循环判定置零(连续跳出双层循环)
                break_flag=0
                #跳出for(y)循环
                
                
            #所放飞机的空白区域处有之前放置的飞机机身或机头    
            elif a[m]==0 and GZ[x][y]!=0:
                #将位置记录下来
                b.append(m)
                m+=1
                if m==25:
                    #下一层循环判定置零(连续跳出双层循环)
                    break_flag=0
                    #跳出for(y)循环
                    break
                
            #无重叠    
            else:
                m+=1
                if m==25:
                    #下一层循环判定置零(连续跳出双层循环)
                    break_flag=0
                    #跳出for(y)循环
                    break
                
        #跳出for(x)循环           
        if break_flag==0:
            break
         
    #递归标志为零时进行递归，重新生成飞机形状和放置点                
    if flag==0:
        new_piece(s,GZ)
    #递归标志为初始值1时进行赋值，将飞机放入
    elif flag==1:
         m=0
         for x in range(npx,npx+5):
             for y in range(npy,npy+5):
                 if m not in b:
                     #不是标记位置，即放置飞机时空白区域不会对之前的飞机机身或机头造成覆盖时，将一维数组的值赋给二维数组指定区域
                     GZ[x][y]=a[m]
                     m+=1
                 else:
                     #位于标记位置，即放置飞机时空白区域会覆盖之前的飞机机身或机头，则不将空白格子的值赋给之前的格子，而是进入下一个格子的判断
                     m+=1
                   
    return GZ

    pygame.display.update()


    
if __name__=='__main__':
    main()