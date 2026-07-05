import tkinter as tk
from tkinter import messagebox
import numpy as np

class ErfanAbdi_P4:
    def __init__(self, root):
        self.root = root
        self.root.title("Erfan Abdi p4 - Inverted Pendulum")
        
        # Physics Parameters
        self.m, self.M, self.L, self.g, self.dt = 0.1, 1.0, 1.0, 9.81, 0.02
        self.state = [0.0, 0.0, 0.15, 0.0] # x, x_dot, theta, theta_dot
        self.force = 0
        self.running = False
        
        # UI Setup
        self.canvas = tk.Canvas(root, bg="#f4f7f6", width=800, height=400)
        self.canvas.pack(pady=10)
        
        panel = tk.Frame(root)
        panel.pack()
        
        # Control Buttons
        for txt, f in [("◀ LEFT", -25), ("RIGHT ▶", 25)]:
            btn = tk.Button(panel, text=txt, width=12, bg="#2c3e50", fg="white")
            btn.pack(side=tk.LEFT, padx=5)
            btn.bind("<ButtonPress-1>", lambda e, v=f: self.set_f(v))
            btn.bind("<ButtonRelease-1>", lambda e: self.set_f(0))

        self.pid_on = tk.BooleanVar(value=True)
        tk.Checkbutton(root, text="PID Assist", variable=self.pid_on).pack()
        self.noise_lvl = tk.Scale(root, from_=0, to=0.2, resolution=0.01, label="Sensor Noise", orient="horizontal", length=200)
        self.noise_lvl.pack()
        
        tk.Button(root, text="START / PAUSE", command=self.toggle, bg="#27ae60", fg="white").pack(pady=5)
        tk.Label(root, text="Erfan Abdi p4", font=("Arial", 10, "bold")).pack()

        root.bind("<Left>", lambda e: self.set_f(-25)); root.bind("<Right>", lambda e: self.set_f(25))
        root.bind("<KeyRelease>", lambda e: self.set_f(0))
        self.draw()

    def set_f(self, v): self.force = v
    def toggle(self):
        self.running = not self.running
        if self.running: self.loop()

    def physics(self):
        x, x_dot, theta, theta_dot = self.state
        # Noise & Control Logic
        n = np.random.normal(0, self.noise_lvl.get())
        u = self.force + (45.0*(theta+n) + 12.0*(theta_dot+n) if self.pid_on.get() else 0)
        
        # Nonlinear Equations
        s, c = np.sin(theta), np.cos(theta)
        temp = (u + self.m * self.L * theta_dot**2 * s) / (self.M + self.m)
        t_acc = (self.g * s - c * temp) / (self.L * (4/3 - self.m * c**2 / (self.M + self.m)))
        x_acc = temp - self.m * self.L * t_acc * c / (self.M + self.m)
        
        # Integration
        self.state[1] += x_acc * self.dt
        self.state[0] += self.state[1] * self.dt
        self.state[3] += t_acc * self.dt
        self.state[2] += self.state[3] * self.dt

        # --- محدود کردن حرکت (Keep in View) ---
        if abs(self.state[0]) > 3.5:
            self.state[0] = np.sign(self.state[0]) * 3.5
            self.state[1] = 0 # متوقف کردن ارابه در لبه صفحه

    def draw(self):
        self.canvas.delete("all")
        x_p = self.state[0] * 110 + 400 # ضریب تبدیل به پیکسل
        # Draw Cart
        self.canvas.create_rectangle(x_p-25, 250-12, x_p+25, 250+12, fill="#3498db", outline="black")
        # Draw Pendulum
        px, py = x_p + np.sin(self.state[2])*140, 250 - np.cos(self.state[2])*140
        self.canvas.create_line(x_p, 250, px, py, width=4, fill="#e74c3c")
        self.canvas.create_oval(px-10, py-10, px+10, py+10, fill="#2c3e50")
        # Floor
        self.canvas.create_line(0, 262, 800, 262, fill="#7f8c8d", width=2)

    def loop(self):
        if not self.running: return
        self.physics(); self.draw()
        if abs(self.state[2]) > np.pi/2:
            self.running = False
            messagebox.showinfo("Game Over", "Pendulum fell!")
            self.state = [0.0, 0.0, 0.1, 0.0]; self.draw()
        else: self.root.after(20, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    ErfanAbdi_P4(root)
    root.mainloop()
