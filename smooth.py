import ctypes
import cv2
import json
import math
import mss
import numpy as np
import os
import sys
import time
import torch
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
import uuid
import win32api
import win32con
import win32gui
import win32api
from tkinter import *
import threading
from termcolor import colored
from pynput import keyboard
import tkinter as tk
import win32con
import colorama
import win32api
import win32gui
from colorama import Fore

aimbotEnabled = False
triggerbotEnabled = False
show = False
showAimbotStatus = True
resx = 1720
resy = 1080
started = False
PUL = ctypes.POINTER(ctypes.c_ulong)

w = Fore.WHITE
b = Fore.BLACK
g = Fore.LIGHTGREEN_EX
y = Fore.LIGHTYELLOW_EX
m = Fore.LIGHTMAGENTA_EX
c = Fore.LIGHTCYAN_EX
lr = Fore.LIGHTRED_EX
lb = Fore.LIGHTBLUE_EX

global cls


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def tool():
    os.system("cls" if os.name == "nt" else "clear")


def clearConsole():
    return os.system("cls" if os.name in ("nt", "dos") else "clear")


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort),
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL),
    ]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


os.system("title Hyper Aim")


class Aimbot:
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    screen = mss.mss()
    with open("config.json") as f:
        sens_config = json.load(f)
    aimbot_status = colored("ENABLED", "green")

    def __init__(
        self, box_constant=325, collect_data=False, mouse_delay=0.00001, debug=False
    ):
        # controls the initial centered box width and height of the "Hyper Aim" window
        self.box_constant = box_constant  # controls the size of the detection box (equaling the width and height)
        clear = lambda: os.system("cls")
        clear()
        colorama.init()

        hyper = r"""

$$\   $$\ $$\     $$\ $$$$$$$\  $$$$$$$$\ $$$$$$$\         $$$$$$\  $$$$$$\ $$\      $$\ 
$$ |  $$ |\$$\   $$  |$$  __$$\ $$  _____|$$  __$$\       $$  __$$\ \_$$  _|$$$\    $$$ |
$$ |  $$ | \$$\ $$  / $$ |  $$ |$$ |      $$ |  $$ |      $$ /  $$ |  $$ |  $$$$\  $$$$ |
$$$$$$$$ |  \$$$$  /  $$$$$$$  |$$$$$\    $$$$$$$  |      $$$$$$$$ |  $$ |  $$\$$\$$ $$ |
$$  __$$ |   \$$  /   $$  ____/ $$  __|   $$  __$$<       $$  __$$ |  $$ |  $$ \$$$  $$ |
$$ |  $$ |    $$ |    $$ |      $$ |      $$ |  $$ |      $$ |  $$ |  $$ |  $$ |\$  /$$ |
$$ |  $$ |    $$ |    $$ |      $$$$$$$$\ $$ |  $$ |      $$ |  $$ |$$$$$$\ $$ | \_/ $$ |
\__|  \__|    \__|    \__|      \________|\__|  \__|      \__|  \__|\______|\__|     \__|

                                                                                         
                                    Github.com/hypr1x                                    
"""
        System.Size(120, 30)
        System.Clear()
        Anime.Fade(
            Center.Center(hyper),
            Colors.purple_to_blue,
            Colorate.Vertical,
            interval=0.030,
            enter=True,
        )

        if torch.cuda.is_available():
            Write.Print(
                f"CUDA ACCELERATION [ENABLED]\n", Colors.green_to_cyan, interval=0.000
            )
        else:
            Write.Print(
                f"[!] CUDA ACCELERATION IS UNAVAILABLE",
                Colors.black_to_red,
                interval=0.000,
            )
        self.model = torch.hub.load(
            "ultralytics/yolov3", "custom", path="best.pt", force_reload=True
        )
        self.pixel_increment = (
            1  # controls how many pixels the mouse moves for each relative movement
        )
        self.model.conf = 0.72  # base confidence threshold (or base detection (0-1)
        self.model.iou = 0.72  # NMS IoU (0-1)
        self.collect_data = collect_data
        self.mouse_delay = mouse_delay
        self.debug = debug
        clear()
        Write.Print(f"\n", Colors.blue_to_purple, interval=0.000)
        Write.Print(
            "════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════",
            Colors.purple_to_blue,
            interval=0.000,
        )
        print("\n\n\n\n")
        Write.Print(
            "                                    $$\   $$\ $$\     $$\ $$$$$$$\  $$$$$$$$\ $$$$$$$\  \n",
            Colors.purple_to_blue,
            interval=0.000,
        )
        Write.Print(
            "                                    $$ |  $$ | \$$\ $$  / $$ |  $$ |$$ |      $$ |  $$ |\n",
            Colors.purple_to_blue,
            interval=0.000,
        )
        Write.Print(
            "                                    $$$$$$$$ |  \$$$$  /  $$$$$$$  |$$$$$\    $$$$$$$  |\n",
            Colors.purple_to_blue,
            interval=0.000,
        )
        Write.Print(
            "                                    $$  __$$ |   \$$  /   $$  ____/ $$  __|   $$  __$$< \n",
            Colors.purple_to_blue,
            interval=0.000,
        )
        Write.Print(
            "                                    $$ |  $$ |    $$ |    $$ |      $$ |      $$ |  $$ |\n",
            Colors.purple_to_blue,
            interval=0.000,
        )
        Write.Print(
            f' > [version-{"3.0"}]                    $$ |  $$ |    $$ |    $$ |      $$$$$$$$\ $$ |  $$ |\n',
            Colors.purple_to_blue,
            interval=0.000,
        )
        Write.Print(
            f" > [Github.com/hypr1x]              \__|  \__|    \__|    \__|      \________|\__|  \__|\n",
            Colors.purple_to_blue,
            interval=0.000,
        )
        print("\n\n\n")
        Write.Print(
            "════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════",
            Colors.purple_to_blue,
            interval=0.000,
        )
        print("\n")
        print(
            f"""{m}""".replace("$", f"{m}${w}")
            + f"""
        {m}[{w}r{Fore.RESET}{m}]{Fore.RESET}  Enable SoftAim  {lb}|  {Fore.RESET}{m}[{w}p{Fore.RESET}{m}]{Fore.RESET}  Stream Proof    {lb}|  {Fore.RESET}{m}[{w}f2{Fore.RESET}{m}]{Fore.RESET}   Quit Program    {lb}|  {Fore.RESET}{m}[{w}del{Fore.RESET}{m}]{Fore.RESET}  Delete GUI       {b}
        {m}[{w}r{Fore.RESET}{m}]{Fore.RESET}  Disable Softaim {lb}|  {Fore.RESET}{m}[{w}o{Fore.RESET}{m}]{Fore.RESET}  Toggle Overlay  {lb}|  {Fore.RESET}{m}[{w}ins{Fore.RESET}{m}]{Fore.RESET}  Open GUI        {lb}|  {Fore.RESET}{m}[{w}f8{Fore.RESET}{m}]{Fore.RESET}{lr}   Self Destruct    {b}
"""
        )
        print("\n")
        Write.Print(
            "════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════",
            Colors.blue_to_purple,
            interval=0.000,
        )
        print("\n")

    def update_status_triggerbot():
        global triggerbotEnabled
        if triggerbotEnabled == False:
            triggerbotEnabled = True
        else:
            triggerbotEnabled = False

    def update_status_aimbot():
        global aimbotEnabled
        sys.stdout.write("\033[K")
        if Aimbot.aimbot_status == colored("ENABLED", "green"):
            Aimbot.aimbot_status = colored("DISABLED", "red")
            aimbotEnabled = False
            print(
                f"{m}[{w}!{Fore.RESET}{m}]{Fore.RESET} AIMBOT IS {Fore.RESET}{m}[{lr}DISABLED{Fore.RESET}{m}]",
                end="\r",
            )
        else:
            Aimbot.aimbot_status = colored("ENABLED", "green")
            aimbotEnabled = True
            print(
                f"{m}[{w}!{Fore.RESET}{m}]{Fore.RESET} AIMBOT IS {Fore.RESET}{m}[{lb}ENABLED{Fore.RESET}{m}]",
                end="\r",
            )

    def left_click():
        ctypes.windll.user32.mouse_event(0x0002)  # left mouse down
        Aimbot.sleep(0.000001)
        ctypes.windll.user32.mouse_event(0x0004)  # left mouse up

    def sleep(duration, get_now=time.perf_counter):
        if duration == 0:
            return
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def is_aimbot_enabled():
        return True if Aimbot.aimbot_status == colored("ENABLED", "green") else False

    def is_targeted():
        return True if win32api.GetKeyState(0x02) in (-127, -128) else False

    def is_target_locked(x, y):
        # plus/minus 5 pixel threshold
        threshold = 5
        return (
            True
            if resx / 2 - threshold <= x <= resx / 2 + threshold
            and resy / 2 - threshold <= y <= resy / 2 + threshold
            else False
        )

    def move_crosshair(self, x, y):
        if Aimbot.is_targeted():
            scale = Aimbot.sens_config["targeting_scale"]
        else:
            scale = Aimbot.sens_config["xy_scale"]
            # return #TODO

        for rel_x, rel_y in Aimbot.interpolate_coordinates_from_center(
            self, (x, y), scale
        ):
            Aimbot.ii_.mi = MouseInput(
                rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(Aimbot.extra)
            )
            input_obj = Input(ctypes.c_ulong(0), Aimbot.ii_)
            ctypes.windll.user32.SendInput(
                1, ctypes.byref(input_obj), ctypes.sizeof(input_obj)
            )
            if not self.debug: Aimbot.sleep(self.mouse_delay) #time.sleep is not accurate enough
        # if triggerbotEnabled:
        #     threading.Thread(target=Aimbot.left_click()).start()

    # generator yields pixel tuples for relative movement
    def interpolate_coordinates_from_center(self, absolute_coordinates, scale):
        diff_x = (absolute_coordinates[0] - resx / 2) * scale / self.pixel_increment
        diff_y = (absolute_coordinates[1] - resy / 2) * scale / self.pixel_increment
        length = int(math.dist((0, 0), (diff_x, diff_y)))
        if length == 0:
            return
        unit_x = (diff_x / length) * self.pixel_increment
        unit_y = (diff_y / length) * self.pixel_increment
        x = y = sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += x
            sum_y += y
            x, y = round(unit_x * k - sum_x), round(unit_y * k - sum_y)
            yield x, y

    def clean_up():
        Write.Print(
            "[INFO] F2 WAS PRESSED. QUITTING...", Colors.blue_to_purple, interval=0.000
        )
        os._exit(0)

    def start(self):
        Aimbot.update_status_aimbot()
        global started
        started = True

        half_screen_width = (
            ctypes.windll.user32.GetSystemMetrics(0) / 2
        )  # this should always be 860
        half_screen_height = (
            ctypes.windll.user32.GetSystemMetrics(1) / 2
        )  # this should always be 540

        if self.collect_data:
            collect_pause = 0
        while True:
            detection_box = {
                "left": int(
                    half_screen_width - self.box_constant // 2
                ),  # x1 coord (for top-left corner of the box)
                "top": int(
                    half_screen_height - self.box_constant // 2
                ),  # y1 coord (for top-left corner of the box)
                "width": int(self.box_constant),  # width of the box
                "height": int(self.box_constant),
            }  # height of the box
            start_time = time.perf_counter()
            frame = np.array(Aimbot.screen.grab(detection_box))
            if self.collect_data:
                orig_frame = np.copy((frame))
            results = self.model(frame)
            if len(results.xyxy[0]) != 0:  # player detected
                least_crosshair_dist = closest_detection = player_in_frame = False
                for *box, conf, cls in results.xyxy[
                    0
                ]:  # iterate over each player detected
                    x1y1 = [int(x.item()) for x in box[:2]]
                    x2y2 = [int(x.item()) for x in box[2:]]
                    x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
                    height = y2 - y1
                    relative_head_X, relative_head_Y = int((x1 + x2) / 2), int(
                        (y1 + y2) / 2 - height / 2.65
                    )  # offset to roughly approximate the head using a ratio of the height
                    own_player = x1 < 15 or (
                        x1 < self.box_constant / 5 and y2 > self.box_constant / 1.2
                    )  # helps ensure that your own player is not regarded as a valid detection

                    # calculate the distance between each detection and the crosshair at (self.box_constant/2, self.box_constant/2)
                    crosshair_dist = math.dist(
                        (relative_head_X, relative_head_Y),
                        (self.box_constant / 2, self.box_constant / 2),
                    )

                    if not least_crosshair_dist:
                        least_crosshair_dist = crosshair_dist  # initalize least crosshair distance variable first iteration

                    if crosshair_dist <= least_crosshair_dist and not own_player:
                        least_crosshair_dist = crosshair_dist
                        closest_detection = {
                            "x1y1": x1y1,
                            "x2y2": x2y2,
                            "relative_head_X": relative_head_X,
                            "relative_head_Y": relative_head_Y,
                            "conf": conf,
                        }

                    if not own_player:
                        cv2.rectangle(
                            frame, x1y1, x2y2, (244, 113, 115), 2
                        )  # draw the bounding boxes for all of the player detections (except own)
                        cv2.putText(
                            frame,
                            f"{int(conf * 100)}%",
                            x1y1,
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (244, 113, 116),
                            2,
                        )  # draw the confidence labels on the bounding boxes
                    else:
                        own_player = False
                        if not player_in_frame:
                            player_in_frame = True

                if closest_detection:  # if valid detection exists
                    cv2.circle(
                        frame,
                        (
                            closest_detection["relative_head_X"],
                            closest_detection["relative_head_Y"],
                        ),
                        5,
                        (115, 244, 113),
                        -1,
                    )  # draw circle on the head

                    # draw line from the crosshair to the head
                    cv2.line(
                        frame,
                        (
                            closest_detection["relative_head_X"],
                            closest_detection["relative_head_Y"],
                        ),
                        (self.box_constant // 2, self.box_constant // 2),
                        (244, 242, 113),
                        2,
                    )

                    absolute_head_X, absolute_head_Y = (
                        closest_detection["relative_head_X"] + detection_box["left"],
                        closest_detection["relative_head_Y"] + detection_box["top"],
                    )

                    x1, y1 = closest_detection["x1y1"]
                    if Aimbot.is_target_locked(absolute_head_X, absolute_head_Y):
                        cv2.putText(
                            frame,
                            "LOCKED",
                            (x1 + 40, y1),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (115, 244, 113),
                            2,
                        )  # draw the confidence labels on the bounding boxes
                    else:
                        cv2.putText(
                            frame,
                            "TARGETING",
                            (x1 + 40, y1),
                            cv2.FONT_HERSHEY_DUPLEX,
                            0.5,
                            (115, 113, 244),
                            2,
                        )  # draw the confidence labels on the bounding boxes

                    if Aimbot.is_aimbot_enabled():
                        Aimbot.move_crosshair(self, absolute_head_X, absolute_head_Y)

            if (
                self.collect_data
                and time.perf_counter() - collect_pause > 1
                and Aimbot.is_targeted()
                and Aimbot.is_aimbot_enabled()
                and not player_in_frame
            ):  # screenshots can only be taken every 1 second
                cv2.imwrite(f"lib/data/{str(uuid.uuid4())}.jpg", orig_frame)
                collect_pause = time.perf_counter()

            cv2.putText(
                frame,
                f"FPS: {int(1/(time.perf_counter() - start_time))}",
                (5, 30),
                cv2.FONT_HERSHEY_DUPLEX,
                1,
                (113, 116, 244),
                2,
            )
            if show:
                cv2.imshow("Hyper AIM", frame)
            if cv2.waitKey(1) & 0xFF == ord("0"):
                break


class Overlay(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        # Create the main window
        self.root = tk.Tk()

        # Set the window attributes to make it fully transparent
        self.root.config(bg="white")
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.wm_attributes("-fullscreen", "True")
        self.root.wm_attributes("-topmost", "True")
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the center of the screen
        self.center_x = screen_width // 2
        self.center_y = screen_height // 2

        # Create a canvas widget to draw the circle
        self.canvas = tk.Canvas(
            self.root,
            width=screen_width,
            height=screen_height,
            bg="#000000",
            highlightthickness=0,
        )
        hwnd = self.canvas.winfo_id()
        colorkey = win32api.RGB(0, 0, 0)  # full black in COLORREF structure
        wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
        win32gui.SetLayeredWindowAttributes(hwnd, colorkey, 255, win32con.LWA_COLORKEY)
        self.canvas.pack()

        self.circle_radius = 380 / 2

        # Start the Tkinter main loop
        self.root.mainloop()

    def hide(self):
        self.canvas.delete(self.oval)

    def show(self):
        self.oval = self.canvas.create_oval(
            self.center_x - self.circle_radius,
            self.center_y - self.circle_radius,
            self.center_x + self.circle_radius,
            self.center_y + self.circle_radius,
            outline="#5a03fc",
        )


overlay = Overlay()


def on_release(key):
    global started
    global aimbotEnabled
    try:
        if key == keyboard.KeyCode.from_char("r") and started:
            Aimbot.update_status_aimbot()
            if aimbotEnabled:
                overlay.show()
            else:
                overlay.hide()
        if key == keyboard.Key.f2:
            Aimbot.clean_up()
    except NameError:
        pass


listener = keyboard.Listener(on_release=on_release)
listener.start()

global hyper
hyper = Aimbot()
hyper.start()