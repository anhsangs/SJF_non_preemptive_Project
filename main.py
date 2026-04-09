import tkinter as tk
from tkinter import ttk, messagebox
from algorithms import solve_sjf, calculate_averages 
from models import Process

# --- GIAO DIỆN CHÍNH (CỬA SỔ 1) ---
class SJF_Scheduler_App:
    def __init__(self, root):
        self.root = root
        self.root.title("SJF Scheduler - Nhập liệu")
        self.root.geometry("500x600")
        
        self.input_fields = []

        # Phần nhập số tiến trình
        top_frame = ttk.Frame(root)
        top_frame.pack(pady=20, padx=20, fill="x")
        
        ttk.Label(top_frame, text="Số tiến trình:").pack(side="left")
        self.n_entry = ttk.Entry(top_frame, width=10)
        self.n_entry.pack(side="left", padx=10)
        self.n_entry.insert(0, "4")
        
        ttk.Button(top_frame, text="Tạo form nhập", command=self.create_input_fields).pack(side="left")

        # Vùng chứa các ô nhập AT và BT
        self.form_container = ttk.LabelFrame(root, text="Nhập Arrival Time (AT) và Burst Time (BT)")
        self.form_container.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Nút chạy thuật toán
        ttk.Button(root, text="🚀 Chạy thuật toán & Xem kết quả", command=self.run_algorithm).pack(pady=20)

    def create_input_fields(self):
        # Xóa các ô nhập cũ
        for widget in self.form_container.winfo_children():
            widget.destroy()
        self.input_fields.clear()

        try:
            n = int(self.n_entry.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số tiến trình hợp lệ")
            return

        # Header
        header_frame = ttk.Frame(self.form_container)
        header_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(header_frame, text="PID", width=10).pack(side="left")
        ttk.Label(header_frame, text="Arrival Time", width=15).pack(side="left")
        ttk.Label(header_frame, text="Burst Time", width=15).pack(side="left")

        # Tạo các dòng nhập liệu
        for i in range(n):
            row = ttk.Frame(self.form_container)
            row.pack(fill="x", padx=5, pady=2)
            
            pid = f"P{i+1}"
            ttk.Label(row, text=pid, width=10).pack(side="left")
            
            at_entry = ttk.Entry(row, width=12)
            at_entry.pack(side="left", padx=5)
            at_entry.insert(0, str(i*2)) # Giá trị mặc định gợi ý
            
            bt_entry = ttk.Entry(row, width=12)
            bt_entry.pack(side="left", padx=5)
            bt_entry.insert(0, "5") # Giá trị mặc định gợi ý
            
            self.input_fields.append((at_entry, bt_entry))

    def run_algorithm(self):
        try:
            procs = []
            for i, (at_e, bt_e) in enumerate(self.input_fields):
                at = int(at_e.get())
                bt = int(bt_e.get())
                procs.append(Process(f"P{i+1}", at, bt))
            
            if not procs:
                messagebox.showwarning("Cảnh báo", "Vui lòng tạo form và nhập liệu trước!")
                return

            results = solve_sjf(procs)
            self.show_results_window(results)
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ cho AT và BT!")

    # --- CỬA SỔ KẾT QUẢ (CỬA SỔ 2) ---
    def show_results_window(self, results):
        result_win = tk.Toplevel(self.root)
        result_win.title("Kết quả lập lịch SJF")
        result_win.geometry("900x700")

        # 1. Bảng kết quả (Treeview)
        cols = ("ID", "AT", "BT", "ST", "FT", "WT", "TAT")
        tree = ttk.Treeview(result_win, columns=cols, show="headings", height=8)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")
        tree.pack(padx=20, pady=10, fill="x")

        for p in results:
            tree.insert("", "end", values=(p.pid, p.at, p.bt, p.st, p.ft, p.wt, p.tat))

        # 2. Hiển thị trung bình
        avg_wt, avg_tat = calculate_averages(results)
        
        summary_frame = ttk.Frame(result_win)
        summary_frame.pack(pady=10)
        ttk.Label(summary_frame, text=f"Average Waiting Time: {avg_wt:.2f}ms", font=("Arial", 11, "bold"), foreground="#C0392B").pack(side="left", padx=20)
        ttk.Label(summary_frame, text=f"Average Turnaround Time: {avg_tat:.2f}ms", font=("Arial", 11, "bold"), foreground="#2980B9").pack(side="left", padx=20)

        # 3. Biểu đồ Gantt
        gantt_container = ttk.LabelFrame(result_win, text="Biểu đồ Gantt (Kéo ngang để xem)")
        gantt_container.pack(padx=20, pady=10, fill="both", expand=True)

        h_scroll = ttk.Scrollbar(gantt_container, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")

        canvas = tk.Canvas(gantt_container, bg="white", height=250, xscrollcommand=h_scroll.set)
        canvas.pack(side="top", fill="both", expand=True)
        h_scroll.config(command=canvas.xview)

        scale_x = 45      # Tỷ lệ thời gian
        rect_h = 60       # Chiều cao khối
        left_m = 50       # Lề trái
        top_m = 100       # Lề trên trục thời gian
        
        max_time = max(p.ft for p in results)
        canvas.config(scrollregion=(0, 0, left_m + max_time * scale_x + 100, 250))

        # Vẽ trục thời gian
        canvas.create_line(left_m, top_m, left_m + max_time * scale_x, top_m, width=2, fill="#2C3E50")
        for t in range(max_time + 1):
            x = left_m + t * scale_x
            canvas.create_line(x, top_m, x, top_m - 8, fill="#34495E")
            canvas.create_text(x, top_m - 20, text=str(t), font=("Arial", 9))

        colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F1C40F", "#9B59B6", "#1ABC9C"]

        # Vẽ các khối tiến trình
        for i, p in enumerate(results):
            color = colors[i % len(colors)]
            x_start = left_m + p.st * scale_x
            x_end = left_m + p.ft * scale_x
            
            canvas.create_rectangle(x_start, top_m + 20, x_end, top_m + 20 + rect_h, 
                                     fill=color, outline="#2C3E50", width=2)
            
            canvas.create_text(x_start + (x_end - x_start)/2, top_m + 20 + rect_h/2, 
                                text=p.pid, fill="white", font=("Arial", 11, "bold"))
            
            canvas.create_text(x_start, top_m + 20 + rect_h + 15, text=str(p.st), font=("Arial", 9, "bold"))
            canvas.create_text(x_end, top_m + 20 + rect_h + 15, text=str(p.ft), font=("Arial", 9, "bold"))

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SJF_Scheduler_App(root)
    root.mainloop()