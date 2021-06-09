import numpy as np
import cv2
import time
import win32api,win32con

scroll=0
x=0
y=0
y1=0
y2=0
flagg=0
flagr=0
areab=0
x1=0

def move(x,y):
    nx = x*65535/win32api.GetSystemMetrics(0)
    ny = y*65535/win32api.GetSystemMetrics(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE|win32con.MOUSEEVENTF_MOVE,nx,ny)
def leftclick(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
def rightclick(x,y):
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
cap=cv2.VideoCapture(0)
cap.set(3,276)
cap.set(4,156)
#cap.set(6,60)
while True:
    arear=0
    areag=0
    _,frame=cap.read()
    # _,frame=cap.read()
    # _,frame=cap.read()
    
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    low_blue=np.array([100,100,100])
    high_blue=np.array([120,255,255])
    low_green=np.array([56,50,50])
    high_green=np.array([75,255,255])
    low_red=np.array([168,100,100])
    high_red=np.array([188,255,255])
    maskg=cv2.inRange(hsv,low_green,high_green)
    maskr=cv2.inRange(hsv,low_red,high_red)
    cv2.imshow('maskr',maskr)
    
    maskb=cv2.inRange(hsv,low_blue,high_blue)
    blurb=cv2.bilateralFilter(maskb,15,75,75)
    blurg=cv2.bilateralFilter(maskg,15,75,75)
    blurr=cv2.bilateralFilter(maskr,15,75,75)

    cv2.imshow('camera',frame)
    kernel = np.ones((5,5),np.uint8)
    erosionb = cv2.erode(blurb, kernel,iterations = 1)
    erosiong = cv2.erode(blurg, kernel,iterations = 1)
    erosionr = cv2.erode(blurr, kernel,iterations = 1)
 
    imageb,contoursb, hierarchy = cv2.findContours(erosionb,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    imgb=cv2.drawContours(blurb,contoursb,-1,(128,255,0),3)
    imageg,contoursg, hierarchy = cv2.findContours(erosiong,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    imgg=cv2.drawContours(blurg,contoursg,-1,(128,255,0),3)
    imager,contoursr, hierarchy = cv2.findContours(erosionr,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    imgr=cv2.drawContours(blurr,contoursr,-1,(128,255,0),3)
    max_areab = -1
    
    #cv2.imshow('b',imgb)
    #cv2.imshow('g',imgg)
    #cv2.imshow('r',imgr) 
        
    for i in range(len(contoursb)):
        cntb=contoursb[i]
        areab = cv2.contourArea(cntb)
        if(areab>max_areab):
            max_areab=areab
            ci=i
    centroid_x=0
    centroid_y=0
    try:
        cntb=contoursb[ci]

        M=cv2.moments(cntb)
        centroid_x=int(M['m10']/M['m00'])
        centroid_y=int(M['m01']/M['m00'])
        centre=cv2.circle(blurb,(centroid_x,centroid_y),10,(0,255,0),1)
        #cv2.imshow('blue',imgb)
        centroid_x=276-centroid_x        
        if(centroid_x>=x+3 or centroid_x<=x-3 or centroid_y>=y+3 or centroid_y<=y-3) :
            move(centroid_x*8,centroid_y*8)
            x=centroid_x
            y=centroid_y
            scroll+=1
            if scroll>30 and areag==0 and arear==0:
              if (centroid_x!=x1 and centroid_y!=y1 and (centroid_x>=x1+15 or centroid_x<=x1-15 or centroid_y>=y1+15 or centroid_y<=y1-15)):  
               if (centroid_y>y1+30 and (centroid_x>x1-3 or centroid_x<x1+3)):
                win32api.mouse_event(0x0800, centroid_x, centroid_y,2000,0)
                print 'scrollup'
                
                
               elif (centroid_y<y1-30 and (centroid_x>x1-3 or centroid_x<x1+3)):
                win32api.mouse_event(0x0800, centroid_x, centroid_y,-2000,0)
                print 'scrolldown'
            x1=centroid_x
            y1=centroid_y      
    except Exception as e:
        pass
    
    
    
    for i in range(len(contoursr)):
        cntr=contoursr[i]
        arear = cv2.contourArea(cntr)
        if(arear>1):
            if flagr==0:
                rightclick(centroid_x*8,centroid_y*8)
                #cv2.imshow('r',imgr)
                print('rightclick')
                flagr=1
                break
    if arear<1:
        flagr=0
    for i in range(len(contoursg)):
        cntg=contoursg[i]
        areag = cv2.contourArea(cntg)
        if(areag>25 and areab!=0):
            
           
            
               if flagg==0:
                 leftclick(centroid_x*8,centroid_y*8)
                 print"left click"
                 flagg=1
                 break
    
    if areag<10:
         flagg=0                 
    
    k=cv2.waitKey(1)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
