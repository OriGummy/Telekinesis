import asyncio
from json import dumps
from queue import Queue
import threading
import cv2
import mediapipe as mp
import numpy as np
import websockets
from random import randint
from uuid import getnode as get_mac
mac = get_mac()

SERVER_IP = '10.10.10.31'

queue = Queue()
def ws():
    my_id = mac
    print('My address is ', mac)
    async def run():
        while True:
            try:
                async with websockets.connect(f'ws://{SERVER_IP}:8001') as client:
                    print('Connected.')
                    await client.send(dumps({'display': False, 'camera': True, 'id': my_id}))
                    while True:
                        await client.send(queue.get())
            except:
                print('Exception - reconnecting...')
    asyncio.run(run())

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
def run():
        cap = cv2.VideoCapture(0)
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()
                
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
            
                # Make detection
                results = pose.process(image)
                landmarks = None
                try:
                    landmarks = results.pose_landmarks.landmark
                except:
                    pass

                if landmarks:
                    posture = {}
                    # print(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
                    for key in (
                        mp_pose.PoseLandmark.LEFT_SHOULDER,
                        mp_pose.PoseLandmark.LEFT_ELBOW,
                        mp_pose.PoseLandmark.LEFT_WRIST,
                        mp_pose.PoseLandmark.RIGHT_SHOULDER,
                        mp_pose.PoseLandmark.RIGHT_ELBOW,
                        mp_pose.PoseLandmark.RIGHT_WRIST
                    ):
                        landmark = landmarks[key.value]
                        posture[key.name] = [landmark.x, landmark.y, landmark.z, landmark.visibility]
                        queue.put(dumps(posture))
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )               
                
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    threading.Thread(target=ws).start()
    run()