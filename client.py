from copy import copy
from action import Action
from utils import normalize, posture_to_norm_vector

ids = [0]
class Client:
    def __init__(self, websocket, id=None):
        self.postures = {}
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
        for idx in self.postures.keys():
            coords = postures[idx]
            self.postures[idx] = [*posture_to_norm_vector(coords)[0], 0, 0]

    def dot(self, postures):
        sum = 0
        for idx in self.postures.keys():
            dir = posture_to_norm_vector(postures[idx])
            sum += self.postures[idx][0] * dir[0][0] + self.postures[idx][1] * dir[0][1]
        return sum
