import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

DATA_FILE = 'pomodoro_data.json'

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Pomodoro App')
        self.pomodoro_minutes = 25
        self.time_left = self.pomodoro_minutes * 60
        self.timer_running = False
        self.pomodoros_today = 0
        self.history = []
        self.load_data()
        self.create_widgets()
        self.update_timer_label()
        self.update_calendar()
        self.update_history()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack()

        self.timer_label = ttk.Label(frame, text='', font=('Arial', 36))
        self.timer_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.start_btn = ttk.Button(frame, text='Iniciar', command=self.start_timer)
        self.start_btn.grid(row=1, column=0, padx=5)
        self.pause_btn = ttk.Button(frame, text='Pausar', command=self.pause_timer)
        self.pause_btn.grid(row=1, column=1, padx=5)
        self.reset_btn = ttk.Button(frame, text='Reiniciar', command=self.reset_timer)
        self.reset_btn.grid(row=1, column=2, padx=5)

        ttk.Label(frame, text='Duración (min):').grid(row=2, column=0, pady=10)
        self.duration_var = tk.IntVar(value=self.pomodoro_minutes)
        self.duration_spin = ttk.Spinbox(frame, from_=1, to=120, textvariable=self.duration_var, width=5, command=self.set_duration)
        self.duration_spin.grid(row=2, column=1)
        self.set_btn = ttk.Button(frame, text='Establecer', command=self.set_duration)
        self.set_btn.grid(row=2, column=2)

        ttk.Label(frame, text='Pomodoros hoy:').grid(row=3, column=0, pady=10)
        self.today_label = ttk.Label(frame, text=str(self.pomodoros_today))
        self.today_label.grid(row=3, column=1)

        ttk.Label(frame, text='Calendario:').grid(row=4, column=0, pady=10)
        self.calendar_text = tk.Text(frame, width=20, height=7, state='disabled')
        self.calendar_text.grid(row=5, column=0, columnspan=3)

        ttk.Label(frame, text='Historial:').grid(row=6, column=0, pady=10)
        self.history_text = tk.Text(frame, width=30, height=7, state='disabled')
        self.history_text.grid(row=7, column=0, columnspan=3)

    def update_timer_label(self):
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.config(text=f'{mins:02}:{secs:02}')

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.countdown()

    def pause_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.time_left = self.pomodoro_minutes * 60
        self.update_timer_label()

    def set_duration(self):
        self.pomodoro_minutes = self.duration_var.get()
        self.reset_timer()

    def countdown(self):
        if self.timer_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer_label()
            self.root.after(1000, self.countdown)
        elif self.timer_running and self.time_left == 0:
            self.timer_running = False
            self.pomodoros_today += 1
            self.add_to_history()
            self.save_data()
            self.update_calendar()
            self.update_history()
            self.today_label.config(text=str(self.pomodoros_today))
            messagebox.showinfo('Pomodoro', '¡Pomodoro terminado!')
            self.reset_timer()

    def add_to_history(self):
        now = datetime.now()
        entry = now.strftime('%Y-%m-%d %H:%M:%S')
        self.history.append(entry)

    def update_calendar(self):
        today = datetime.now().strftime('%Y-%m-%d')
        calendar = {}
        for entry in self.history:
            date = entry.split()[0]
            calendar[date] = calendar.get(date, 0) + 1
        self.pomodoros_today = calendar.get(today, 0)
        self.today_label.config(text=str(self.pomodoros_today))
        self.calendar_text.config(state='normal')
        self.calendar_text.delete('1.0', tk.END)
        for date, count in sorted(calendar.items()):
            self.calendar_text.insert(tk.END, f'{date}: {count} pomodoros\n')
        self.calendar_text.config(state='disabled')

    def update_history(self):
        self.history_text.config(state='normal')
        self.history_text.delete('1.0', tk.END)
        for entry in reversed(self.history[-20:]):
            self.history_text.insert(tk.END, f'{entry}\n')
        self.history_text.config(state='disabled')

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                self.history = data.get('history', [])
        else:
            self.history = []

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump({'history': self.history}, f)

def main():
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
