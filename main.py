from algorithms import solve_sjf, calculate_averages
from models import Process

# Input data
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

        # Print table
        for p in results:
            print(f"{p.pid:<5} | {p.at:<5} | {p.bt:<5} | {p.st:<5} | {p.ft:<5} | {p.wt:<5} | {p.tat:<5}")

        print("="*80)

        # Calculate averages
        avg_wt, avg_tat = calculate_averages(results)

        print(f"Average Waiting Time (AWT): {avg_wt:.2f}")
        print(f"Average Turnaround Time (ATAT): {avg_tat:.2f}")