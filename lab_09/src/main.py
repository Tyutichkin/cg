from tkinter import *
from tkinter import messagebox
from numpy import *
from colorutils import *
from copy import *
from itertools import *
from tkinter import colorchooser
import tkmacosx

CANVAS_WIDTH = 795

is_cutter_set = False


def get_cutter_color():
    return btn_cutter_color["bg"]


def get_line_color():
    return btn_line_color["bg"]


def get_result_color():
    return btn_result_color["bg"]


def left_click(event):
    global figure

    update_figure(figure)

    x = event.x
    y = event.y

    color = get_line_color()

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    figure.append([x, y])

    if len(figure) >= 2:
        MainCanvas.create_line(figure[-2], figure[-1], fill=color)


def right_click(event):
    global cutter, figure

    if (is_maked(cutter)):
        cutter.clear()
        MainCanvas.delete("all")
        color = get_line_color()
        MainCanvas.create_polygon(figure, outline=color, fill="white")

    x = event.x
    y = event.y

    color = get_cutter_color()

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    cutter.append([x, y])

    if len(cutter) >= 2:
        MainCanvas.create_line(cutter[-2], cutter[-1], fill=color)


def lock_cutter():
    global cutter

    if len(cutter) < 3:
        messagebox.showwarning("Ошибка", "Отсекатель должен иметь более 2 вершин\n")
        return

    if (is_maked(cutter)):
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return

    if cutter[0] == cutter[-1]:
        return

    color = get_cutter_color()

    cutter.append(cutter[0])

    MainCanvas.create_line(cutter[-2], cutter[-1], fill=color)


def lock_figure():
    global figure

    if len(figure) < 3:
        messagebox.showwarning("Ошибка", "Многоугольник должен иметь более 2 вершин\n")
        return

    if (is_maked(figure)):
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return

    if figure[0] == figure[-1]:
        return

    color = get_line_color()

    figure.append(figure[0])

    MainCanvas.create_line(figure[-2], figure[-1], fill=color)


def update_figure(figure):
    global cutter

    if (len(figure) > 3 and figure[0] == figure[-1]):
        figure.clear()
        cutter.clear()
        MainCanvas.delete("all")

        return


def add_cutter_point():
    global cutter

    try:
        x = int(XC_entry.get())
        y = int(YC_entry.get())
    except:
        messagebox.showwarning("Ошибка", "Неверно заданны координаты вершины отсекателя\n")
        return

    if (is_maked(cutter)):
        cutter.clear()
        MainCanvas.delete("all")
        color = get_line_color()
        MainCanvas.create_polygon(figure, outline=color, fill="white")

    color = get_cutter_color()

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    cutter.append([x, y])

    if len(cutter) >= 2:
        MainCanvas.create_line(cutter[-2], cutter[-1], fill=color)


def add_figure_point():
    global figure

    try:
        x = int(XF_entry.get())
        y = int(YF_entry.get())
    except:
        messagebox.showwarning("Ошибка", "Неверно заданны координаты вершины отрезка\n")
        return

    update_figure(figure)

    color = get_line_color()

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    figure.append([x, y])

    if len(figure) >= 2:
        MainCanvas.create_line(figure[-2], figure[-1], fill=color)


def is_maked(object):
    maked = False

    if (len(object) > 3):
        if ((object[0][0] == object[len(object) - 1][0]) and (object[0][1] == object[len(object) - 1][1])):
            maked = True

    return maked


def solve():
    if (not is_maked(cutter)):
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if (not is_maked(figure)):
        messagebox.showinfo("Ошибка", "Многоугольник не замкнут")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    if (len(cutter) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (extra_check(figure)):
        messagebox.showinfo("Ошибка", "Отсекаемое должно быть многоугольником")
        return

    result = deepcopy(figure)

    for current_point_index in range(-1, len(cutter) - 1):
        line = [cutter[current_point_index], cutter[current_point_index + 1]]

        position_point = cutter[current_point_index + 1]

        result = sutherland_hodgman_algorithm(line, position_point, result)

        if (len(result) <= 2):
            return

    draw_result_figure(result)


def draw_result_figure(figure_dots):
    fixed_figure = remove_odd_sides(figure_dots)

    color = get_result_color()

    for line in fixed_figure:
        MainCanvas.create_line(line[0], line[1], fill=color)


def line_coefficients(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c


def lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    if (opr == 0):
        return -5, -5  # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def is_coord_between(left, right, point):
    return (min(left, right) <= point) and (max(left, right) >= point)


def is_point_common(point_l, point_r, inter):
    return is_coord_between(point_l[0], point_r[0], inter[0]) and is_coord_between(point_l[1], point_r[1], inter[1])


def are_lines_connected(line1, line2):
    if ((line1[0][0] == line2[0][0]) and (line1[0][1] == line2[0][1])) \
            or ((line1[1][0] == line2[1][0]) and (line1[1][1] == line2[1][1])) \
            or ((line1[0][0] == line2[1][0]) and (line1[0][1] == line2[1][1])) \
            or ((line1[1][0] == line2[0][0]) and (line1[1][1] == line2[0][1])):
        return True

    return False


def extra_check(object):  # чтобы не было пересечений

    cutter_lines = []

    for i in range(len(object) - 1):
        cutter_lines.append([object[i], object[i + 1]])  # разбиваю отсекатель на линии

    combinations_lines = list(combinations(cutter_lines, 2)) # все возможные комбинации сторон
    

    for i in range(len(combinations_lines)):
        line1 = combinations_lines[i][0]
        line2 = combinations_lines[i][1]

        if (are_lines_connected(line1, line2)):
            continue

        a1, b1, c1 = line_coefficients(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
        a2, b2, c2 = line_coefficients(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

        intersection_point = lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_point_common(line1[0], line1[1], intersection_point)) and (
                is_point_common(line2[0], line2[1], intersection_point)):
            return True

    return False


def get_vector(point_1, point_2):
    return [point_2[0] - point_1[0], point_2[1] - point_1[1]]


def vector_product(vector_1, vector_2):
    return (vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0])


def scalar_product(vector_1, vector_2):
    return (vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1])


def check_polygon():  # через проход по всем точкам, поворот которых должен быть все время в одну сторону
    if (len(cutter) < 3):
        return False

    temp = vector_product(get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1]))

    sign = 1 if temp > 0 else -1  # 1 - clockwise; -1 = counterclockwise

    for i in range(3, len(cutter)):
        temp = sign * vector_product(get_vector(cutter[i - 1], cutter[i]), get_vector(cutter[i - 2], cutter[i - 1]))

        if temp < 0:
            return False

    temp = sign * vector_product(get_vector(cutter[0], cutter[1]), get_vector(cutter[-2], cutter[0]))
    print(cutter[0], cutter[-1], cutter[-2], cutter[1])

    if temp < 0:
        return False

    if (extra_check(cutter)):
        return False

    if (sign < 0):
        cutter.reverse()

    return True


def get_normal(point_1, point_2, point_3):
    f_vector = get_vector(point_1, point_2)

    if (f_vector[1]):
        normal = [1, -f_vector[0] / f_vector[1]]
    else:
        normal = [0, 1]

    position_vector = get_vector(point_2, point_3)

    if (scalar_product(position_vector, normal) < 0):
        normal[0] = -normal[0]
        normal[1] = -normal[1]

    return normal


def is_visible(point, f_point, s_point):
    vector_1 = get_vector(f_point, s_point)
    vector_2 = get_vector(f_point, point)

    if (vector_product(vector_1, vector_2) <= 0):
        return True
    else:
        return False


def get_lines_parametric_intersection(line1, line2, normal):
    d = get_vector(line1[0], line1[1])
    w = get_vector(line2[0], line1[0])

    d_scalar = scalar_product(d, normal)
    w_scalar = scalar_product(w, normal)

    t = -w_scalar / d_scalar

    intersection_point = [line1[0][0] + d[0] * t, line1[0][1] + d[1] * t]

    return intersection_point


def sutherland_hodgman_algorithm(cutter_line, position, previous_result):
    current_result = []

    point_1 = cutter_line[0]
    point_2 = cutter_line[1]

    normal = get_normal(point_1, point_2, position)

    previous_vision = is_visible(previous_result[-2], point_1, point_2)

    for current_point_index in range(-1, len(previous_result)):
        current_vision = is_visible(previous_result[current_point_index], point_1, point_2)

        if (previous_vision):
            if (current_vision):
                current_result.append(previous_result[current_point_index])
            else:
                figure_line = [previous_result[current_point_index - 1], previous_result[current_point_index]]

                current_result.append(get_lines_parametric_intersection(figure_line, cutter_line, normal))
        else:
            if (current_vision):
                figure_line = [previous_result[current_point_index - 1], previous_result[current_point_index]]

                current_result.append(get_lines_parametric_intersection(figure_line, cutter_line, normal))

                current_result.append(previous_result[current_point_index])

        previous_vision = current_vision

    return current_result


def make_unique(sides):
    for side in sides:
        side.sort()

    return list(sides)


def is_point_on_side(point, side):
    if abs(vector_product(get_vector(point, side[0]), get_vector(side[1], side[0]))) <= 1e-6:
        if (side[0] < point < side[1] or side[1] < point < side[0]):
            return True

    return False


def get_sides(side, rest_point):
    point_list = [side[0], side[1]]

    for point in rest_point:
        if is_point_on_side(point, side):
            point_list.append(point)

    point_list.sort()

    sections_list = list()

    for i in range(len(point_list) - 1):
        sections_list.append([point_list[i], point_list[i + 1]])

    return sections_list


def remove_odd_sides(figure_points):
    all_sides = list()
    rest_points = figure_points[2:]

    for i in range(len(figure_points)):
        current_side = [figure_points[i], figure_points[(i + 1) % len(figure_points)]]

        all_sides.extend(get_sides(current_side, rest_points))

        rest_points.pop(0)
        rest_points.append(figure_points[i])

    return make_unique(all_sides)


def clear_field():
    global lines
    global cutter
    global figure

    MainCanvas.delete("all")

    lines = []
    cutter = []
    figure = []


def change_line_color():
    print("OK1")
    global btn_line_color
    line_color = colorchooser.askcolor(title="Выберите цвет линии")[1]
    btn_line_color.configure(bg=line_color)


def change_cutter_color():
    print("OK2")
    global btn_cutter_color
    cutter_color = colorchooser.askcolor(title="Выберите цвет отсекателя")[1]
    btn_cutter_color.configure(bg=cutter_color)


def change_res_color():
    print("OK3")
    global btn_result_color
    res_color = colorchooser.askcolor(title="Выберите цвет результата")[1]
    btn_result_color.configure(bg=res_color)

def show_infobox(window_title, text):
    messagebox.showinfo(window_title, text)

if __name__ == "__main__":
    window = Tk()

    menubar = Menu(window)
    window.config(menu=menubar)
    menu = Menu(menubar, tearoff=0)
    menu.add_command(label='О программе', command=lambda: show_infobox('О программе',
                                                                       'Реализация алгоритма Сазерленда-Ходжмена отсечения многоугольников.')
                     )
    menu.add_command(label='Об авторе', command=lambda: show_infobox('Об авторе', 'Тютичкин Семен ИУ7-45Б'))
    menu.add_separator()
    menu.add_command(label='Выход', command=lambda: window.destroy())
    menubar.add_cascade(
        label="Меню",
        menu=menu
    )

    window.geometry("1370x800")
    window.title("Lab_09")
    window.tk_setPalette("#E6E9ED")
    window.resizable(True, True)
    window.columnconfigure(tuple(range(4, 14)), weight=1)
    window.columnconfigure(tuple(range(4)), weight=3)
    window.rowconfigure(tuple(range(13)), weight=1)

    MainCanvas = Canvas(window, width=795, height=795, bg="#ffffff")
    MainCanvas.grid(column=4, columnspan=2, row=0, rowspan=13, sticky=NSEW)

    lines = []
    figure = []

    cutter = []

    MainCanvas.bind('<1>', lambda event: left_click(event))
    MainCanvas.bind('<2>', lambda event: right_click(event))

    alg_label = Label(text="Цвет многоугольника", font=("Arial", 15))
    alg_label.grid(row=0, column=0, columnspan=2, sticky=NSEW)
    btn_line_color = tkmacosx.Button(window, bg="#0f0f0f", width=10, command=lambda: change_line_color())
    btn_line_color.grid(row=0, column=3, sticky=NSEW)

    cutter_color_label = Label(text="Цвет отсекателя", font=("Arial", 15))
    cutter_color_label.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    btn_cutter_color = tkmacosx.Button(window, bg="#fcba03", width=10, command=lambda: change_cutter_color())
    btn_cutter_color.grid(row=1, column=3, sticky=NSEW)

    color_label = Label(text="Цвет результата", font=("Arial", 15))
    color_label.grid(row=2, column=0, columnspan=2, sticky=NSEW)
    btn_result_color = tkmacosx.Button(window, "#fc0303", width=10, command=lambda: change_res_color())
    btn_result_color.grid(row=2, column=3, sticky=NSEW)

    line_label = Label(text="Построение многоугольника", font=("Arial", 15))
    line_label.grid(row=3, column=0, columnspan=4, sticky=NSEW)

    XF_label = Label(text="X:", font=("Arial", 15))
    XF_label.grid(row=4, column=0, sticky=NSEW)

    XF_entry = Entry(window, bg="#ffffff", font=("Arial", 15))
    XF_entry.grid(row=4, column=1, sticky=NSEW)

    YF_label = Label(text="Y:", font=("Arial", 15))
    YF_label.grid(row=4, column=2, sticky=NSEW)

    YF_entry = Entry(window, bg="#ffffff", font=("Arial", 15))
    YF_entry.grid(row=4, column=3, sticky=NSEW)

    line_button = tkmacosx.Button(text="Построить отрезок", font=("Arial", 15), bg="#FFFFFF", command=lambda: add_figure_point())
    line_button.grid(row=5, column=0, columnspan=4, sticky=NSEW)

    cutter_label = Label(text="Построение вершины отсекателя", font=("Arial", 15))
    cutter_label.grid(row=6, column=0, columnspan=4, sticky=NSEW)

    XC_label = Label(text="X:", font=("Arial", 15))
    XC_label.grid(row=7, column=0, sticky=NSEW)

    XC_entry = Entry(window, bg="#ffffff", font=("Arial", 15))
    XC_entry.grid(row=7, column=1, sticky=NSEW)

    YC_label = Label(text="Y:", font=("Arial", 15))
    YC_label.grid(row=7, column=2, sticky=NSEW)

    YC_entry = Entry(window, bg="#ffffff", font=("Arial", 15))
    YC_entry.grid(row=7, column=3, sticky=NSEW)

    cutter_button = tkmacosx.Button(text="Построить вершину отсекателя", font=("Arial", 15), bg="#FFFFFF",
                           command=lambda: add_cutter_point())
    cutter_button.grid(row=8, column=0, columnspan=4, sticky=NSEW)

    lock_cutter_button = tkmacosx.Button(text="Замкнуть отсекатель", font=("Arial", 15), bg="#FFFFFF",
                                command=lambda: lock_cutter())
    lock_cutter_button.grid(row=9, column=0, columnspan=4, sticky=NSEW)

    lock_figure_button = tkmacosx.Button(text="Замкнуть многоугольник", font=("Arial", 15), bg="#FFFFFF",
                                command=lambda: lock_figure())
    lock_figure_button.grid(row=10, column=0, columnspan=4, sticky=NSEW)

    result_button = tkmacosx.Button(text="Отсечь", font=("Arial", 15), bg="#FFFFFF", command=lambda: solve())
    result_button.grid(row=11, column=0, columnspan=4, sticky=NSEW)

    clear_button = tkmacosx.Button(text="Очистить поле", font=("Arial", 15), bg="#FFFFFF", command=lambda: clear_field())
    clear_button.grid(row=12, column=0, columnspan=4, sticky=NSEW)

    window.mainloop()
