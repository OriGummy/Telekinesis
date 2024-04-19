def normalize(x, y):
    d = (x ** 2 + y ** 2) ** 0.5
    return x / d, y / d

def posture_to_norm_vector(posture):
    xl, yl = posture['LEFT_WRIST'][0] - posture['LEFT_SHOULDER'][0], posture['LEFT_WRIST'][1] - posture['LEFT_SHOULDER'][1]
    xr, yr = posture['RIGHT_WRIST'][0] - posture['RIGHT_SHOULDER'][0], posture['RIGHT_WRIST'][1] - posture['RIGHT_SHOULDER'][1]
    return normalize(xl, yl), normalize(xr, yr)