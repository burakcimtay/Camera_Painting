import cv2
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,1600)
cap.set(4,900)
cap.set(10,100)

imageFolder="images"
overlay=[]
overlayImage=cv2.imread('images/header.png')
#overlayImage=cv2.resize(overlayImage,(1280,100))
overlay.append(overlayImage)

colors=[[36,93,92,72,255,255],[92,127,89,159,255,255],[135,172,121,179,255,255],[3,99,247,28,255,255]]       #yesil, mavi, mor, turuncu

colorValues=[[0,255,0],[255,0,0],[255,0,255],[0,127,255]]       #renk kodlari

points=[] #[x, y, color]

def findcolor(img, colors, colorValues):                                   #kalem rengini bulma
    img_HSV=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    colorNum=0
    newPoints=[]
    for i in colors:
        lower=np.array(i[0:3])
        upper=np.array(i[3:6])
        final_mask=cv2.inRange(img_HSV, lower, upper)
        x,y=getContours(final_mask)
        cv2.circle(imgResult, (x,y), 16, colorValues[colorNum], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,colorNum])
        colorNum=colorNum+1

    return newPoints
        
def getContours(img):                                                                          #kalemin etrafını bulma
    contours, hierarchy=cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            prm=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt, 0.2*prm, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y
    
def drawPoints(points, colorValues):                                                           #kameraya resim cizme
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]), 16, colorValues[point[2]], cv2.FILLED)

status = "3"
while True:
    success, img=cap.read()
    img = cv2.flip(img,1)
    imgResult=img.copy()
    
    if cv2.waitKey(1) & 0xFF==ord('w'):
        status="1"
        
    elif cv2.waitKey(1) & 0xFF==ord('e'):
        status="2"
        points.clear()
        
    elif cv2.waitKey(1) & 0xFF==ord('s'):
        status="3"
        
    elif cv2.waitKey(1) & 0xFF==ord('q'):
        break
        
    if status =="1":
        newPoints= findcolor(img, colors, colorValues)
        if len(newPoints)!=0:
            for nP in newPoints:
                points.append(nP)
            
        if len(points)!=0:
            drawPoints(points, colorValues)
            
    elif status=="3":
        drawPoints(points, colorValues)
        
    if cv2.waitKey(1) & 0xFF==ord('d'):
        cv2.imwrite('paint.jpg', imgResult)
        
    cv2.putText(imgResult,'Burak Cimtay 180208026',(830,125), cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,255),1)
    imgResult[0:100, 0:1600]=overlay[0]
    cv2.imshow("Painting", imgResult)
    