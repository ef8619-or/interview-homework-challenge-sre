import psutil

def ram_stats():
    # Get the virtual memory statistics
    ram = psutil.virtual_memory()

    # Print the RAM statistics
    print("RAM Statistics:\n")
    print(f"Total RAM: {ram.total / (1024 ** 3):.2f} GB")
    print(f"Available RAM: {ram.available / (1024 ** 3):.2f} GB")
    print(f"Used RAM: {ram.used / (1024 ** 3):.2f} GB")
    print(f"RAM Usage: {ram.percent}%")