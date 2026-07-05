import tkinter as tk
import random

# --- مفاهیم اصلی پروژه ---
class Person:
    def __init__(self, start, end, time):
        self.start, self.end, self.entry_time = start, end, time
        self.wait_time = 0

class Elevator:
    def __init__(self):
        self.current_floor = 1
        self.passengers = []
        self.capacity = 10
        self.direction = 0 # 0: توقف، 1: بالا، -1: پایین

class Building:
    def __init__(self):
        self.elevator = Elevator()
        self.floors = [[] for _ in range(51)]
        self.total_time = 0

# --- منطق کنترلر ---
def add_request():
    try:
        s, e = int(ent_s.get()), int(ent_e.get())
        if 1 <= s <= 50 and 1 <= e <= 50 and s != e:
            b.floors[s].append(Person(s, e, b.total_time))
            update_ui()
    except: pass

def run_step():
    if btn_run["text"] == "شروع": return
    b.total_time += 1
    el = b.elevator
    
    # تخلیه و سوار کردن + محاسبه زمان انتظار
    el.passengers = [p for p in el.passengers if p.end != el.current_floor]
    while len(el.passengers) < el.capacity and b.floors[el.current_floor]:
        p = b.floors[el.current_floor].pop(0)
        p.wait_time = b.total_time - p.entry_time
        el.passengers.append(p)

    # تشخیص هوشمند جهت
    up = any(p.end > el.current_floor for p in el.passengers) or any(b.floors[i] for i in range(el.current_floor+1, 51))
    down = any(p.end < el.current_floor for p in el.passengers) or any(b.floors[i] for i in range(1, el.current_floor))

    if el.direction == 1 and not up: el.direction = -1 if down else 0
    elif el.direction == -1 and not down: el.direction = 1 if up else 0
    elif el.direction == 0: el.direction = 1 if up else (-1 if down else 0)

    el.current_floor += el.direction
    update_ui()
    root.after(600, run_step)

def update_ui():
    can.delete("all")
    h = 12 
    for i in range(1, 51):
        y = 630 - (i * h)
        can.create_line(70, y, 330, y, fill="#f0f0f0") # خطوط طبقات عریض‌تر
        can.create_text(35, y-6, text=f"Floor {i}", font=("Arial", 7))
        if b.floors[i]:
            can.create_text(360, y-6, text=f"👤{len(b.floors[i])}", fill="blue", font=("Arial", 8))

    y_el = 630 - (b.elevator.current_floor * h)
    color = "#27ae60" if b.elevator.direction == 1 else "#c0392b" if b.elevator.direction == -1 else "#7f8c8d"
    can.create_rectangle(75, y_el - 18, 325, y_el + 4, fill=color, outline="#2c3e50", width=2)
    can.create_text(200, y_el-7, text=f"ELEVATOR | {len(b.elevator.passengers)} PASSENGERS", fill="white", font=("Arial", 9, "bold"))
    
    lbl_info["text"] = f"Current Floor: {b.elevator.current_floor}\nTotal Time: {b.total_time}s\nStatus: {('UP' if b.elevator.direction==1 else 'DOWN' if b.elevator.direction==-1 else 'IDLE')}"

# --- ساختار GUI ---
b = Building()
root = tk.Tk()
root.title("Smart Elevator Simulator")
root.geometry("650x700")

f_ctrl = tk.Frame(root, padx=20, pady=20)
f_ctrl.pack(side=tk.LEFT, fill=tk.Y)

# نام دانشجو
tk.Label(f_ctrl, text="Erfan Abdi p1", font=("Arial", 14, "bold"), fg="#2980b9").pack(pady=(0, 20))

tk.Label(f_ctrl, text="Start Floor:").pack()
ent_s = tk.Entry(f_ctrl, width=12); ent_s.pack(pady=2)
tk.Label(f_ctrl, text="Dest Floor:").pack()
ent_e = tk.Entry(f_ctrl, width=12); ent_e.pack(pady=2)

tk.Button(f_ctrl, text="Add Request", command=add_request, bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=10, fill=tk.X)
tk.Button(f_ctrl, text="Random Person", command=lambda: [ent_s.delete(0, 9), ent_s.insert(0, random.randint(1,50)), ent_e.delete(0, 9), ent_e.insert(0, random.randint(1,50)), add_request()]).pack(fill=tk.X)

btn_run = tk.Button(f_ctrl, text="شروع", bg="#2ecc71", height=2, font=("Arial", 11, "bold"), command=lambda: [btn_run.config(text="در حال اجرا" if btn_run["text"]=="شروع" else "شروع"), run_step()])
btn_run.pack(pady=30, fill=tk.X)

lbl_info = tk.Label(f_ctrl, text="", justify=tk.LEFT, font=("Consolas", 10))
lbl_info.pack(side=tk.BOTTOM)

# ساختمان عریض‌تر
can = tk.Canvas(root, width=400, height=660, bg="white", relief="ridge", borderwidth=3)
can.pack(side=tk.RIGHT, padx=20, pady=15)

update_ui()
root.mainloop()
