import cv2
import time



cap = cv2.VideoCapture(0)

if cap.isOpened():
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print('\n',f'CAP_PROP_FRAME_WIDTH\t{width}',f'CAP_PROP_FRAME_HEIGHT\t{height}',f'CAP_PROP_FRAME_FPS\t{fps}',f'CAP_PROP_FRAME_FRAME_COUNT\t{frame_count}')

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
cap.set(cv2.CAP_PROP_FPS,30)
#start=time.time()

while True:
    try:
        ret,img = cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imshow('image',img)
        if cv2.waitKey(1) == ord('q'):
            break
    except AssertionError as e:
        print(e)

cap.release()

cv2.destroyAllWindows()