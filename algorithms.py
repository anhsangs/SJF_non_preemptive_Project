from models import Process

# Algorithm to calculate averages
def calculate_averages(processes):
    total_wt = 0
    total_tat = 0

    for p in processes:
        total_wt += p.wt
        total_tat += p.tat

    avg_wt = total_wt / len(processes)
    avg_tat = total_tat / len(processes)

    return avg_wt, avg_tat


# Algorithm SJF Non-preemptive
def solve_sjf(processes):
    # Sắp xếp theo Arrival Time ban đầu
    processes.sort(key=lambda x: x.at)
    
    ready_queue = []
    finished_processes = []
    current_time = 0
    temp_processes = processes[:]

    while temp_processes or ready_queue:
        # 1. Đưa tất cả các tiến trình đã đến vào hàng đợi sẵn sàng
        while temp_processes and temp_processes[0].at <= current_time:
            ready_queue.append(temp_processes.pop(0))

        # 2. Xử lý trường hợp CPU nhàn rỗi (không có tiến trình nào trong queue)
        if not ready_queue:
            current_time = temp_processes[0].at
            continue

        # 3. Chọn tiến trình ngắn nhất (SJF). Nếu bằng BT, ưu tiên AT, rồi đến PID
        ready_queue.sort(key=lambda x: (x.bt, x.at, x.pid))
        p = ready_queue.pop(0)

        # 4. Tính toán các mốc thời gian
        p.st = current_time
        p.ft = p.st + p.bt
        p.tat = p.ft - p.at
        p.wt = p.tat - p.bt

        current_time = p.ft
        finished_processes.append(p)

    return finished_processes

