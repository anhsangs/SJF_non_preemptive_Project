
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid          # Name Pr
        self.at = arrival_time  # Arrival Time
        self.bt = burst_time    # Burst Time
        self.st = 0             # Start Time
        self.ft = 0             # Finish Time
        self.wt = 0             # Waiting Time
        self.tat = 0            # Turnaround Time

def solve_sjf(processes):
    # Sort the list by arrival time (AT)
    processes.sort(key=lambda x: x.at)
    ready_queue = []
    finished_processes = []
    current_time = 0
    temp_processes = processes[:]

    while temp_processes or ready_queue:
        # Add all arrived processes (AT <= current_time) to the ready queue
        while temp_processes and temp_processes[0].at <= current_time:
            ready_queue.append(temp_processes.pop(0))
        
        # In case the queue is empty (CPU is idle)
        if not ready_queue:
            current_time = temp_processes[0].at
            continue
            
        # Select the process with the shortest Burst Time (BT) from the Ready Queue
        ready_queue.sort(key=lambda x: (x.bt, x.at))
        
        # Execute the selected process
        p = ready_queue.pop(0)
        p.st = current_time
        p.ft = p.st + p.bt
        p.tat = p.ft - p.at
        p.wt = p.tat - p.bt
        
        # Update the system time after the process finishes execution
        current_time = p.ft
        finished_processes.append(p)
        
    return finished_processes

def input_processes():
    processes = []
    try:
        n = int(input("Number of processes: "))
        for i in range(n):
            auto_pid = f"P{i+1}"
            print(f"\nProcess ID: {auto_pid} ")
            at = int(input(f"Arrival Time: "))
            bt = int(input(f"Burst Time: "))
            processes.append(Process(auto_pid, at, bt))
        return processes
    except ValueError:
        print("Error: Please enter integers only for AT and BT!")
        return []

# --- Main Process ---
if __name__ == "__main__":
    print("Algorithm SJF (Shortest Job First) ")
    
    data = input_processes()
    
    if data:
        results = solve_sjf(data)
        
        print("\n" + "="*80)
        print(f"{'ID':<5} | {'AT':<5} | {'BT':<5} | {'ST':<5} | {'FT':<5} | {'WT':<5} | {'TAT':<5}")
        print("-" * 80)
        
        for p in results:
            print(f"{p.pid:<5} | {p.at:<5} | {p.bt:<5} | {p.st:<5} | {p.ft:<5} | {p.wt:<5} | {p.tat:<5}")
        
        print("="*80)
  