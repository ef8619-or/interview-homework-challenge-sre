# Challenge 2: System information scripting

I decided not to put all the code into one single file and instead modularize it a bit for better readability. So all of the needed modules reside in the */modules* directory and will be imported in the `main.py`

## Requirements

We will use a Python module named `psutil`. Unfortunately, it is not included in the Python standard library, so we need to install it using the Python package manager `pip`. Furthermore we will a virtual environment (venv) to isolate project dependencies, avoid conflicts with global packages, and ensure reproducibility.

To meet those requirements we have to execute the following commands:

```sh
python3 -m venv venv
source venv/bin/activate
pip install psutil
```

## Command line options
The application needs to receive input values from the user so we are going to import the `argparse` module into our main.py. Then we add some arguments and parse them with if-else statements. Regarding the parsed argument we call the appropriate functions. If there is none or no suitable option for the inputted argument the user will be displayed some helpful information on how to use the application.

## __init__.py

We use the `__init__.py` file to mark the modules directory as a Python package ensuring that modules can be imported.

## disk.py

We import the `psutil` modul. Normally there are multiple partitions available on a computer so we iterate over all of them. Inside the for-loop we will use a try-exception block as there can be partitions which may not be accessible by our application, so we need to make sure it doesn't break. With the help of `psutil.disk_usage(partition.mountpoint)` we can get all the information we need for a specific partition. 

For reasons of better readability we need to multiple the result of each usage metric with factor 1024 to the power of 3 so we get Gigabytes.

## cpu.py

Again we import the `psutil` module. Then we need to count the CPU cores - we only count the physical ones as Python can not distinct between physical and logical on our OS. After we have the number of CPU cores we iterate over each of them and print the number, frequency and usage.

## ports.py

Instead of importing the psutil module we need to use the `subprocess` module for this. This gives us the possibility to run `lsof` with parameters where `-i` filters for Internet sockets, `-P` gives us the ports as numbers instead of names and `-n` prevents DNS resolution so we get the IPs. The output of the `lsof` function is then saved in the result variable.

Finally we iterate over the all of the entries saved in result (therefore we need to split the lines first). Because we only want to print the interesting parts we use the `split()` function twice to get the last two segments of each line.

## ram.py

The `psutil` module need to be imported in the first step. After that we can simply call the `virtual_memory()` function in psutil and print the desired information. As we want the values to be more readable we need to multiple by 1024 to the power of 3 to get Gigabytes.

## overview.py

Besides the import of the `psutil` module we also need to import the `time` module. 

The goal of this module is to list the top 10 processes with the highest CPU usage. Therefore we first create an empty list where we will store the process information.

There is a small issue when working with `psutil.cpu_percent()`. When calling this function for the first time it always returns 0.0 because it calculates the CPU usage based on the time since the last call. To solve this we first iterate over all processes and call cpu_percent(None) once just to initialize the calculation.

After that we wait for one second using `time.sleep(1)` so that psutil has enough time to calculate the actual CPU usage.

Now we iterate over all processes again, this time including additional information like pid, name and cpu_percent. Inside a try-exception block we make sure that inaccessible processes do not break the application. All valid process information will be stored in our list.

Finally we sort the list by CPU usage in descending order and print the top 10 processes including their PID, name and CPU usage.