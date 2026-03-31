
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

# TEST
if __name__ == "__main__":
    data = [
        Process("P1", 0, 7),
        Process("P2", 0, 4),
        Process("P3", 4, 1)
    ]
    
    results = solve_sjf(data)
    
    print(f"{'ID':<5} | {'Arrival Time':<5} | {'Burst Time':<5} | {'Start Time':<5} | {'Finish Time':<5} | {'Waiting Time':<5} | {'Turnaround Time':<5}")
    for p in results:
        print(f"{p.pid:<5} | {p.at:<12} | {p.bt:<10} | {p.st:<10} | {p.ft:<11} | {p.wt:<12} | {p.tat:<5}")