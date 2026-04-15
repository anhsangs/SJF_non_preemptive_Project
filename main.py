import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.widgets.scrolled import ScrolledFrame
from ttkbootstrap.constants import *
from algorithms import solve_sjf, calculate_averages 
from models import Process

# --- MAIN INTERFACE ---
class SJF_Scheduler_App:
    def __init__(self, root):
        self.root = root
        self.root.title(" CPU Scheduling: SJF Non-Preemptive ")
        self.root.geometry("700x850")
        
        self.input_fields = []

        # App Header
        header_frame = tb.Frame(root)
        header_frame.pack(fill="x", pady=(30, 20), padx=30)
        tb.Label(header_frame, text="SHORTEST JOB FIRST (SJF)", font=("Segoe UI Black", 28, "bold"), bootstyle="warning").pack(anchor="w")
        tb.Label(header_frame, text="Non-Preemptive Process Scheduling Analysis", font=("Segoe UI", 12), bootstyle="light").pack(anchor="w", pady=(5,0))

        # Input Toolbar
        toolbar = tb.Frame(root)
        toolbar.pack(fill="x", padx=30, pady=15)
        
        tb.Label(toolbar, text="Number of Processes:", font=("Segoe UI", 12, "bold"), bootstyle="light").pack(side="left", padx=(0, 10))
        
        self.n_entry = tb.Entry(toolbar, width=8, font=("Segoe UI", 12), justify="center")
        self.n_entry.pack(side="left", padx=10)
        
        btn_create = tb.Button(toolbar, text="INITIALIZE DATA", command=self.create_input_fields, bootstyle="primary", padding=(15, 8))
        btn_create.pack(side="left", padx=15)

        self.card_frame = tb.Frame(root)
        self.card_frame.pack(pady=10, padx=30, fill="both", expand=True)
        
        self.scroll_frame = ScrolledFrame(self.card_frame, autohide=True)
        self.scroll_frame.pack(fill="both", expand=True)

        # Main Action Button 
        self.btn_run = tb.Button(root, text=" RUN ALGORITHM", command=self.run_algorithm, bootstyle="success", padding=(0, 15))
        self.btn_run.pack(pady=30, padx=30, fill="x")

    def create_input_fields(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.input_fields.clear()

        try:
            n = int(self.n_entry.get())
            if n <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive integer!")
            return

        table_container = tb.Labelframe(self.scroll_frame, text=" PROCESS PARAMETERS ", bootstyle="info")
        table_container.pack(fill="x", padx=10, pady=10, ipadx=10, ipady=10)

        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_columnconfigure(1, weight=2)
        table_container.grid_columnconfigure(2, weight=2)

        tb.Label(table_container, text="PID", font=("Segoe UI", 12, "bold"), bootstyle="light").grid(row=0, column=0, pady=(0, 15))
        tb.Label(table_container, text="Arrival Time (ms)", font=("Segoe UI", 12, "bold"), bootstyle="light").grid(row=0, column=1, pady=(0, 15))
        tb.Label(table_container, text="Burst Time (ms)", font=("Segoe UI", 12, "bold"), bootstyle="light").grid(row=0, column=2, pady=(0, 15))

        for i in range(n):
            pid_label = tb.Label(table_container, text=f"P{i+1}", font=("Segoe UI", 14, "bold"), bootstyle="info")
            pid_label.grid(row=i+1, column=0, pady=8)
            
            at_entry = tb.Entry(table_container, font=("Segoe UI", 11), justify="center")
            at_entry.grid(row=i+1, column=1, padx=20, pady=8, sticky="ew")
            
            bt_entry = tb.Entry(table_container, font=("Segoe UI", 11), justify="center")
            bt_entry.grid(row=i+1, column=2, padx=20, pady=8, sticky="ew")
            
            self.input_fields.append((at_entry, bt_entry))

    def run_algorithm(self):
        try:
            procs = []
            for i, (at_e, bt_e) in enumerate(self.input_fields):
                at_val, bt_val = at_e.get().strip(), bt_e.get().strip()
                if not at_val or not bt_val:
                    messagebox.showerror("Missing Data", f"Please provide full details for P{i+1}")
                    return
                procs.append(Process(f"P{i+1}", int(at_val), int(bt_val)))
            
            if not procs: 
                messagebox.showwarning("Warning", "Please generate the form and input data first!")
                return
                
            results = solve_sjf(procs)
            self.show_results_window(results)
            
        except ValueError:
            messagebox.showerror("Type Error", "Arrival Time and Burst Time must be integers!")

    # --- RESULTS WINDOW ---
    def show_results_window(self, results):
        res_win = tb.Toplevel(self.root)
        res_win.title("SJF Analysis Report")
        res_win.geometry("1050x850")

        master_scroll = ScrolledFrame(res_win, autohide=True)
        master_scroll.pack(fill="both", expand=True, padx=40, pady=30)

        tb.Label(master_scroll, text="PERFORMANCE ANALYTICS", font=("Segoe UI Black", 22, "bold"), bootstyle="warning").pack(anchor="w", pady=(0, 15))

        table_container = tb.Frame(master_scroll)
        table_container.pack(fill="x", pady=(0, 20))
        
        table_frame = tb.Frame(table_container)
        table_frame.pack(fill="x", expand=True)

        cols = ("ID", "ARRIVAL TIME", "BURST TIME", "START TIME", "FINISH TIME", "WAITING TIME", "TURNAROUND TIME")
        col_width = 12 

        for j, col in enumerate(cols):
            tb.Label(table_frame, text=col, font=("Segoe UI", 10, "bold"), 
                     bootstyle="inverse-primary", borderwidth=1, relief="solid", 
                     padding=6, anchor="center", width=col_width).grid(row=0, column=j, sticky="nsew")

        for i, p in enumerate(results):
            bg_color = "#2b3e50" if i % 2 == 0 else "#3a4f63"
            values = (p.pid, p.at, p.bt, p.st, p.ft, p.wt, p.tat)
            for j, val in enumerate(values):
                tb.Label(table_frame, text=str(val), font=("Segoe UI", 11), 
                         background=bg_color, foreground="white", 
                         borderwidth=1, relief="solid", padding=6, 
                         anchor="center", width=col_width).grid(row=i+1, column=j, sticky="nsew")

        avg_wt, avg_tat = calculate_averages(results)
        score_frame = tb.Frame(master_scroll)
        score_frame.pack(fill="x", pady=10)

        card1 = tb.Frame(score_frame, bootstyle="danger")
        card1.pack(side="left", fill="x", expand=True, padx=(0, 15), ipady=5)
        tb.Label(card1, text="Average Waiting Time", font=("Segoe UI", 10, "bold"), bootstyle="inverse-danger").pack(pady=(5,0))
        tb.Label(card1, text=f"{avg_wt:.2f} ms", font=("Segoe UI Black", 16), bootstyle="inverse-danger").pack()

        card2 = tb.Frame(score_frame, bootstyle="info")
        card2.pack(side="left", fill="x", expand=True, padx=(15, 0), ipady=5)
        tb.Label(card2, text="Average Turnaround Time", font=("Segoe UI", 10, "bold"), bootstyle="inverse-info").pack(pady=(5,0))
        tb.Label(card2, text=f"{avg_tat:.2f} ms", font=("Segoe UI Black", 16), bootstyle="inverse-info").pack()

        # GANTT CHART
        gantt_container = tb.Labelframe(master_scroll, text=" GANTT CHART (Multi-Lane Timeline) ", bootstyle="light")
        gantt_container.pack(fill="both", expand=True, pady=(25, 0))

        h_scroll = tb.Scrollbar(gantt_container, orient="horizontal", bootstyle="warning-round")
        h_scroll.pack(side="bottom", fill="x")

        # Calculate Dynamic Height based 
        row_spacing = 100
        top_m = 40
        canvas_h = top_m + len(results) * row_spacing + 20

        canvas = tk.Canvas(gantt_container, bg="#2b3e50", height=canvas_h, highlightthickness=0, xscrollcommand=h_scroll.set)
        canvas.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        h_scroll.config(command=canvas.xview)

        scale_x = 50 
        rect_h = 40 
        left_m = 70 
        
        max_time = max(p.ft for p in results)
        canvas.config(scrollregion=(0, 0, left_m + max_time * scale_x + 80, canvas_h))

        canvas.create_line(left_m, top_m, left_m + max_time * scale_x, top_m, width=2, fill="#df691a")
        for t in range(max_time + 1):
            x = left_m + t * scale_x
            canvas.create_line(x, top_m, x, top_m - 8, fill="#df691a")
            canvas.create_text(x, top_m - 20, text=str(t), font=("Segoe UI", 9, "bold"), fill="white")

        colors = ["#FF3366", "#00CFFF", "#00E676", "#FFEA00", "#B338FF", "#FF9100", "#1DE9B6", "#F50057"]

        for i, p in enumerate(results):
            color = colors[i % len(colors)]
            row_y = top_m + 20 + i * row_spacing
            
            x_at = left_m + p.at * scale_x
            x_st = left_m + p.st * scale_x
            x_ft = left_m + p.ft * scale_x
            
            canvas.create_text(left_m - 35, row_y + rect_h/2, text=p.pid, fill="white", font=("Segoe UI Black", 14))
            
            if p.wt > 0:
                canvas.create_rectangle(x_at, row_y, x_st, row_y + rect_h, fill="#6c757d", outline="#8899a6")
                
                line_y = row_y + rect_h + 20
                canvas.create_line(x_at, line_y, x_st, line_y, fill="#8899a6", width=2)
                canvas.create_line(x_at, line_y - 6, x_at, line_y + 6, fill="#8899a6", width=2) # Left tick
                canvas.create_line(x_st, line_y - 6, x_st, line_y + 6, fill="#8899a6", width=2) # Right tick
                
                canvas.create_text((x_at + x_st)/2, line_y + 12, text="waiting time", fill="#8899a6", font=("Segoe UI", 9, "italic"))
                
                canvas.create_text(x_at, row_y + rect_h + 8, text="at", fill="#8899a6", font=("Segoe UI", 10, "bold"))
                canvas.create_text(x_st, row_y + rect_h + 8, text="st", fill="#8899a6", font=("Segoe UI", 10, "bold"))
            else:
                canvas.create_text(x_st, row_y + rect_h + 8, text="st", fill="#8899a6", font=("Segoe UI", 10, "bold"))

            canvas.create_rectangle(x_st, row_y, x_ft, row_y + rect_h, fill=color, outline=color)
            canvas.create_text(x_st + (x_ft - x_st)/2, row_y + rect_h/2, text=p.pid, fill="#2b3e50", font=("Segoe UI Black", 12))
            
            canvas.create_text(x_ft, row_y + rect_h + 8, text="ft", fill="#8899a6", font=("Segoe UI", 10, "bold"))

if __name__ == "__main__":
    root = tb.Window(themename="superhero") 
    app = SJF_Scheduler_App(root)
    root.mainloop()

