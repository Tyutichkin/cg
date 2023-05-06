import colorutils as cu

C_W = 900
C_H = 700

def set_pixel(img, x, y, color):
    img.put(color, (x, y))

def draw_line(img, points):
    for i in points:
        set_pixel(img, i[0], i[1], i[2])

def rgb(color):
    return (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))

def seed(img, canvas, seed_pixel, mark_color, border_color_rgb, delay):
    mark_color_rgb = rgb(mark_color)
    stack = [seed_pixel]

    while(len(stack)):
        seed_pixel = stack.pop()
        x = seed_pixel[0]
        y = seed_pixel[1]
        set_pixel(img, x, y, mark_color)
        x_tmp = x
        y_tmp = y
        x += 1

        while img.get(x, y) != mark_color_rgb and img.get(x, y) != border_color_rgb and x < C_W:
            set_pixel(img, x, y, mark_color)
            x += 1
        x_right = x - 1
        x = x_tmp - 1

        while img.get(x, y) != mark_color_rgb and img.get(x, y) != border_color_rgb and x > 0:
            set_pixel(img, x, y, mark_color)
            x -= 1
        x_left = x + 1
        x = x_left
        y = y_tmp + 1

        while x <= x_right:
            flag = False

            while img.get(x, y) != mark_color_rgb and img.get(x, y) != border_color_rgb and x <= x_right:
                flag = True
                x += 1

            if flag:
                if x == x_right and img.get(x, y) != mark_color_rgb and img.get(x, y) != border_color_rgb:
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
                flag = False
            x_beg = x
    
            while (img.get(x, y) == mark_color_rgb or img.get(x, y) == border_color_rgb) and x < x_right:
                x = x + 1

            if x == x_beg:
                x += 1

        x = x_left
        y = y_tmp - 1

        while x <= x_right:
            flag = False

            while img.get(x, y) != mark_color_rgb and img.get(x, y) != border_color_rgb and x <= x_right:
                flag = True
                x += 1
            if flag:
                if x == x_right and img.get(x, y) != mark_color_rgb and img.get(x, y) != border_color_rgb:
                    stack.append([x, y])
                else:
                    stack.append([x - 1, y])
                flag = False
            x_beg = x
            
            while (img.get(x, y) == mark_color_rgb or img.get(x, y) == border_color_rgb) and x < x_right:
                x = x + 1

            if x == x_beg:
                x += 1
            
        if (delay):
            canvas.update()