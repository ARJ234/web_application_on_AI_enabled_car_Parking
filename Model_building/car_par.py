import cv2
import pickle
import cvzone
import numpy as np

""" Function to train the video and to preview the result """

def Video_processing(video_path,c):
    cap = cv2.VideoCapture(video_path)
    """old approach Stores the processed video in the path defined"""
    output_path="/home/arj/IBM_project/flask/static/processed_video.mp4"
    fourcc=cv2.VideoWriter_fourcc(*'avc1')
    fps=cap.get(cv2.CAP_PROP_FPS)
    frame_size=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    length_of_video=frame_count/fps
    print(length_of_video)
    out=cv2.VideoWriter(output_path,fourcc,fps,frame_size)
    if c == 2:
         width,height=45,21
         with open('ParkingSlotPosition3', 'rb') as f:
            posList = pickle.load(f)
    if c == 1:
         width,height=107,48
         with open('ParkingSlotPosition', 'rb') as f:
            posList = pickle.load(f)
    if c==3:
         
        width, height = 140,72
        width1,height1=65,155
        with open('ParkingSlotPosition2', 'rb') as f:
            posList = pickle.load(f)
    def empty(a):
        pass
    if c==0:
         val1=26
         val2=25
         val3=2
    if c==1:
        val1=25
        val2=14
        val3=4
    if c==3:
        val1=26
        val2=14
        val3=4
    def checkSpaces():
        b=0
        spaces = 0
        for pos in posList:
            x, y = pos
            if c==0:
                if (b<=7):
                    w, h = width, height
                    b=b+1
                else:
                    w,h=width1,height1
            elif c==1:
                w,h=width,height
            elif c==3:
                w,h=width,height
 
            imgCrop = imgThres[y:y + h, x:x + w]
            count = cv2.countNonZero(imgCrop)
            if c==1:

                if count < 980:
                    color = (0, 255, 0)
                    thic = 5
                    spaces += 1
 
                else:
                    color = (0, 0, 255)
                    thic = 2
            if c==0:
                if count < 710:
                    color = (0, 255, 0)
                    thic = 5
                    spaces += 1
 
                else:
                    color = (0, 0, 255)
                    thic = 2
            if c==3:
                if count < 250:
                    color = (0, 255, 0)
                    thic = 5
                    spaces += 1
 
                else:
                    color = (0, 0, 255)
                    thic = 2
 
            cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
 
            cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1,
                        color, 2)
 
            cvzone.putTextRect(img, f'Free:{spaces}/{len(posList)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))
    while (cap.isOpened()):
        # Get image frame
        success, img = cap.read()
        if success:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                # img = cv2.imread('img.png')
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            # ret, imgThres = cv2.threshold(imgBlur, 150, 255, cv2.THRESH_BINARY)
            if val1 % 2 == 0: val1 += 1
            if val3 % 2 == 0: val3 += 1
            imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, val1, val2)
            imgThres = cv2.medianBlur(imgThres, val3)
            kernel = np.ones((3, 3), np.uint8)
            imgThres = cv2.dilate(imgThres, kernel, iterations=1)
            checkSpaces()
            # Display Output
            out.write(img)
            cv2.imshow("Image",img)
            key = cv2.waitKey(1)
            if (cv2.waitKey(1)==ord('q')):
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return

    if key == ord('r'):
            pass

""" Function to return the frames to flask inorder to render the result to webpage"""

def process_video(frame,c):
        if c == '2':
             width,height=45,21
             with open('ParkingSlotPosition3', 'rb') as f:
                posList = pickle.load(f)
        if c == '1':
            width,height=107,48
            with open('ParkingSlotPosition', 'rb') as f:
              posList = pickle.load(f)
        if c=='3':
            width, height = 140,72
            width1,height1=65,155
            with open('ParkingSlotPosition2', 'rb') as f:
                posList = pickle.load(f)
        def empty(c):
            pass
        if c=='3':
            val1=26
            val2=25
            val3=2
        if c=='1':
            val1=25
            val2=14
            val3=4
        if c=='2':
            val1=26
            val2=14
            val3=4
        
        def checkSpaces():
            b = 0
            spaces = 0

            for pos in posList:
                x, y = pos
                if c == '3':
                    if b <= 7:
                        w, h = width, height
                        b = b + 1
                    else:
                        w, h = width1, height1
                elif c == '1':
                    w, h = width, height
                elif c == '2':
                    w, h = width, height

                imgCrop = imgThres[y:y + h, x:x + w]
                count = cv2.countNonZero(imgCrop)
                if c == '1':
                    if count < 980:
                        color = (0, 255, 0)
                        thic = 5
                        spaces += 1
                    else:
                        color = (0, 0, 255)
                        thic = 2
                if c == '3':
                    if count < 710:
                        color = (0, 255, 0)
                        thic = 5
                        spaces += 1
                    else:
                        color = (0, 0, 255)
                        thic = 2
                if c == '2':
                    if count < 250:
                        color = (0, 255, 0)
                        thic = 5
                        spaces += 1
                    else:
                        color = (0, 0, 255)
                        thic = 2

                cv2.rectangle(frame, (x, y), (x + w, y + h), color, thic)
                cv2.putText(frame, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
                cvzone.putTextRect(frame, f'Free:{spaces}/{len(posList)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))
        if val1 % 2 == 0: val1 += 1
        if val3 % 2 == 0: val3 += 1
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, val1, val2)
        imgThres = cv2.medianBlur(imgThres, val3)
        kernel = np.ones((3, 3), np.uint8)
        imgThres = cv2.dilate(imgThres, kernel, iterations=1)
        checkSpaces()
        return frame
if __name__=="__main__":
    #c = 1 parking slot 1
    #c = 0 parking slot 2
    #c = 3 parking slot 3
    video_path = '/home/arj/IBM_project/Data/carParkingInput.mp4'
    parking_slot=1
    Video_processing(video_path,parking_slot) 
                
        