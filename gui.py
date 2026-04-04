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
        self.root.geometry("1300x850")
        
        self.input_fields = []

        # Tiêu đề
        tk.Label(root, text="Thuật toán SJF Non-preemptive", 
                 font=("Arial", 20, "bold"), fg="#2C3E50").pack(pady=15)

        # Frame điều khiển phía trên
        top_frame = ttk.Frame(root)
        top_frame.pack(pady=10, padx=30, fill="x")
        
        ttk.Label(top_frame, text="Số tiến trình (1-10):", font=("Arial", 11)).pack(side="left")
        self.n_entry = ttk.Entry(top_frame, width=8, font=("Arial", 11))
        self.n_entry.pack(side="left", padx=10)
        self.n_entry.insert(0, "4")
        
        ttk.Button(top_frame, text="Tạo form nhập", command=self.create_inputs).pack(side="left", padx=5)
        ttk.Button(root, text="🚀 CHẠY SJF & VẼ GANTT CHART", command=self.run_algorithm).pack(pady=10)

        # Container cho phần nhập liệu chi tiết
        self.form_container = ttk.LabelFrame(root, text="Nhập chi tiết tiến trình")
        self.form_container.pack(padx=30, pady=5, fill="x")

        # Bảng kết quả tính toán
        res_frame = ttk.LabelFrame(root, text="Kết quả tính toán chi tiết")
        res_frame.pack(padx=30, pady=10, fill="x")
        
        cols = ("ID", "AT", "BT", "ST", "FT", "WT", "TAT")
        self.tree = ttk.Treeview(res_frame, columns=cols, show="headings", height=5)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="x")

        # Thêm vào dưới bảng kết quả Treeview
        self.summary_frame = ttk.Frame(root)
        self.summary_frame.pack(pady=5, padx=30, fill="x")
        
        self.label_awt = ttk.Label(self.summary_frame, text="Average Waiting Time: --", font=("Arial", 11, "bold"))
        self.label_awt.pack(side="left", padx=20)
        
        self.label_atat = ttk.Label(self.summary_frame, text="Average Turnaround Time: --", font=("Arial", 11, "bold"))
        self.label_atat.pack(side="left", padx=20)
        # KHU VỰC GANTT CHART CÓ THANH CUỘN
        gantt_frame = ttk.LabelFrame(root, text="Biểu đồ Gantt Chart (Cuộn để xem hết)")
        gantt_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Tạo thanh cuộn ngang và dọc
        self.canvas_frame = ttk.Frame(gantt_frame)
        self.canvas_frame.pack(fill="both", expand=True)

        self.v_scroll = ttk.Scrollbar(self.canvas_frame, orient="vertical")
        self.v_scroll.pack(side="right", fill="y")
        
        self.h_scroll = ttk.Scrollbar(gantt_frame, orient="horizontal")
        self.h_scroll.pack(side="bottom", fill="x")

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", 
                                xscrollcommand=self.h_scroll.set,
                                yscrollcommand=self.v_scroll.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        # Tạo mặc định
        self.create_inputs()

    def create_inputs(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()
        self.input_fields.clear()

        try:
            n = int(self.n_entry.get())
            if n < 1: n = 1
            if n > 10: n = 10
        except: return

        # Header hàng nhập
        header = ttk.Frame(self.form_container)
        header.pack(fill="x", padx=10, pady=5)
        ttk.Label(header, text="Process ID", width=15, font=("Arial", 9, "bold")).pack(side="left")
        ttk.Label(header, text="Arrival Time (AT)", width=20, font=("Arial", 9, "bold")).pack(side="left")
        ttk.Label(header, text="Burst Time (BT)", width=20, font=("Arial", 9, "bold")).pack(side="left")

        for i in range(n):
            row = ttk.Frame(self.form_container)
            row.pack(fill="x", padx=10, pady=2)
            pid = f"P{i+1}"
            ttk.Label(row, text=pid, width=15).pack(side="left")
            
            at_e = ttk.Entry(row, width=15)
            at_e.insert(0, str(i*2)) # Mặc định 0, 2, 4, 6...
            at_e.pack(side="left", padx=15)
            
            bt_e = ttk.Entry(row, width=15)
            bt_e.insert(0, "5") # Mặc định 5
            bt_e.pack(side="left", padx=5)
            
            self.input_fields.append((pid, at_e, bt_e))

    def run_algorithm(self):
        try:
            # Thu thập dữ liệu từ các ô nhập liệu
            procs = [Process(pid, int(at.get()), int(bt.get())) for pid, at, bt in self.input_fields]
            
            # Chạy thuật toán SJF (từ algorithms.py)
            results = solve_sjf(procs) 
            
            # 1. Cập nhật bảng Treeview
            for item in self.tree.get_children(): 
                self.tree.delete(item)
            for p in results:
                self.tree.insert("", "end", values=(p.pid, p.at, p.bt, p.st, p.ft, p.wt, p.tat))
            
            # 2. Tính toán và hiển thị trung bình lên Summary Frame
            avg_wt, avg_tat = calculate_averages(results)
            
            # Cập nhật nội dung cho các Label đã tạo trong __init__
            self.label_awt.config(text=f"Average Waiting Time: {avg_wt:.2f}", foreground="#E74C3C")
            self.label_atat.config(text=f"Average Turnaround Time: {avg_tat:.2f}", foreground="#2980B9")
            
            # 3. Vẽ Gantt Chart đa tầng
            self.draw_gantt(results)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
    def draw_gantt(self, processes):
        """Vẽ Gantt Chart chuẩn - Mỗi process một hàng riêng, thẳng hàng, dễ nhìn"""
        self.canvas.delete("all")
        if not processes:
            return

        scale_x = 42                    # 1 đơn vị thời gian = 42 pixel
        rect_h = 58                     # chiều cao thanh
        gap_y = 52                      # khoảng cách giữa các hàng
        left_margin = 130
        top_margin = 90

        max_time = max(p.ft for p in processes) + 4
        total_width = left_margin + max_time * scale_x + 180
        total_height = top_margin + len(processes) * (rect_h + gap_y) + 100

        self.canvas.config(scrollregion=(0, 0, total_width, total_height))

        # Tiêu đề Gantt Chart
        self.canvas.create_text(left_margin - 30, 45, 
                               text="GANTT CHART - SJF Non-preemptive", 
                               font=("Arial", 15, "bold"), anchor="w", fill="#2C3E50")

        # Trục thời gian (X-axis)
        self.canvas.create_line(left_margin, top_margin - 15, 
                               left_margin + max_time * scale_x, top_margin - 15, 
                               width=3, fill="#2C3E50")

        # Các mốc thời gian
        for t in range(0, max_time + 1, max(1, max_time // 12)):
            x = left_margin + t * scale_x
            self.canvas.create_line(x, top_margin - 22, x, top_margin - 8)
            self.canvas.create_text(x, top_margin - 35, text=str(t), font=("Arial", 9))

        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]

        y = top_margin

        for i, p in enumerate(processes):
            color = colors[i % len(colors)]
            
            x_start = left_margin + p.st * scale_x
            width = (p.ft - p.st) * scale_x

            # Vẽ thanh tiến trình
            self.canvas.create_rectangle(x_start, y, x_start + width, y + rect_h,
                                        fill=color, outline="#2C3E50", width=3)

            # Tên process ở giữa thanh
            self.canvas.create_text(x_start + width/2, y + rect_h/2,
                                   text=p.pid, font=("Arial", 13, "bold"), fill="white")

            # Nhãn process bên trái (rất quan trọng)
            self.canvas.create_text(left_margin - 65, y + rect_h/2,
                                   text=p.pid, font=("Arial", 12, "bold"), anchor="e")

            # Thời gian bắt đầu và kết thúc
            self.canvas.create_text(x_start, y + rect_h + 18, text=str(p.st),
                                   font=("Arial", 9), anchor="n")
            self.canvas.create_text(x_start + width, y + rect_h + 18, text=str(p.ft),
                                   font=("Arial", 9), anchor="n")

            y += rect_h + gap_y
if __name__ == "__main__":
    root = tk.Tk()
    app = SJF_GUI(root)
    root.mainloop()