
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid          # Tên tiến trình (P1, P2...)
        self.at = arrival_time  # Thời điểm đến (Arrival Time)
        self.bt = burst_time    # Thời gian chạy (Burst Time)
        self.st = 0             # Thời điểm bắt đầu (Start Time)
        self.ft = 0             # Thời điểm kết thúc (Finish Time)
        self.wt = 0             # Thời gian chờ (Waiting Time)
        self.tat = 0            # Thời gian hoàn thành (Turnaround Time)

def solve_sjf(processes):
    # Sắp xếp danh sách gốc theo thời điểm đến (AT)
    processes.sort(key=lambda x: x.at)
    
    ready_queue = []
    finished_processes = []
    current_time = 0
    
    # Copy danh sách để không làm hỏng dữ liệu gốc
    temp_processes = processes[:]

    while temp_processes or ready_queue:
        # 1. Đưa tất cả các tiến trình đã đến (AT <= current_time) vào hàng đợi sẵn sàng
        while temp_processes and temp_processes[0].at <= current_time:
            ready_queue.append(temp_processes.pop(0))
        
        # Trường hợp hàng đợi rảnh (CPU rảnh)
        if not ready_queue:
            current_time = temp_processes[0].at
            continue
            
        # 2. Thuật toán SJF: Chọn tiến trình có Burst Time (BT) ngắn nhất trong Ready Queue
        ready_queue.sort(key=lambda x: x.bt)
        
        # 3. Lấy tiến trình đó ra chạy (Lưu ý: Non-preemptive nên chạy hết BT)
        p = ready_queue.pop(0)
        p.st = current_time
        p.ft = p.st + p.bt
        p.tat = p.ft - p.at
        p.wt = p.tat - p.bt
        
        # Cập nhật thời gian hệ thống sau khi chạy xong
        current_time = p.ft
        finished_processes.append(p)
        
    return finished_processes

# TEST THỬ CODE CỦA BẠN
if __name__ == "__main__":
    # Tạo thử 3 tiến trình mẫu
    data = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1)
    ]
    
    results = solve_sjf(data)
    
    print(f"{'ID':<5} | {'AT':<5} | {'BT':<5} | {'ST':<5} | {'FT':<5} | {'WT':<5} | {'TAT':<5}")
    for p in results:
        print(f"{p.pid:<5} | {p.at:<5} | {p.bt:<5} | {p.st:<5} | {p.ft:<5} | {p.wt:<5} | {p.tat:<5}")