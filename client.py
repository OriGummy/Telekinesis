from copy import copy
from action import Action
from utils import *

ids = [0]
class Client:
    def __init__(self, websocket, id=None):
        self.postures = {}
        self.directions = {}
        self.enemy = False
        self.websocket = websocket
        if id is not None:
            self.id = id
        else:
            self.id = ids[0]
            ids[0] += 1
        

    async def send_action(self, action: Action):
        await self.websocket.send(action)

    def set_postures(self, postures):
        self.postures = copy(postures)
        for camera_id in self.postures.keys():
            right_hand = posture_to_hands(postures[camera_id])[1]
            if right_hand is None:
                return False
            self.directions[camera_id] = pointing_direction(right_hand) # Right Hand Calibrates!!!
        return True
    
    def dot(self, directions_by_camera):
        return sum(dot(self.directions[camera_id], directions_by_camera.get(camera_id, (0, 0, 0))) for camera_id in self.directions.keys())

    def dot_by_posture(self, postures):
        sum = 0
        for idx in self.postures.keys():
            dir = posture_to_norm_vector(postures[idx])
            sum += self.postures[idx][0] * dir[0][0] + self.postures[idx][1] * dir[0][1]
        return sum
