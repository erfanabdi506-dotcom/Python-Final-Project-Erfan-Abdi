import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy import signal


class TransferFunction:
    def __init__(self, K=1.0, zeta=0.5, wn=2.0):
        self.K = K
        self.zeta = zeta
        self.wn = wn
        self.num = []
        self.den = []
        self.update()

    def update(self):
        self.num = [self.K * self.wn ** 2]
        self.den = [1, 2 * self.zeta * self.wn, self.wn ** 2]

    def set_params(self, K, zeta, wn):
        self.K = K
        self.zeta = zeta
        self.wn = wn
        self.update()

    def get_system(self):
        return signal.TransferFunction(self.num, self.den)


class StepResponse:
    def __init__(self, transfer_function):
        self.tf = transfer_function
        self.t = None
        self.y = None
        self.rise_time = 0
        self.settling_time = 0
        self.overshoot = 0

    def calculate(self):
        system = self.tf.get_system()
        self.t, self.y = signal.step(system, T=np.linspace(0, 15, 600))
        self.calculate_info()

    def calculate_info(self):
        final_value = self.y[-1]

        if abs(final_value) < 1e-6:
            self.rise_time = 0
            self.settling_time = 0
            self.overshoot = 0
            return

        max_value = np.max(self.y)
        self.overshoot = max(0, (max_value - final_value) / abs(final_value) * 100)

        low = 0.1 * final_value
        high = 0.9 * final_value

        try:
            t10_index = np.where(self.y >= low)[0][0]
            t90_index = np.where(self.y >= high)[0][0]
            self.rise_time = self.t[t90_index] - self.t[t10_index]
        except:
            self.rise_time = 0

        error = np.abs(self.y - final_value)
        limit = 0.02 * abs(final_value)
        outside = np.where(error > limit)[0]

        if len(outside) > 0:
            last_index = outside[-1]
            self.settling_time = self.t[last_index]
        else:
            self.settling_time = 0


class Plotter:
    def __init__(self, root):
        self.fig, self.ax = plt.subplots(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def plot(self, step_response):
        self.ax.clear()

        t = step_response.t
        y = step_response.y
        final_value = y[-1]

        self.ax.plot(t, y, color="#d32f2f", linewidth=2, label="Step Response")
        self.ax.axhline(final_value, color="black", linestyle="--", alpha=0.4, label="Final Value")

        self.ax.set_title("Step Response Analysis")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Output")
        self.ax.grid(True, alpha=0.3)
        self.ax.legend()

        self.canvas.draw()


class Analyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Project 4 - Erfan Abdi")
        self.root.geometry("1200x750")
        self.root.configure(bg="#f5f5f5")

        self.tf = TransferFunction()
        self.response = StepResponse(self.tf)

        self.create_gui()
        self.plotter = Plotter(self.root)

        self.update_analysis()

    def create_gui(self):
        panel = tk.Frame(self.root, width=350, bg="white", padx=20, pady=15, relief=tk.RIDGE, borderwidth=1)
        panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(panel, text="Erfan Abdi", font=("Arial", 28, "bold"), fg="#1a237e", bg="white").pack()
        tk.Label(panel, text="Project 4: Control System Analyzer", font=("Arial", 11), fg="#546e7a", bg="white").pack(pady=(0, 15))

        input_frame = tk.LabelFrame(panel, text=" System Parameters ", bg="white", padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=10)

        self.K_var = tk.DoubleVar(value=1.0)
        self.zeta_var = tk.DoubleVar(value=0.5)
        self.wn_var = tk.DoubleVar(value=2.0)

        self.add_slider(input_frame, "Gain K", self.K_var, 0.1, 5)
        self.add_slider(input_frame, "Damping Ratio ζ", self.zeta_var, 0, 2)
        self.add_slider(input_frame, "Natural Frequency ωn", self.wn_var, 0.1, 10)

        result_frame = tk.LabelFrame(panel, text=" Results ", bg="white", padx=10, pady=10)
        result_frame.pack(fill=tk.X, pady=10)

        self.rise_label = self.add_result(result_frame, "Rise Time:")
        self.settling_label = self.add_result(result_frame, "Settling Time:")
        self.overshoot_label = self.add_result(result_frame, "Overshoot:")

        info = (
            "Transfer Function:\n"
            "G(s) = Kωn² / (s² + 2ζωn s + ωn²)"
        )

        tk.Label(panel, text=info, bg="white", fg="#333333", font=("Arial", 10), justify=tk.LEFT).pack(pady=20)

    def add_slider(self, parent, text, variable, min_value, max_value):
        tk.Label(parent, text=text, bg="white", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        ttk.Scale(
            parent,
            from_=min_value,
            to=max_value,
            variable=variable,
            command=lambda e: self.update_analysis()
        ).pack(fill=tk.X, pady=(0, 10))

    def add_result(self, parent, text):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill=tk.X, pady=3)

        tk.Label(frame, text=text, bg="white").pack(side=tk.LEFT)
        label = tk.Label(frame, text="-", bg="white", font=("Arial", 9, "bold"))
        label.pack(side=tk.RIGHT)

        return label

    def update_analysis(self):
        try:
            K = self.K_var.get()
            zeta = self.zeta_var.get()
            wn = self.wn_var.get()

            self.tf.set_params(K, zeta, wn)
            self.response.calculate()

            self.rise_label.config(text=f"{self.response.rise_time:.2f} s")
            self.settling_label.config(text=f"{self.response.settling_time:.2f} s")
            self.overshoot_label.config(text=f"{self.response.overshoot:.1f} %")

            if hasattr(self, "plotter"):
                self.plotter.plot(self.response)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = Analyzer(root)
    root.mainloop()
