#import libraries

import numpy as  np 
import  cv2
import time 

cap = cv2.VideoCapture(0)    #can also give address of video ; right now just using webcam 0 since only 1 webcam active right now 
time.sleep(3)  #give time for camera to adjust to enviornment 

background = 0 

# capturing the background 
for i in range(30):
    ret , background = cap.read()       # cap.read() returns 2 things image that is captured and return value true if works

while(cap.isOpened()):
    ret , img = cap.read()
    
    if not ret:
        break  
    
    hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV) #converting bgr(default in which webcam captures)image  to hsv format 
    
    #HSB values
    lower_red = np.array([0, 50, 30])  #[0,120,70]
    upper_red = np.array([33, 255, 255]) #[10,255,255]

    mask1 = cv2.inRange(hsv,lower_red,upper_red) #Seperating the cloak part 

    #saturation is darkness of color 
    # lower_red = np.array([160,120,70]) 
    # upper_red = np.array([170,255,255]) 
    mask2  = cv2.inRange(hsv,lower_red,upper_red)

    mask1 = mask1+ mask2  #overloading the + operator to bitwise OR finally got the segmented color we wanted

    mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,
                            np.ones((3,3) , np.uint8),iterations=3)   #Noise removal 
    mask1 = cv2.morphologyEx(mask1 , cv2.MORPH_DILATE,            
                            np.ones((3,3), np.uint8), iterations=3)   #smoothning
    
    mask2 = cv2.bitwise_not(mask1)             #except  the cloak  ; opposite of mask1

    res1 = cv2.bitwise_and(background,background , mask=mask1)  #used for  segmentation of color
    res2 = cv2.bitwise_and(img,img,mask=mask2)      #used to subsitute the cloak 
    final_output = cv2.addWeighted(res1,1,res2,1,0)

    cv2.imshow("Invisble cloak !!",final_output)

    k = cv2.waitKey(10)                               #press esc to exit 
    if k == 27:
        break 

#destructing video capture object 
cap.release()
cv2.destroyAllWindows()