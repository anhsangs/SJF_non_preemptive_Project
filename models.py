class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid          # Process ID
        self.at = arrival_time  # Arrival Time
        self.bt = burst_time    # Burst Time
        self.st = 0             # Start Time
        self.ft = 0             # Finish Time
        self.wt = 0             # Waiting Time
        self.tat = 0            # Turnaround Time