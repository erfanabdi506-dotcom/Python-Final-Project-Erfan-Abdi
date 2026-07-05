import tkinter as tk
import random

class Card:
    def __init__(self, balance=10): self.balance = balance
    def pay(self, fare=3):
        if self.balance >= fare:
            self.balance -= fare
            return True
        return False

class Passenger:
    def __init__(self, name="Passenger"):
        self.name = name
        self.card = Card(random.randint(0, 15))
        self.inside = False

class Sensor:
    def __init__(self): self.detected = False
    def read(self, passenger):
        self.detected = passenger is not None
        return self.detected

class Motor:
    def __init__(self): self.state = "closed"
    def open_gate(self): self.state = "open"
    def close_gate(self): self.state = "closed"

class Gate:
    def __init__(self):
        self.sensor = Sensor()
        self.motor = Motor()
        self.current_passenger = None
        self.fare = 3
    def insert_passenger(self, passenger):
        self.current_passenger = passenger
        self.sensor.read(passenger)
    def check_card(self):
        if not self.current_passenger: return False, "No passenger"
        p = self.current_passenger
        if p.card.pay(self.fare):
            self.motor.open_gate()
            return True, f"Access granted: {p.name} can pass"
        self.motor.close_gate()
        return False, f"Access denied: {p.name} has insufficient balance"
    def finish_passing(self):
        if self.current_passenger: self.current_passenger.inside = not self.current_passenger.inside
        self.current_passenger = None
        self.sensor.read(None)
        self.motor.close_gate()
    def reset(self):
        self.current_passenger = None
        self.sensor.read(None)
        self.motor.close_gate()

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project 6 - Metro Gate Simulator")
        self.root.geometry("700x450")
        self.root.configure(bg="#f0f4f8")
        self.gate = Gate()
        self.passenger_count = 0
        self.passenger_x = 150
        self.animating = False
        tk.Label(root, text="Metro Gate Simulator", font=("Arial", 20, "bold"), bg="#f0f4f8", fg="#1a237e").pack(pady=10)
        self.canvas = tk.Canvas(root, width=620, height=180, bg="white", highlightthickness=1, highlightbackground="#ccc")
        self.canvas.pack(pady=10)
        btn_frame = tk.Frame(root, bg="#f0f4f8")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add Passenger", width=15, command=self.add_passenger, bg="#1976d2", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Process Gate", width=15, command=self.process_gate, bg="#2e7d32", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", width=15, command=self.reset_gate, bg="#c62828", fg="white").pack(side=tk.LEFT, padx=5)
        self.info = tk.Label(root, text="Ready", font=("Arial", 11), bg="#f0f4f8", fg="#333")
        self.info.pack(pady=10)
        self.card_info = tk.Label(root, text="", font=("Arial", 10), bg="#f0f4f8", fg="#555")
        self.card_info.pack()
        self.draw()

    def add_passenger(self):
        if self.animating: return
        self.passenger_count += 1
        p = Passenger(f"P{self.passenger_count}")
        self.gate.insert_passenger(p)
        self.passenger_x = 150
        self.info.config(text=f"{p.name} arrived at gate")
        self.card_info.config(text=f"Card Balance: {p.card.balance} | Inside: {p.inside}")
        self.draw()

    def process_gate(self):
        if self.animating: return
        ok, result = self.gate.check_card()
        self.info.config(text=result)
        if self.gate.current_passenger:
            p = self.gate.current_passenger
            self.card_info.config(text=f"{p.name} | Balance: {p.card.balance} | Inside: {p.inside}")
        self.draw()
        if ok:
            self.animating = True
            self.root.after(300, self.animate_passenger)

    def animate_passenger(self):
        if not self.gate.current_passenger:
            self.animating = False
            return
        self.passenger_x += 8
        self.draw()
        if self.passenger_x < 500: self.root.after(30, self.animate_passenger)
        else:
            p = self.gate.current_passenger
            self.gate.finish_passing()
            self.animating = False
            self.info.config(text=f"{p.name} passed successfully. Gate closed.")
            self.card_info.config(text="")
            self.draw()

    def reset_gate(self):
        if self.animating: return
        self.gate.reset()
        self.passenger_x = 150
        self.info.config(text="Gate reset")
        self.card_info.config(text="")
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.canvas.create_line(20, 140, 600, 140, fill="#666", width=2)
        self.canvas.create_rectangle(260, 40, 360, 140, outline="#333", width=3)
        if self.gate.motor.state == "open":
            self.canvas.create_line(270, 60, 270, 130, fill="green", width=6)
            self.canvas.create_line(350, 60, 350, 130, fill="green", width=6)
            self.canvas.create_text(310, 25, text="GATE OPEN", fill="green", font=("Arial", 12, "bold"))
        else:
            self.canvas.create_line(310, 60, 310, 130, fill="red", width=8)
            self.canvas.create_text(310, 25, text="GATE CLOSED", fill="red", font=("Arial", 12, "bold"))
        sensor_color = "#4caf50" if self.gate.sensor.detected else "#ffd54f"
        self.canvas.create_oval(290, 95, 330, 125, fill=sensor_color, outline="#333")
        self.canvas.create_text(310, 110, text="SENSOR", font=("Arial", 8, "bold"))
        if self.gate.current_passenger:
            x = self.passenger_x
            self.canvas.create_oval(x - 20, 80, x + 20, 120, fill="#64b5f6", outline="black")
            self.canvas.create_text(x, 130, text=self.gate.current_passenger.name, font=("Arial", 10, "bold"))
            self.canvas.create_rectangle(x + 25, 90, x + 55, 110, fill="#ffeb3b", outline="black")
            self.canvas.create_text(x + 40, 100, text="CARD", font=("Arial", 7, "bold"))
        else: self.canvas.create_text(150, 100, text="No Passenger", font=("Arial", 11, "italic"), fill="#888")

if __name__ == "__main__":
    root = tk.Tk(); app = GUI(root); root.mainloop()
