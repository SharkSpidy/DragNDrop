import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(0)
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

    if hands is not None and len(hands) > 0:
        hand = hands[0]

    if isinstance(hand, dict) and 'lmList' in hand:
        lmList = hand['lmList']
        fingers = detector.fingersUp(hand)

        length, _, _ = detector.findDistance(lmList[8], lmList[12], img, draw=False)

        if length < 30:
            cursor = lmList[8]
            for rect in rectList:
                rect.update(cursor)


    # Create transparent layer
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx - w // 2, cy - h // 2),
                    (cx + w // 2, cy + h // 2), colorR, cv2.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    # Blend transparent overlay safely
    alpha = 0.5
    mask = imgNew.any(axis=2)  # Create a valid 2D boolean mask
    blended = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)
    out = np.where(mask[..., None], blended, img)


    cv2.imshow("Image", out)
    cv2.waitKey(1)