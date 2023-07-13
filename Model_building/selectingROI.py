import cv2
import pickle
 
def selecting_ROI(a):
    

    if a==1:
        width,height=107,48
    elif a==0:
        width,height=140,72
    elif a==3:
        width,height=45,21
    width1,height1=65,155
    try:
        if a == 1:
        
            with open('ParkingSlotPosition', 'rb') as f:
                posList = pickle.load(f)
        elif a ==0:
            with open('ParkingSlotPosition2','rb')as g:
                posList2 = pickle.load(g)
        elif a ==3:
            with open('ParkingSlotPosition3','rb')as h:
                posList3 = pickle.load(h)
    except:
        posList = []
        posList2=[]
        posList3=[]
 
    def mouseClick(events, x, y, flags, params):
        if a == 1:

            if events == cv2.EVENT_LBUTTONDOWN:
                posList.append((x, y))
            if events == cv2.EVENT_RBUTTONDOWN:
                for i, pos in enumerate(posList):
                    x1, y1 = pos
                    if x1 < x < x1 + width and y1 < y < y1 + height:
                        posList.pop(i)
 
            with open('ParkingSlotPosition', 'wb') as f:
                pickle.dump(posList, f)
        if a==0:
            if events == cv2.EVENT_LBUTTONDOWN:
                posList2.append((x, y))
            if events == cv2.EVENT_RBUTTONDOWN:
                for i, pos in enumerate(posList2):
                    x1, y1 = pos
                    if x1 < x < x1 + width and y1 < y < y1 + height:
                        posList2.pop(i)
 
            with open('ParkingSlotPosition2', 'wb') as g:
                pickle.dump(posList2, g)
        if a == 3:

            if events == cv2.EVENT_LBUTTONDOWN:
                posList3.append((x, y))
            if events == cv2.EVENT_RBUTTONDOWN:
                for i, pos in enumerate(posList3):
                    x1, y1 = pos
                    if x1 < x < x1 + width and y1 < y < y1 + height:
                        posList3.pop(i)
 
            with open('ParkingSlotPosition3', 'wb') as h:
                pickle.dump(posList3, h)
 
 
    while True:
        
        if a==3:

            img = cv2.imread('/home/arj/IBM_project/Data/car3.png')
            imgresized = cv2.resize(img,(1336,768))
            for pos in posList3 :

                cv2.rectangle(imgresized, pos, (pos[0] + width, pos[1] + height), (0,0, 0), 3)

            cv2.imshow("Image", imgresized)
            cv2.setMouseCallback("Image", mouseClick)

        if a==1:

            img = cv2.imread('/home/arj/IBM_project/Data/carParkImg.png')
            for pos in posList:

                cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0,0, 0), 3)
            cv2.imshow("Image", img)
            cv2.setMouseCallback("Image", mouseClick)
        if a==0:
            b=0
            img1=cv2.imread('/home/arj/IBM_project/Data/carParking2.png')
            imgresized = cv2.resize(img1,(1080,720))
        
            for pos in posList2:
                if (b<=7):
                    cv2.rectangle(imgresized, pos, (pos[0] + width, pos[1] + height), (0, 0, 0), 3)
                    b=b+1
                else:
                    b=b+1
                    cv2.rectangle(imgresized, pos, (pos[0] + width1, pos[1] + height1), (0, 0, 0), 3)
            cv2.imshow("Image",imgresized)
            cv2.setMouseCallback("Image", mouseClick)
        cv2.waitKey(1)

if __name__=='__main__':
    #Passing input 
    #Here three parking slot is used
    #need to pass the image.Here we need to pass values 1 0 and 3
    #1 = carparking input 1
    #0 = carparking input 2
    #3 = carparking input 3
    selecting_ROI(1)
