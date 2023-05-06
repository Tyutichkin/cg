import tkinter as tk
from tkmacosx import *
from tkinter import messagebox
from time import time, sleep
from tkinter.colorchooser import askcolor
# import matplotlib.pyplot as plt
# import numpy as np
# from math import floor, fabs, cos, sin, radians, pi

from seed import *

C_W = 900
C_H = 700

index_point = 0


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def bresenham_int(beg_point, end_point, color):
    dx = end_point[0] - beg_point[0]
    dy = end_point[1] - beg_point[1]

    if dx == 0 and dy == 0:
        return [[beg_point[0], beg_point[1], color]]
    x_sign = sign(dx)
    y_sign = sign(dy)
    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        exchange = 1
    else:
        exchange = 0
    two_dy = 2 * dy
    two_dx = 2 * dx
    e = two_dy - dx
    x = beg_point[0]
    y = beg_point[1]
    points = []
    i = 0
    while i <= dx:
        points.append([x, y, color])

        if e >= 0:
            if exchange == 1:
                x += x_sign
            else:
                y += y_sign
            e -= two_dx

        if exchange == 1:
            y += y_sign
        else:
            x += x_sign
        e += two_dy
        i += 1
    return points


def click_left(event, figures, img, color_var, points_listbox):
    global index_point
    x = event.x
    y = event.y
    # TODO: check what color do
    color = "#0f0f0f"
    set_pixel(img, x, y, color)
    figures[-1][-1].append([x, y])
    index_point += 1
    pstr = "%d. (%d, %d)" % (index_point, x, y)
    points_listbox.insert(tk.END, pstr)

    if len(figures[-1][-1]) == 2:
        points = bresenham_int(figures[-1][-1][0], figures[-1][-1][1], color)
        draw_line(img, points)
        figures[-1][-1].append(points)
        figures[-1].append([figures[-1][-1][1]])


def click_centre(event, figures, img, color_var):
    if len(figures[-1][-1]) == 0:
        messagebox.showwarning("Ошибка", "Незамкнутых фигур нет!")
        return

    if len(figures[-1]) <= 2:
        messagebox.showwarning("Ошибка", "Фигура должна иметь больше 1 ребра!")
        return
    point = figures[-1][0][0]
    figures[-1][-1].append(point)
    color = "#0f0f0f"
    points = bresenham_int(figures[-1][-1][0], figures[-1][-1][1], color)
    draw_line(img, points)
    figures[-1][-1].append(points)
    figures.append([[]])

def change_color(btn: Button):
    color = askcolor(title="Tkinter Color Chooser")[1]
    btn.configure(bg=color)


def click_right(event, seed_pixel, img, color, points_listbox):
    x = event.x
    y = event.y
    seed_pixel[0] = x
    seed_pixel[1] = y
    set_pixel(img, x, y, color)
    pstr = f"Starting point [{points_listbox.size()}]: (%d, %d)" % (x, y)
    points_listbox.insert(tk.END, pstr)


def draw_point(figures, img, color_var, x_entry, y_entry, points_listbox):
    global index_point

    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except:
        messagebox.showwarning(
            "Ошибка", "Неверно заданны координаты точки!\n" "Ожидался ввод целых чисел."
        )
        return
    color = "#ff8000"
    set_pixel(img, x, y, color)
    figures[-1][-1].append([x, y])
    index_point += 1
    pstr = "%d. (%d, %d)" % (index_point, x, y)
    points_listbox.insert(tk.END, pstr)

    if len(figures[-1][-1]) == 2:
        points = bresenham_int(figures[-1][-1][0], figures[-1][-1][1], color)
        draw_line(img, points)
        figures[-1][-1].append(points)
        figures[-1].append([figures[-1][-1][1]])


def fill_figure(figures, img, canvas, color_var, mode_var, time_entry, seed_pixel):
    if len(figures[-1][0]) != 0:
        messagebox.showwarning("Ошибка", "Не все фигуры замкнуты!")
        return

    if seed_pixel == [-1, -1]:
        messagebox.showwarning("Ошибка", "Отсутствует затравка!")
        return
    mark_color = color_var
    border_color = rgb("#0f0f0f")
    delay = mode_var.get()
    start_time = time()
    seed(img, canvas, seed_pixel, mark_color, border_color, delay)
    end_time = time()
    time_str = str(round(end_time - start_time, 2)) + "s"
    time_entry.delete(0, tk.END)
    time_entry.insert(0, time_str)


def clear_canvas(img, canvas, figures, time_entry, points_listbox, seed_pixel):
    global index_point
    img.put("#ffffff", to=(0, 0, C_W, C_H))
    seed_pixel[0] = -1
    seed_pixel[1] = -1
    index_point = 0
    points_listbox.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    figures.clear()
    figures.append([[]])


def information():
    messagebox.showinfo(
        "Условие задачи",
        "Реализовать алгоритм растрового заполнения сплошных областей с использованием затравочного пиксела.",
    )


window = tk.Tk()
window.title("Lab_06")
window.geometry("1300x720")
window.resizable(True, True)
window["bg"] = "white"

c = tk.Canvas(window, width=C_W, height=C_H, bg="white", borderwidth=2, relief=tk.RAISED)
c.xview_scroll(800, "units")
c.yview_scroll(800, "units")
c.grid(row=0, column=2, columnspan=20, rowspan=14, sticky=tk.NSEW)

figures = [[[]]]

t = tk.IntVar()
t.set(0)

label1 = tk.Label(
    window,
    text="Цвет закраски:",
    height="1",
    font=("arial", 14),
)
label1.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

btn1 = Button(
    window,
    width=30,
    bg="#ff0000"
)
btn1["command"] = lambda :change_color(btn1)
btn1.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

label2 = tk.Label(
    window,
    text="Режим закраски:",
    height="1",
    font=("arial", 14),
)
label2.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW)

rad_btn_delay = Radiobutton(
    window,
    text="Без задержки",
    variable=t,
    value=0,
    height="1",
)
rad_btn_delay.grid(row=3, column=0, sticky=tk.W)

rad_btn_delay = Radiobutton(
    window,
    text="С задержкой",
    variable=t,
    value=1,
    height="1",
)
rad_btn_delay.grid(row=4, column=0, sticky=tk.W)

label3 = tk.Label(
    window,
    text="Построение точки вручную",
    height="1",
    font=("arial", 14),
)
label3.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW)

label4 = tk.Label(window, text="X:", height="1")
label4.grid(row=6, column=0, sticky=tk.NSEW)

ent_x = tk.Entry(window)
ent_x.grid(row=7, column=0, sticky=tk.NSEW)
ent_x.insert(0, 200)

label5 = tk.Label(window, text="Y:", height="1")
label5.grid(row=6, column=1, sticky=tk.NSEW)

ent_y = tk.Entry(window)
ent_y.grid(row=7, column=1, sticky=tk.NSEW)
ent_y.insert(0, 200)

btn_create_p = Button(
    text="Построение точки",
    command=lambda: draw_point(figures, img, btn1["bg"], ent_x, ent_y, points_listbox),
)
btn_create_p.grid(row=8, column=0, columnspan=2, sticky=tk.NSEW)

points_listbox = tk.Listbox(font=("Arial", 16))
points_listbox.grid(row=9, column=0, columnspan=2, sticky=tk.NSEW)

label6 = tk.Label(
    window, text="Время :", height="1", font=("arial", 14)
)
label6.grid(row=13, column=0, sticky=tk.NSEW)


time_entry = tk.Entry(window)
time_entry.grid(row=13, column=1, sticky=tk.NSEW)


butn1 = Button(
    text="Замыкание фигуры",
    command=lambda event="<3>": click_centre(event, figures, img, "#0f0f0f"),
)
butn1.grid(row=10, column=0, columnspan=2, sticky=tk.NSEW)

butn2 = Button(
    text="Закрашивание",
    command=lambda: fill_figure(figures, img, c, btn1["bg"], t, time_entry, seed_pixel),
)
butn2.grid(row=11, column=0, columnspan=2, sticky=tk.NSEW)

butn3 = Button(
    text="Очистка экрана",
    command=lambda: clear_canvas(
        img, c, figures, time_entry, points_listbox, seed_pixel
    ),
)
butn3.grid(row=12, column=0, columnspan=2, sticky=tk.NSEW)

# TODO: make menu info
# butn4 = Button(text="Условие задачи", command=lambda: information())
# butn4.place(x=15, y=725, width=255, height=35)


img = tk.PhotoImage(width=C_W, height=C_H)
c.create_image(-270, -370, image=img, state="normal")

seed_pixel = [-1, -1]

c.bind("<1>", lambda event: click_left(event, figures, img, "#0f0f0f", points_listbox))
c.bind(
    "<2>", lambda event: click_right(event, seed_pixel, img, btn1["bg"], points_listbox)
)

window.mainloop()
