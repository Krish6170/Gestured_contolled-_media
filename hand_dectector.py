import cv2
import time
import mediapipe as mp


class detector:
    def __init__(self, static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.static_image_mode=static_image_mode
        self.max_num_hands=max_num_hands
        self.min_detection_confidence=min_detection_confidence
        self.min_tracking_confidence=min_tracking_confidence
        self.hand = mp.solutions.hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing = mp.solutions.drawing_utils



    def detect(self,image,flip=0,draw=1):
        """
        detects the image and draws and return image
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if flip:
            image = cv2.flip(image, 1)
        self.results = self.hand.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        if self.results.multi_hand_landmarks:

            for hdlm in self.results.multi_hand_landmarks:
                for id, ldm in enumerate(hdlm.landmark):
                    if draw:
                        self.drawing.draw_landmarks(image, hdlm, mp.solutions.hands.HAND_CONNECTIONS)
        return image



    def track_landmark_list(self,image,handnumber=0):
        lst = []
        if self.results.multi_hand_landmarks:
            # if len(self.results.multi_hand_landmarks) == 2:
            #
            #     handno = self.results.multi_hand_landmarks[handnumber]
            #
            #     for id, ldm in enumerate(handno.landmark):
            #         h, w, c = image.shape
            #         x, y = int(w * ldm.x), int(h * ldm.y)
            #         temp = [x, y]
            #         lst.append(temp)

            handno = self.results.multi_hand_landmarks[0]
            for id, ldm in enumerate(handno.landmark):
                h, w, c = image.shape
                x, y = int(w * ldm.x), int(h * ldm.y)
                temp = [x, y]
                lst.append(temp)
        return lst

if __name__ == '__main__':
    p_time = 0
    c_time = 0
    vid = cv2.VideoCapture(0)
    hand=detector()

    while True:

        success, image = vid.read()
        image=hand.detect(image,1)
        lst = hand.track_landmark_list(image)
        print("helllo")


        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(image, str(int(fps)), (70, 80), 2, 3, [200, 0, 0])

        cv2.imshow("image", image)


        if cv2.waitKey(1) & 0xFF == ord("p"):
            break
