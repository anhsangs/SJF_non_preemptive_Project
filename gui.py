import tkinter as tk
from tkinter import ttk, messagebox
from algorithms import solve_sjf, calculate_averages
# --- LỚP DỮ LIỆU TIẾN TRÌNH ---
class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid
        self.at = at
        self.bt = bt
        self.st = 0
        self.ft = 0
        self.wt = 0
        self.tat = 0

# --- THUẬT TOÁN SJF NON-PREEMPTIVE ---
def solve_sjf_non_preemptive(processes):
    n = len(processes)
    ready_pool = sorted(processes, key=lambda x: x.at)
    completed = []
    current_time = 0

    while len(completed) < n:
        # Lấy các tiến trình đã đến
        available = [p for p in ready_pool if p.at <= current_time]
        
        if not available:
            # Nếu chưa có cái nào đến, nhảy thời gian đến cái gần nhất
            current_time = ready_pool[0].at
            continue
        
        # Chọn tiến trình có Burst Time nhỏ nhất
        current_p = min(available, key=lambda x: x.bt)
        
        current_p.st = current_time
        current_p.ft = current_p.st + current_p.bt
        current_p.tat = current_p.ft - current_p.at
        current_p.wt = current_p.tat - current_p.bt
        
        current_time = current_p.ft
        completed.append(current_p)
        ready_pool.remove(current_p)
        
    return completed

# --- GIAO DIỆN CHÍNH ---
class SJF_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SJF Scheduler - Gantt Chart Pro")
        self.root.geometry("900x600")
        
        self.input_fields = []

        # Tiêu đề
        tk.Label(root, text="Thuật toán SJF Non-preemptive", 
                 font=("Arial", 20, "bold"), fg="#2C3E50").pack(pady=15)

        # Frame điều khiển phía trên
        top_frame = ttk.Frame(root)
        top_frame.pack(pady=10)
        
        ttk.Label(top_frame, text="Số tiến trình (1-10):" ).pack(side="left")
        self.n_entry = ttk.Entry(top_frame, width=8,)
        self.n_entry.pack(side="left", padx=10)
        self.n_entry.insert(0, "4")
        
        ttk.Button(top_frame, text="Tạo form nhập", command=self.create_inputs).pack(side="left", padx=5)
        ttk.Button(root, text="🚀 Run", command=self.run_algorithm).pack(pady=5)
        ttk.Button(root, text="🧹 Clear", command=self.clear_table).pack(pady=5)
        ttk.Button(root, text="🎲 Random", command=self.random_data).pack(pady=5)
        # Container cho phần nhập liệu chi tiết
        self.form_container = ttk.LabelFrame(root, text="Nhập chi tiết tiến trình")
        self.form_container.pack(padx=20, pady=10, fill="x")

       self.create_inputs()

    def create_inputs(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()
        self.input_fields.clear()

        try:
            n = int(self.n_entry.get())
            if n < 1: n = 1
            if n > 10: n = 10
        except:
            return

        header = ttk.Frame(self.form_container)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(header, text="Process ID", width=15).pack(side="left")
        ttk.Label(header, text="Arrival Time (AT)", width=20).pack(side="left")
        ttk.Label(header, text="Burst Time (BT)", width=20).pack(side="left")

        for i in range(n):
            row = ttk.Frame(self.form_container)
            row.pack(fill="x", padx=10, pady=2)
            pid = f"P{i+1}"
            ttk.Label(row, text=pid, width=15).pack(side="left")

            at_e = ttk.Entry(row, width=15)
            at_e.insert(0, str(i*2))
            at_e.pack(side="left", padx=15)

            bt_e = ttk.Entry(row, width=15)
            bt_e.insert(0, "5")
            bt_e.pack(side="left", padx=5)

            self.input_fields.append((pid, at_e, bt_e))

    def run_algorithm(self):
        try:
            procs = [Process(pid, int(at.get()), int(bt.get())) for pid, at, bt in self.input_fields]
            results = solve_sjf_non_preemptive(procs)

            avg_wt = sum(p.wt for p in results) / len(results)
            avg_tat = sum(p.tat for p in results) / len(results)

            # Mở cửa sổ kết quả
            result_win = tk.Toplevel(self.root)
            result_win.title("Kết quả SJF")
            result_win.geometry("800x600")

            cols = ("ID", "AT", "BT", "ST", "FT", "WT", "TAT")
            tree = ttk.Treeview(result_win, columns=cols, show="headings", height=8)
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=80, anchor="center")
            tree.pack(padx=10, pady=10, fill="x")

            for p in results:
                tree.insert("", "end", values=(p.pid, p.at, p.bt, p.st, p.ft, p.wt, p.tat))

            ttk.Label(result_win, text=f"Average Waiting Time: {avg_wt:.2f}",
                      font=("Arial", 12, "bold")).pack(pady=5)
            ttk.Label(result_win, text=f"Average Turnaround Time: {avg_tat:.2f}",
                      font=("Arial", 12, "bold")).pack(pady=5)

            # Vẽ Gantt Chart trên cùng một dòng
            canvas = tk.Canvas(result_win, bg="white", height=200)
            canvas.pack(fill="x", padx=10, pady=10)

            scale_x = 50
            rect_h = 50
            left_margin = 50
            y = 80
            colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]

            for i, p in enumerate(results):
                color = colors[i % len(colors)]
                x_start = left_margin + p.st * scale_x
                width = (p.ft - p.st) * scale_x

                canvas.create_rectangle(x_start, y, x_start + width, y + rect_h,
                                        fill=color, outline="black")
                canvas.create_text(x_start + width/2, y + rect_h/2,
                                   text=p.pid, fill="white", font=("Arial", 12, "bold"))
                canvas.create_text(x_start, y + rect_h + 20, text=str(p.st))
                canvas.create_text(x_start + width, y + rect_h + 20, text=str(p.ft))

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ cho AT và BT!")

    def clear_table(self):
        clear_win = tk.Toplevel(self.root)
        clear_win.title("Clear")
        ttk.Label(clear_win, text="Form đã được xóa!", font=("Arial", 12)).pack(pady=20)
        for widget in self.form_container.winfo_children():
            widget.destroy()
        self.input_fields.clear()

    def random_data(self):
        for pid, at_entry, bt_entry in self.input_fields:
            at_entry.delete(0, tk.END)
            bt_entry.delete(0, tk.END)
            at_entry.insert(0, random.randint(0, 10))
            bt_entry.insert(0, random.randint(1, 10))

        rand_win = tk.Toplevel(self.root)
        rand_win.title("Random Data")
        ttk.Label(rand_win, text="Dữ liệu ngẫu nhiên đã được tạo!",
                  font=("Arial", 12)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SJF_GUI(root)
    root.mainloop()

    root = tk.Tk()
    app = SJF_GUI(root)
    root.mainloop()
