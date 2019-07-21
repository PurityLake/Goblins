def init_2d_array(w, h):
        arr = []
        for _ in range(h):
            line = []
            for _ in range(w):
                line.append(0.0)
            arr.append(line)
        return arr
    
def init_3d_array(w, h, l):
    arr = []
    for _ in range(l):
        area = []
        for _ in range(h):
            line = []
            for _ in range(w):
                line.append(0.0)
            area.append(line)
        arr.append(area)
    return arr

def interpolate(x0, x1, alpha):
    return x0 * (1 - alpha) + alpha * x1