import subprocess

def ports_stats():
    print("Listening ports:\n")

    # Use subprocess to run the lsof command with option -i to get the list of open files 
    # and their associated network connections. To get a better overwiew of the ports, 
    # we can also use options -P to display port numbers and -n to avoid resolving hostnames.
    result = subprocess.run(
        ["lsof", "-i", "-P", "-n"],
        capture_output = True,
        text = True
    )

    # We iterate through the result of lsof and print only the lines that contain "LISTEN", 
    # which indicates that the port is open and listening for incoming connections.
    for line in result.stdout.splitlines():
        if "LISTEN" in line:
            # We will only print the number of the listening port
            port = line.split()[-2].split(":")[-1]
            print(port)