import psutil

def disk_stats():
    print("Disk Stats:")

    # As there can be multiple disk partitions, we loop through each one and print its stats
    # We use try-except to handle any potential permission errors when accessing certain partitions
    for partition in psutil.disk_partitions():
        try:
            print(f"Volume: {partition.mountpoint}")
            
            # Get the disk usage statistics for the current partition
            # We convert the total, used, and free space from bytes to gigabytes by raising the numbers
            # to the power of 3 (1024^3 = 1 GB)
            disk_usage = psutil.disk_usage(partition.mountpoint)
            total_usage = disk_usage.total / (1024 ** 3)
            used_usage = disk_usage.used / (1024 ** 3)
            free_usage = disk_usage.free / (1024 ** 3)
            percent_usage = disk_usage.percent

            print(f"  Total: {total_usage:.2f} GB")
            print(f"  Used: {used_usage:.2f} GB")
            print(f"  Free: {free_usage:.2f} GB")
            print(f"  Usage: {percent_usage:.2f}%")
        except PermissionError:
            print(f"Cannot read stats, permission denied for volume: {partition.mountpoint}")
