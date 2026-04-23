import psutil

def cpu_stats():
    print("CPU Stats:")

    # Get the number of CPU cores
    cpu_cores = psutil.cpu_count(logical=False)
    print(f"CPU Cores: {cpu_cores}\n")

    # Get the frequency of each CPU core and its usage percentage
    for i in range(cpu_cores):
        print(f"CPU Core {i+1}:")
        print(f"\tFrequency: {psutil.cpu_freq().current:.2f} GHz")
        print(f"\tUsage: {psutil.cpu_percent(interval=1, percpu=True)[i]}%")