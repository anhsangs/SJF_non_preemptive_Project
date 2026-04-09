class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid          # Process ID
        self.at = at            # Arrival Time
        self.bt = bt            # Burst Time
        self.st = 0             # Start Time
        self.ft = 0             # Finish Time
        self.wt = 0             # Waiting Time
        self.tat = 0            # Turnaround Time