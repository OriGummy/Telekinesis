def normalize(x, y):
    d = (x ** 2 + y ** 2) ** 0.5
    return x / d, y / d

def posture_to_norm_vector(posture):
    xl, yl = posture['LEFT_WRIST'][0] - posture['LEFT_SHOULDER'][0], posture['LEFT_WRIST'][1] - posture['LEFT_SHOULDER'][1]
    xr, yr = posture['RIGHT_WRIST'][0] - posture['RIGHT_SHOULDER'][0], posture['RIGHT_WRIST'][1] - posture['RIGHT_SHOULDER'][1]
    return normalize(xl, yl), normalize(xr, yr)

def posture_to_hands(posture):
    hands = [None, None]
    try:
        hands[0] = [posture['LEFT_SHOULDER'], posture['LEFT_ELBOW'], posture['LEFT_WRIST']]
    except KeyError:
        hands[0] = tuple((0, 0, 0, 1) for i in range(3))
        pass
    try:
        hands[1] = [posture['RIGHT_SHOULDER'], posture['RIGHT_ELBOW'], posture['RIGHT_WRIST']]
    except KeyError:
        hands[1] = tuple((0, 0, 0, 1) for i in range(3))
        pass
    return hands

def pointing_direction(hand):
    return vector_diff(hand[2], hand[0])

def is_shooting(hand):
    return elbow_angle_arccosine(hand) > 0.5

def vector_diff(vec1, vec2):
    return vec1[0] - vec2[0], vec1[1] - vec2[1], vec1[2] - vec2[2]

def abs(vec):
    return (vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2) ** 0.5

def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1] + vec1[2] * vec2[2]

def elbow_angle_arccosine(hand):
    a = vector_diff(hand[0], hand[1])
    b = vector_diff(hand[1], hand[2])
    return dot(a, b) / (abs(a) * abs(b))
