class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid          # Process ID
        self.at = arrival_time  # Arrival Time
        self.bt = burst_time    # Burst Time
        self.st = 0             # Start Time
        self.ft = 0             # Finish Time
        self.wt = 0             # Waiting Time
        self.tat = 0            # Turnaround Time


# Hàm tính trung bình
def calculate_averages(processes):
    total_wt = 0
    total_tat = 0

    for p in processes:
        total_wt += p.wt
        total_tat += p.tat

    avg_wt = total_wt / len(processes)
    avg_tat = total_tat / len(processes)

    return avg_wt, avg_tat


# Thuật toán SJF Non-preemptive
def solve_sjf(processes):
    processes.sort(key=lambda x: x.at)

    ready_queue = []
    finished_processes = []
    current_time = 0
    temp_processes = processes[:]

    while temp_processes or ready_queue:

        # Đưa process đã đến vào hàng đợi
        while temp_processes and temp_processes[0].at <= current_time:
            ready_queue.append(temp_processes.pop(0))

        # Nếu CPU rảnh
        if not ready_queue:
            current_time = temp_processes[0].at
            continue

        # Chọn process có Burst Time nhỏ nhất
        ready_queue.sort(key=lambda x: (x.bt, x.at, x.pid))

        p = ready_queue.pop(0)

        # Nếu CPU rảnh trước khi process đến
        if current_time < p.at:
            current_time = p.at

        # Tính thời gian
        p.st = current_time
        p.ft = p.st + p.bt
        p.tat = p.ft - p.at
        p.wt = p.tat - p.bt

        current_time = p.ft
        finished_processes.append(p)

    return finished_processes


# Nhập dữ liệu
def input_processes():
    processes = []

    try:
        n = int(input("Number of processes: "))

        for i in range(n):
            pid = f"P{i+1}"

            print(f"\nProcess ID: {pid}")

            at = int(input("Arrival Time: "))
            bt = int(input("Burst Time: "))

            processes.append(Process(pid, at, bt))

        return processes

    except ValueError:
        print("Error: Please enter integers only!")
        return []


# --- Main ---
if __name__ == "__main__":

    print("Algorithm SJF (Shortest Job First)")

    data = input_processes()

    if data:

        results = solve_sjf(data)

        print("\n" + "="*80)
        print(f"{'ID':<5} | {'AT':<5} | {'BT':<5} | {'ST':<5} | {'FT':<5} | {'WT':<5} | {'TAT':<5}")
        print("-" * 80)

        # In bảng
        for p in results:
            print(f"{p.pid:<5} | {p.at:<5} | {p.bt:<5} | {p.st:<5} | {p.ft:<5} | {p.wt:<5} | {p.tat:<5}")

        print("="*80)

        # Tính trung bình
        avg_wt, avg_tat = calculate_averages(results)

        print(f"Average Waiting Time (AWT): {avg_wt:.2f}")
        print(f"Average Turnaround Time (ATAT): {avg_tat:.2f}")