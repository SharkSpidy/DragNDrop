import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(2)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
colorR = (255, 0, 255)


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and \
           cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

rectList = [DragRect([x * 250 + 150, 150]) for x in range(5)]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, hands = detector.findHands(img, draw=True)  # Now returns both image and hand list

    if hands:
        hand = hands[0]
        lmList = hand['lmList']  # List of 21 landmarks
        fingers = detector.fingersUp(hand)

        # Check distance between index and middle finger tips (landmarks 8 & 12)
        length, _, _ = detector.findDistance(lmList[8], lmList[12], img, draw=False)

        if length < 30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)



    cv2.imshow("Image", out)
    cv2.waitKey(1)