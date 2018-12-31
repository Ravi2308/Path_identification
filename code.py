#PROJECT TITLE:- PATH IDENTIFIACTION FOR INDOOR MOVEMENT

# IMPORTING PACAKGES

import cv2
import numpy as np
from scipy.ndimage.measurements import label
from skimage.measure import regionprops

#COMMAND TO CAPTURE THE VIDEO

video= cv2.VideoCapture("D:/Inter/new_1.mp4")

while True:
    
    ret,orig_frame= video.read()
    
    col=orig_frame.shape[1]
    row=orig_frame.shape[0]
    
    if not ret:
        video=cv2.VideoCapture("D:/Inter/new_1.mp4")
        continue
#APPLY GAUSSIAN FILTER TO REMOVE THE NOISE
        
    frame= cv2.GaussianBlur(orig_frame,(5,5),0)
    
# CONVERTING THE COLOR TO GRAYSCALE    

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
# FOR EDGE DETECTION APPLY CANNY DETECTOR    

    edges= cv2.Canny(gray,45,45)
    
    #cv2.imshow("Canny",edges)
    
    rows = edges.shape[0]
    cols = edges.shape[1]
    
# APPLY MORPHOLOGICAL OPERATION    
    Structure1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,17))
    vertical = cv2.dilate(edges, Structure1,(-1,-1))
    Structure2 = cv2.getStructuringElement(cv2.MORPH_RECT, (17,9))
    vertical = cv2.erode(vertical, Structure2,(-1,-1))
    kernel=np.ones((8,8),np.uint8)
    closing =cv2.morphologyEx(vertical,cv2.MORPH_CLOSE,kernel)
    
    Structure2=np.ones((2,10),np.uint8)
    vertical = cv2.erode(closing, Structure2,(-1,-1))
    
    #cv2.imshow("image",vertical)
    
#CONVERTING INTO BINARY IMAGE

    ret,thresh1 = cv2.threshold(vertical,100,255,cv2.THRESH_BINARY)
    
    labeled_array, num_features =label(thresh1)
    props=regionprops(labeled_array)
    comp=len(props)
    
# CREATE THE NEW BLACK IMAGE
    
    black=np.zeros((rows,cols),np.float)
    
    #cv2.imshow("black_img",black)
    
    rows2 = black.shape[0]
    cols2 = black.shape[1]

# SELECT AREA
    
    for i in range(1,comp):
        if props[i].area>3501:
            max=props[i].area
            index=i
            var1=props[index].coords
            length = var1.shape[0]
            for i in range(0,(length-1)):
                xcor=var1[i,0]
                ycor=var1[i,1]
                black[xcor,ycor]=1
                
    
    #cv2.imshow("After_area",black)

#FIND THE SLOPE
    
    for i in range(1,comp):
        if props[i].area>3501:
            index=i
            var1=props[index].coords
            length = var1.shape[0]
            l=length-1
            xcor1=var1[i,0]
            ycor1=var1[i,1]
            xcor2=var1[l,0]
            ycor2=var1[l,1]
            slope=(ycor2-ycor1)/(xcor2-xcor1)
            if slope in range(0,1):
                for i in range(xcor1,xcor2):
                    for j in range(ycor1,ycor2):
                        black[i,j]=0
                        


    #cv2.imshow("image",frame)
    #cv2.imshow("After_area_slope",black)
    
    ret1,thresh2 = cv2.threshold(black,0,255,cv2.THRESH_BINARY)

    labeled_array2, num_features =label(thresh2)
    props=regionprops(labeled_array2)
    
    #cv2.imshow("thresh2",thresh2)
    comp=len(props)
    
    black2=np.zeros((rows,cols),np.float)
    
    k=0
    maxx=0
    maxy=0
    minx=10000
    miny=10000
    for i in range(0,comp):
        k=k+1
        
        var2=props[i].coords
        
        length=var2.shape[0]


        for j in range(1,length):
            if var2[j,0]>maxx:
                maxx=var2[j,0]
                maxy=var2[j,1]
            if var2[j,0]<minx:
                minx=var2[j,0]
                miny=var2[j,1]


# MAKING THE POLYGON
                
        if k==2:
            pts = np.array([[1920,1080],[maxy,maxx],[miny,minx],[0,1080]] ,np.int32)
        else:
            pts = np.array([[1920,1080],[miny,minx],[maxy,maxx],[0,1080]], np.int32)
           
        cv2.fillPoly(frame, np.int_([pts]), (0, 0, 255))            
                    
    line= cv2.line(frame,(miny,minx),(maxy,maxx),(255,255,255),5)
        
#    cv2.imshow("image",img)
    cv2.imshow("final",frame)
    
    key=cv2.waitKey(500)
    if key==27:
        break
    
video.release()
cv2.destroyAllWindows()
