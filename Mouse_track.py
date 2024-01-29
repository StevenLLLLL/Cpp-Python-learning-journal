from pynput.mouse import Listener
import tkinter as tk
from PIL import Image, ImageDraw
import time as ti
from tkinter import messagebox
import os

# -------------------------声明
root = tk.Tk()
switch_total = False
switch_move = False
switch_click = False
screen_width = root.winfo_screenwidth()  # 获取屏幕宽度和高度
screen_height = root.winfo_screenheight()
img = Image.new('RGB', (screen_width, screen_height), color='black')
listener = None


# -------------------------绘制函数


def draw_image(dx, dy, radius, color):  # 绘制函数
    global img
    global root
    radius = radius
    draw = ImageDraw.Draw(img)
    leftUpPoint = (dx - radius, dy - radius)
    rightDownPoint = (dx + radius, dy + radius)
    twoPointList = [leftUpPoint, rightDownPoint]
    draw.ellipse(twoPointList, fill=color)

# -------------------------监听函数


def on_click(x, y, button, pressed):  # 持续检测鼠标的点击
    if pressed and switch_click and switch_total:
        print(f'Mouse clicked at ({x}, {y}) with {button}')
        draw_image(x, y, 6, 'pink')


def on_move(x, y):  # 持续检测鼠标的移动
    if switch_move and switch_total:
        print(f"Mouse moved at ({x}, {y})")
        draw_image(x, y, 1, 'white')


# -------------------------GUI函数


def create_GUI():
    def onclick_start():
        print("开始记录")
        global switch_total
        if not switch_total:
            switch_total = True
            global listener
            listener = Listener(on_click=on_click, on_move=on_move)
            listener.start()
        else:
            messagebox.showwarning("!", message="正在记录")

    def onclick_over():
        global img
        global switch_total
        if switch_total:
            print("结束记录")
            switch_total = False
            global listener
            listener.stop()
            listener = None
            local_time = ti.localtime()
            formatted_time = ti.strftime("%Y_%m_%d_%H_%M_%S", local_time)
            print(formatted_time)
            img.save(f"{formatted_time}.png")
            img.show()
            messagebox.showinfo("记录结束", message=f"图片保存到{os.path.dirname(__file__)}")
        else:
            print("已经结束")
            messagebox.showwarning("!", message="记录已经结束")
    global root
    root.title("监视鼠标轨迹")
    global screen_width
    global screen_height
    x = int(screen_width/2)
    y = int(screen_height/2)
    root.geometry(f"300x400+{x}+{y}")
    button_start = tk.Button(root, text="开始记录", command=onclick_start)
    button_over = tk.Button(root, text="结束记录", command=onclick_over)
    check_moveonly = tk.BooleanVar()
    check_clickonly = tk.BooleanVar()

    def onselect_only():
        if check_moveonly.get():
            print("记录移动")
            global switch_move
            switch_move = True
        else:
            print("取消记录移动")
            switch_move = False
        if check_clickonly.get():
            print("记录点击")
            global switch_click
            switch_click = True
        else:
            print("取消记录点击")
            switch_click = False

    Checkbutton_moveonly = tk.Checkbutton(root, text="记录移动", variable=check_moveonly, command=onselect_only)
    Checkbutton_clickonly = tk.Checkbutton(root, text="记录点击", variable=check_clickonly, command=onselect_only)
    button_start.place(x=115, y=50, width=70, height=30)
    button_over.place(x=115, y=90, width=70, height=30)
    Checkbutton_moveonly.place(x=115, y=130, width=70, height=30)
    Checkbutton_clickonly.place(x=115, y=160, width=70, height=30)
    root.mainloop()  # 启动事件循环


# -------------------------主程序
create_GUI()
