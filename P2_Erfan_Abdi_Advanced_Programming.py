import tkinter as tk
import random

class Car:
    def __init__(self, direction):
        self.direction = direction

class TrafficLight:
    def __init__(self):
        self.color = "red"
        self.timer = 0

class Lane:
    def __init__(self, name):
        self.name = name
        self.cars = []
        self.light = TrafficLight()

class Intersection:
    def __init__(self):
        self.lanes = {"شمال": Lane("شمال"), "جنوب": Lane("جنوب"), 
                      "شرق": Lane("شرق"), "غرب": Lane("غرب")}
        self.axis = "NS" 
        self.passed_count = 0

class Controller:
    def __init__(self, inter):
        self.inter = inter

    def update(self):
        ns_q = len(self.inter.lanes["شمال"].cars) + len(self.inter.lanes["جنوب"].cars)
        ew_q = len(self.inter.lanes["شرق"].cars) + len(self.inter.lanes["غرب"].cars)

        for name, lane in self.inter.lanes.items():
            if lane.light.timer > 0:
                lane.light.timer -= 1
            else:
                if self.inter.axis == "NS":
                    if name in ["شمال", "جنوب"]:
                        lane.light.color = "green"
                        lane.light.timer = 7 + (ns_q // 2)
                    else: lane.light.color = "red"
                else:
                    if name in ["شرق", "غرب"]:
                        lane.light.color = "green"
                        lane.light.timer = 7 + (ew_q // 2)
                    else: lane.light.color = "red"

        if self.inter.lanes["شمال"].light.timer == 0 and self.inter.lanes["شرق"].light.timer == 0:
            self.inter.axis = "EW" if self.inter.axis == "NS" else "NS"

# --- بخش گرافیک و مدیریت دکمه‌ها ---
def add_car(direct):
    inter.lanes[direct].cars.append(Car(direct))
    update_ui()

def add_random():
    d = random.choice(["شمال", "جنوب", "شرق", "غرب"])
    add_car(d)

def step():
    if btn_run["text"] == "شروع": return
    controller.update()
    for name, lane in inter.lanes.items():
        if lane.light.color == "green" and lane.cars:
            lane.cars.pop(0) # عبور ماشین
            inter.passed_count += 1
    update_ui()
    root.after(800, step) # سرعت شبیه‌سازی

def update_ui():
    can.delete("all")
    # رسم جاده‌ها
    can.create_rectangle(160, 0, 240, 400, fill="#34495e", outline="") # جاده عمودی
    can.create_rectangle(0, 160, 400, 240, fill="#34495e", outline="") # جاده افقی
    
    pos = {"شمال":(200,130), "جنوب":(200,270), "شرق":(270,200), "غرب":(130,200)}
    for name, p in pos.items():
        lane = inter.lanes[name]
        c = "green" if lane.light.color == "green" else "red"
        can.create_oval(p[0]-12, p[1]-12, p[0]+12, p[1]+12, fill=c, outline="white")
        can.create_text(p[0], p[1]+22, text=f"{lane.light.timer}s", font=("Arial", 9, "bold"))
        # نمایش خودروها به صورت مستطیل‌های کوچک
        for i in range(len(lane.cars)):
            dist = (i+1)*18
            if name=="شمال": can.create_rectangle(192, 110-dist, 208, 100-dist, fill="yellow")
            if name=="جنوب": can.create_rectangle(192, 290+dist, 208, 300+dist, fill="yellow")
            if name=="شرق": can.create_rectangle(290+dist, 192, 300+dist, 208, fill="yellow")
            if name=="غرب": can.create_rectangle(110-dist, 192, 100-dist, 208, fill="yellow")

    lbl_info["text"] = f"خودروهای عبوری: {inter.passed_count}\nمحور فعال فعلی: {inter.axis}"

# --- تنظیمات رابط کاربری ---
inter = Intersection(); controller = Controller(inter)
root = tk.Tk(); root.title("Traffic Controller"); root.geometry("650x480")

f_ctrl = tk.Frame(root, padx=15, pady=10)
f_ctrl.pack(side=tk.LEFT, fill=tk.Y)

# نام در بالای پنل
tk.Label(f_ctrl, text="Erfan Abdi p2", font=("Arial", 14, "bold"), fg="#d35400").pack(pady=(0,15))

# دکمه‌های انتخاب جهت
tk.Label(f_ctrl, text="ورود خودرو از سمت:", font=("Arial", 10)).pack()
btn_f = tk.Frame(f_ctrl)
btn_f.pack(pady=5)
tk.Button(btn_f, text="شمال", width=6, command=lambda: add_car("شمال")).grid(row=0, column=1)
tk.Button(btn_f, text="غرب", width=6, command=lambda: add_car("غرب")).grid(row=1, column=0)
tk.Button(btn_f, text="شرق", width=6, command=lambda: add_car("شرق")).grid(row=1, column=2)
tk.Button(btn_f, text="جنوب", width=6, command=lambda: add_car("جنوب")).grid(row=2, column=1)

tk.Button(f_ctrl, text="خودرو تصادفی", bg="#ecf0f1", command=add_random, width=18).pack(pady=10)

btn_run = tk.Button(f_ctrl, text="شروع", bg="#2ecc71", font=("Arial", 11, "bold"), 
                    command=lambda: [btn_run.config(text="در حال اجرا" if btn_run["text"]=="شروع" else "شروع"), step()], width=16)
btn_run.pack(pady=15)

lbl_info = tk.Label(f_ctrl, text="", justify=tk.LEFT, font=("Tahoma", 9))
lbl_info.pack(side=tk.BOTTOM, pady=10)

can = tk.Canvas(root, width=400, height=400, bg="#ecf0f1", relief="ridge", borderwidth=2)
can.pack(side=tk.RIGHT, padx=15, pady=15)

update_ui()
root.mainloop()
