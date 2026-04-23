import psutil
import time

def get_overview():
    # We will list the top 10 processes with most CPU usage
    processes = []

    # There is a problem when we call proc.cpu_percent() for the first time, 
    # it returns 0.0 because it calculates the percentage since the last call. 
    # To get accurate CPU usage, we need to call it once for all processes, wait a bit, 
    # and then call it again to get the actual CPU usage.
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(None)
        except:
            pass

    # Now we will wait for 1 second to allow the CPU usage to be calculated
    time.sleep(1)

    # At this point, we can call proc.cpu_percent() again to get the actual 
    # CPU usage for each process
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            if proc.info['cpu_percent'] is not None:
                processes.append(proc.info)
        except:
            continue

    # Sort processes by CPU usage in descending order and take the top 10
    processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
    
    # Print the top 10 processes with their PID, name, and CPU usage
    for proc in processes[:10]:
        print(f"PID: {proc['pid']}, Name: {proc['name']}, CPU usage: {proc['cpu_percent']}%")