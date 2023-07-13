import cv2


cap = cv2.VideoCapture('/home/arj/IBM_project/Data/carParkingInput2.mp4')

output_path="/home/arj/IBM_project/Data/carparking2.mp4"
fourcc=cv2.VideoWriter_fourcc(*'avc1')
fps=cap.get(cv2.CAP_PROP_FPS)
frame_size=(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
length_of_video=frame_count/fps
print(length_of_video)
out=cv2.VideoWriter(output_path,fourcc,fps,(1080,720))

while (cap.isOpened()):
        
        # Get image frame
        success, img = cap.read()
        imgresized=cv2.resize(img,(1080,720))
        cv2.imshow("IMAGE",imgresized)
        cv2.waitKey(1)
        out.write(imgresized)


##code to find confidence score
import cv2
import pickle
import cvzone
import numpy as np

def Video_processing(video_path, c):
    cap = cv2.VideoCapture(video_path)
    
    # Define the output path for the processed video
    output_path = "/home/arj/IBM_project/flask/static/processed_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    length_of_video = frame_count / fps
    print(length_of_video)
    out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    # Define the parameters based on the value of 'c'
    if c == 2:
        width, height = 45, 21
        with open('ParkingSlotPosition3', 'rb') as f:
            posList = pickle.load(f)
    elif c == 1:
        width, height = 107, 48
        with open('ParkingSlotPosition', 'rb') as f:
            posList = pickle.load(f)
    elif c == 3:
        width, height = 140, 72
        width1, height1 = 65, 155
        with open('ParkingSlotPosition2', 'rb') as f:
            posList = pickle.load(f)

    # Define the threshold values based on the value of 'c'
    if c == 0:
        val1 = 26
        val2 = 25
        val3 = 2
    elif c == 1:
        val1 = 25
        val2 = 14
        val3 = 4
    elif c == 3:
        val1 = 26
        val2 = 14
        val3 = 4

    def checkSpaces():
        b = 0
        spaces = 0
        confidences = []

        for pos in posList:
            x, y = pos
            if c == 0:
                if b <= 7:
                    w, h = width, height
                    b += 1
                else:
                    w, h = width1, height1
            elif c == 1:
                w, h = width, height
            elif c == 3:
                w, h = width, height

            imgCrop = imgThres[y:y + h, x:x + w]
            count = cv2.countNonZero(imgCrop)

            confidence = count / (w * h)
            confidences.append(confidence)

            if c == 1:
                if count < 980:
                    color = (0, 255, 0)
                    thic = 5
                    spaces += 1
                else:
                    color = (0, 0, 255)
                    thic = 2
            if c == 0:
                if count < 710:
                    color = (0, 255, 0)
                    thic = 5
                    spaces += 1
                else:
                    color = (0, 0, 255)
                    thic = 2
            if c == 3:
                if count < 250:
                    color = (0, 255, 0)
                thic = 5
                spaces += 1
            else:
                color = (0, 0, 255)
                thic = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thic)
        cv2.putText(img, str(cv2.countNonZero(imgCrop)), (x, y + h - 6), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

        # Display confidence score
        confidence_text = f"Confidence: {confidence:.2f}"
        cv2.putText(img, confidence_text, (x, y + h + 20), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

        cvzone.putTextRect(img, f'Free:{spaces}/{len(posList)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))

        return confidences

    while cap.isOpened():
        success, img = cap.read()
        if success:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            if val1 % 2 == 0:
                val1 += 1
            if val3 % 2 == 0:
                val3 += 1
            imgThres = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, val1, val2)
            imgThres = cv2.medianBlur(imgThres, val3)
            kernel = np.ones((3, 3), np.uint8)
            imgThres = cv2.dilate(imgThres, kernel, iterations=1)
            confidences = checkSpaces()
            out.write(img)
            cv2.imshow("Image", img)
            key = cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

    return confidences

if __name__ == "__main__":
    video_path = '/home/arj/IBM_project/Data/carParkingInput.mp4'
    confidences = Video_processing(video_path, 1)
    print("Confidences:", confidences)
