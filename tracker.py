import cv2
import math

p1= 525
p2= 300

xs= []
ys= []

video= cv2.VideoCapture("footvolleyball.mp4")

tracker= cv2.TrackerCSRT_create()
ret, img= video.read()

bbox= cv2.selectROI("tracking", img, False)
tracker.init(img, bbox)
print(bbox)

def drawBox(img, bbox):
    x,y,w,h= int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y),((x+w),(y+h)), (255,0,0), 3, 1)
    cv2.putText(img, "tracking", (80,90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)

def goalTrack(img, bbox):
        x,y,w,h= int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        c1= x+int(w/2)
        c2= y+int(h/2)
        cv2.circle(img, (c1, c2), 2, (0,0, 255), 5 )
        cv2.circle(img, (int(p1), int(p2)), 2, (0,0, 255), 5 )
        dist = math.sqrt(((c1-p1)**2) + (c2-p2)**2) 
        print(dist)
        # Goal is reached if distance is less than 20 pixel points 
        if(dist<=20): 
            cv2.putText(img,"Goal",(300,90),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        
        xs.append(c1)
        ys.append(c2)

        for i in range(len(xs)-1):
            cv2.circle(img, (xs[i], ys[i]), 2, (0,255,0), 5)

while(True):
    check, img= video.read()

    success, bbox= tracker.update(img)

    if success:
        drawBox(img, bbox)
    else:
        cv2.putText(img, "lost", (80,90), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 2)
    
    goalTrack(img, bbox)


    cv2.imshow("output", img)
    key= cv2.waitKey(25)
    if(key==ord('q')):
        print("stopped") 
        break


video.release()
cv2.destroyAllWindows()
