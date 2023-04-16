from math import floor, fabs, radians, pi, cos, sin

PI = pi

def drawLine(curAlgorithm: int, begPoint: list, endPoint: list, lineColor, stepCount = False):

    points = []

    begPoint = list(map(lambda x: round(x), begPoint))
    endPoint = list(map(lambda x: round(x), endPoint))

    if curAlgorithm == 0:
        points = dda(begPoint, 
                     endPoint,
                    lineColor,
                    stepCount)
    elif curAlgorithm == 1:
        points = bresenhamFloat(begPoint,
                                endPoint,
                                lineColor,
                                stepCount)
    elif curAlgorithm == 2:
        points = bresenhamInt(begPoint,
                            endPoint,
                            lineColor,
                            stepCount)
    elif curAlgorithm == 3:
        points = bresenhamSmooth(begPoint,
                                endPoint,
                                lineColor,
                                stepCount)
    elif curAlgorithm == 4:
        points = wu(begPoint,
                    endPoint,
                    lineColor,
                    stepCount)
    else:
        points = [begPoint, 
                  endPoint, 
                  getColor(lineColor, 100), 
                  "libFunc"]
        
    return points

def getColor(color: tuple, intensity):
    # print(color, " ||| ", color + (intensity,))
    return color + (intensity,)

def getRadians(angel):
    return radians(angel)

def getCos(angel):
    return cos(angel)

def getSin(angel):
    return sin(angel)

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def dda(begPoint: list, endPoint: list, color, stepCount = False):

    x1, y1 = begPoint
    x2, y2 = endPoint

    if (x2 - x1 == 0) and (y2 - y1 == 0):
        begPoint.append(getColor(color, 100))
        return [begPoint]

    dx = x2 - x1
    dy = y2 - y1
    
    l = abs(dy)
    if abs(dx) >= abs(dy): 
        l = abs(dx) 

    dx /= l
    dy /= l

    x = x1
    y = y1

    points = [[x, y, getColor(color, 100)]]

    i = 1
    steps = 0

    while i <= l:

        if stepCount:
            xTemp = x
            yTemp = y

        x += dx
        y += dy

        if not stepCount:
            points.append([int(round(x)), int(round(y)), getColor(color, 100)])
        elif (round(xTemp) != round(x) and round(yTemp) != round(y)):
            steps += 1

        i += 1

    if stepCount:
        return steps
    else:
        return points
    
def bresenhamFloat(begPoint: list, endPoint: list, color, stepCount = False):

    x1, y1 = begPoint
    x2, y2 = endPoint

    dx = x2 - x1
    dy = y2 - y1

    if (dx == 0) and (dy == 0):
        begPoint.append(getColor(color, 100))
        return [begPoint]
    
    x = x1
    y = y1

    signX = sign(dx)
    signY = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    swaped = False
    if dy > dx:
        swaped = True
        dx, dy = dy, dx

    m = dy / dx
    e = m - 0.5

    xTemp = x
    yTemp = y

    points = []
    steps = 0

    i = 0
    while i <= dx:
        if not stepCount:
            points.append([x, y, getColor(color, 100)])
        if e >= 0:
            if swaped:
                x += signX
            else:
                y += signY
            e -= 1
        if swaped:
            y += signY
        else:
            x += signX
        e += m

        if stepCount :
            if xTemp != x and yTemp != y:
                steps += 1

            xTemp = x
            yTemp = y

        i += 1

    if stepCount:
        return steps
    else:
        return points

def bresenhamInt(begPoint: list, endPoint: list, color, stepCount = False):

    x1, y1 = begPoint
    x2, y2 = endPoint

    dx = x2 - x1
    dy = y2 - y1

    if (dx == 0) and (dy == 0):
        begPoint.append(getColor(color, 100))
        return [begPoint]
    
    x = x1
    y = y1

    signX = sign(dx)
    signY = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    swaped = False
    if dy > dx:
        swaped = True
        dx, dy = dy, dx

    e = 2 * dy - dx

    points = []
    steps = 0

    xTemp = x
    yTemp = y

    i = 0
    while i <= dx:
        if not stepCount:
            points.append([x, y, getColor(color, 100)])
        if e >= 0:
            if swaped:
                x += signX
            else:
                y += signY
            e -= 2 * dx
        if swaped:
            y += signY
        else:
            x += signX
        e += 2 * dy
        if stepCount :
            if xTemp != x and yTemp != y:
                steps += 1
            xTemp = x
            yTemp = y
        i += 1

    if stepCount:
        return steps
    else:
        return points

def bresenhamSmooth(begPoint: list, endPoint: list, color, stepCount = False):
    
    x1, y1 = begPoint
    x2, y2 = endPoint

    dx = x2 - x1
    dy = y2 - y1

    if (dx == 0) and (dy == 0):
        begPoint.append(getColor(color, 100))
        return [begPoint]
    
    x = x1
    y = y1

    signX = sign(dx)
    signY = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    swaped = False
    if dy > dx:
        swaped = True
        dx, dy = dy, dx

    intensity = 255

    m = dy / dx
    w = 1 - m
    e = 0.5

    points = []

    xTemp = x
    yTemp = y

    i = 0
    steps = 0
    while i <= dx:
        if not stepCount:
            points.append([x, y, getColor(color, round(intensity * e))])
        if e < w:
            if swaped:
                y += signY
            else:
                x += signX
            e += m
        else:
            x += signX
            y += signY
            e -= w

        if stepCount :
            if xTemp != x and yTemp != y:
                steps += 1

            xTemp = x
            yTemp = y

        i += 1

    if stepCount:
        return steps
    else:
        return points

def wu(begPoint: list, endPoint: list, color, stepCount = False):
    
    x1, y1 = begPoint
    x2, y2 = endPoint

    dx = x2 - x1
    dy = y2 - y1

    if (dx == 0) and (dy == 0):
        begPoint.append(getColor(color, 100))
        return [begPoint]

    m = 1
    step = 1
    intensity = 255

    points = []
    steps = 0

    if abs(dy) >= abs(dx):
        if dy != 0:
            m = dx / dy
        m1 = m
        if y1 > y2:
            m1 *= -1
            step *= -1
        yEnd = round(y2) - 1 if (dy < dx) else round(y2) + 1
        for yCur in range(round(y1), yEnd, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1
            if not stepCount:
                points.append([int(x1) + 1, yCur, getColor(color, round(fabs(d1) * intensity))])
                points.append([int(x1), yCur, getColor(color, round(fabs(d2) * intensity))])
            elif yCur < round(y2) and int(x1) != int(x1 + m):
                steps += 1
            x1 += m1
    else:
        if dx != 0:
            m = dy / dx
        m1 = m
        if x1 > x2:
            m1 *= -1
            step *= -1
        xEnd = round(x2) - 1 if (dy > dx) else round(x2) + 1
        for xCur in range(round(x1), xEnd, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1
            if not stepCount:
                points.append([xCur, int(y1) + 1, getColor(color, round(fabs(d1) * intensity))])
                points.append([xCur, int(y1), getColor(color, round(fabs(d2) * intensity))])
            elif xCur < round(x2) and int(y1) != int(y1 + m):
                steps += 1
            y1 += m1

    if stepCount:
        return steps
    else:
        return points
