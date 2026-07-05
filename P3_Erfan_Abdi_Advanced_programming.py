import tkinter as tk

# --- کلاس‌های اصلی پروژه ---
class Tank:
    def __init__(self, capacity=250):
        self.capacity = capacity
        self.level = 0.0

class Pump:
    def __init__(self, flow_rate=15):
        self.flow_rate = flow_rate
        self.is_on = False

class Sensor:
    def get_level(self, tank): return tank.level

class Controller:
    def __init__(self):
        self.integral = 0
        self.last_error = 0

    def on_off(self, current, setpoint, hys=5):
        if current < setpoint - hys: return True
        if current > setpoint + hys: return False
        return None

    def pid(self, current, setpoint):
        kp, ki, kd = 0.8, 0.05, 0.1
        err = setpoint - current
        self.integral = max(-50, min(self.integral + err, 50))
        der = err - self.last_error
        self.last_error = err
        return (kp * err + ki * self.integral + kd * der) > 0

# --- منطق اصلی و GUI ---
def run_simulation():
    if not running: return
    
    current_level = sensor.get_level(tank)
    setpoint = setpoint_slider.get()
    
    if control_mode.get() == "On-Off":
        res = controller.on_off(current_level, setpoint)
        if res is not None: pump.is_on = res
    elif control_mode.get() == "PID":
        pump.is_on = controller.pid(current_level, setpoint)

    inflow = pump.flow_rate if pump.is_on else 0
    tank.level += (inflow - outflow_slider.get()) * 0.1
    tank.level = max(0, min(tank.level, tank.capacity))

    update_ui()
    root.after(100, run_simulation)

def update_ui():
    can.delete("all")
    sp = setpoint_slider.get()
    
    # --- رسم مخزن بزرگتر ---
    # مختصات: چپ: 50, بالا: 50, راست: 200, پایین: 400
    can.create_rectangle(60, 50, 210, 400, outline="black", width=3)
    for i in range(0, 251, 50):
        y = 400 - (i / 250) * 350
        can.create_text(35, y, text=str(i), font=("Arial", 10, "bold"))
        can.create_line(50, y, 60, y, width=2)
    
    # آب داخل مخزن
    h = (tank.level / 250) * 350
    can.create_rectangle(63, 400-h, 207, 398, fill="#3498db", outline="")
    
    # خط ست‌پوینت روی مخزن و نمودار
    sp_y_tank = 400 - (sp / 250) * 350
    can.create_line(50, sp_y_tank, 220, sp_y_tank, fill="red", dash=(6,4), width=2)
    can.create_text(240, sp_y_tank, text="TARGET", fill="red", font=("Arial", 10, "bold"))

    # --- رسم نمودار بزرگتر ---
    # محورها
    can.create_line(300, 400, 750, 400, arrow=tk.LAST, width=2) # محور زمان (X)
    can.create_line(300, 400, 300, 50, arrow=tk.LAST, width=2)  # محور سطح (Y)
    
    # خط ست‌پوینت روی نمودار
    sp_y_graph = 400 - (sp / 250) * 340
    can.create_line(300, sp_y_graph, 740, sp_y_graph, fill="red", dash=(2,2))

    for i in range(0, 251, 50):
        y_g = 400 - (i / 250) * 340
        can.create_text(280, y_g, text=str(i), font=("Arial", 9))

    history.append(tank.level)
    if len(history) > 110: history.pop(0)
    for i in range(1, len(history)):
        x1, y1 = 300 + (i-1)*4, 400 - (history[i-1]/250)*340
        x2, y2 = 300 + i*4, 400 - (history[i]/250)*340
        can.create_line(x1, y1, x2, y2, fill="blue", width=3)

def start():
    global running; running = True; run_simulation()

# --- تنظیمات اولیه ---
tank = Tank(); pump = Pump(); sensor = Sensor(); controller = Controller()
running = False; history = []

root = tk.Tk(); root.title("Project 3 - Erfan Abdi"); root.geometry("1100x550")

# پنل کنترل سمت چپ
pnl = tk.Frame(root, padx=30)
pnl.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(pnl, text="Erfan Abdi\np3", font=("Arial", 32, "bold"), fg="darkblue").pack(pady=30)

tk.Label(pnl, text="CONTROL MODE:", font=("Arial", 10, "bold")).pack()
control_mode = tk.StringVar(value="Manual")
tk.OptionMenu(pnl, control_mode, "Manual", "On-Off", "PID").pack(pady=5)

tk.Label(pnl, text="SETPOINT (LITERS):", font=("Arial", 10, "bold")).pack(pady=(15,0))
setpoint_slider = tk.Scale(pnl, from_=0, to=250, orient=tk.HORIZONTAL, length=200)
setpoint_slider.set(125); setpoint_slider.pack()

tk.Label(pnl, text="OUTFLOW RATE:", font=("Arial", 10, "bold")).pack(pady=(15,0))
outflow_slider = tk.Scale(pnl, from_=0, to=15, orient=tk.HORIZONTAL, length=200)
outflow_slider.set(5); outflow_slider.pack()

tk.Button(pnl, text="PUMP ON", bg="#e0e0e0", height=2, command=lambda: setattr(pump, 'is_on', True) if control_mode.get()=="Manual" else None).pack(fill=tk.X, pady=5)
tk.Button(pnl, text="PUMP OFF", bg="#e0e0e0", height=2, command=lambda: setattr(pump, 'is_on', False) if control_mode.get()=="Manual" else None).pack(fill=tk.X, pady=5)
tk.Button(pnl, text="START SIMULATION", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), height=2, command=start).pack(fill=tk.X, pady=20)

lbl_stat = tk.Label(pnl, text="", font=("Arial", 14, "bold"))
lbl_stat.pack()

# بوم گرافیکی بزرگ در سمت راست
can = tk.Canvas(root, width=800, height=500, bg="white", highlightthickness=2, highlightbackground="#bdc3c7")
can.pack(side=tk.RIGHT, padx=30, pady=20)

update_ui()
root.mainloop()
