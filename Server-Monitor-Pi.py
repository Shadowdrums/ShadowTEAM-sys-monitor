import os
import psutil
from rich.console import Console
from rich.table import Table
import time

# Function to read CPU temperature from the system file
def get_cpu_temperature():
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
            temp = float(file.read()) / 1000.0
            return temp
    except FileNotFoundError:
        return None

# Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def get_cpu_info():
    try:
        cpu_info = os.popen("lscpu | grep 'Model name'").read().strip().split(":")[1].strip()
        return cpu_info
    except Exception as e:
        print(f"Error getting CPU information: {e}")
        return "N/A"

def get_main_storage_usage():
    try:
        main_storage = psutil.disk_usage('/')
        total_storage_gb = round(main_storage.total / (1024.0 ** 3), 2)
        used_storage_gb = round(main_storage.used / (1024.0 ** 3), 2)
        free_storage_gb = round(main_storage.free / (1024.0 ** 3), 2)
        used_storage_percent = main_storage.percent
        return total_storage_gb, used_storage_gb, free_storage_gb, used_storage_percent
    except Exception as e:
        print(f"Error getting main storage usage: {e}")
        return 0, 0, 0, 0

def get_network_usage():
    try:
        network_info = psutil.net_io_counters()
        sent_mb = round(network_info.bytes_sent / (1024.0 ** 2), 2)
        recv_mb = round(network_info.bytes_recv / (1024.0 ** 2), 2)
        return sent_mb, recv_mb
    except Exception as e:
        print(f"Error getting network usage: {e}")
        return 0, 0

def get_active_users():
    try:
        active_users = [user.name for user in psutil.users()]
        return active_users
    except Exception as e:
        print(f"Error getting active users: {e}")
        return []

def get_usage():
    try:
        cpu_percent = psutil.cpu_percent(percpu=True)
        ram_percent = psutil.virtual_memory().percent
        total_ram = round(psutil.virtual_memory().total / (1024.0 ** 3), 2)
        cpu_temp_celsius = get_cpu_temperature()
        cpu_temp_fahrenheit = celsius_to_fahrenheit(cpu_temp_celsius) if cpu_temp_celsius is not None else None
        total_storage_gb, used_storage_gb, free_storage_gb, used_storage_percent = get_main_storage_usage()
        sent_mb, recv_mb = get_network_usage()
        active_users = get_active_users()
        return cpu_percent, ram_percent, total_ram, cpu_temp_celsius, cpu_temp_fahrenheit, total_storage_gb, used_storage_gb, free_storage_gb, used_storage_percent, sent_mb, recv_mb, active_users
    except Exception as e:
        print(f"Error getting system usage: {e}")
        return [], 0, 0, None, None, 0, 0, 0, 0, 0, 0, []

def render_live_graph(console):
    while True:
        # Clear the console
        console.clear()

        # Display the system information
        display_system_info(console)

        # Display the live graph
        display_live_graph(console)

        # Sleep for a short duration (adjust as needed)
        time.sleep(1)

def display_system_info(console):
    cpu_model = get_cpu_info()
    console.print(f"{'CPU Model':<25}: {cpu_model}")

def display_live_graph(console):
    # Create a new table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", justify="left")
    table.add_column("Info", justify="left")
    table.add_column("Usage", justify="left")
    table.add_column("Graph", justify="left")

    # Add rows to the table dynamically based on live data
    cpu_percent, ram_percent, total_ram, cpu_temp_celsius, cpu_temp_fahrenheit, total_storage_gb, used_storage_gb, free_storage_gb, used_storage_percent, sent_mb, recv_mb, active_users = get_usage()

    table.add_row("Cores", "", "4", "")
    table.add_row("Overall CPU Usage", f"{cpu_percent[0]:.2f}%", f"[{'█' * int(cpu_percent[0] / 5)}{' ' * (20 - int(cpu_percent[0] / 5))}]", "")
    for i in range(1, 5):
        table.add_row(f"Core {i}", f"{cpu_percent[i-1]:.2f}%", f"[{'█' * int(cpu_percent[i-1] / 5)}{' ' * (20 - int(cpu_percent[i-1] / 5))}]", "")

    table.add_row("Total RAM", "", f"{total_ram} GB", "")
    table.add_row("Used RAM", f"{ram_percent:.2f}%", f"[{'█' * int(ram_percent / 5)}{' ' * (20 - int(ram_percent / 5))}]", "")

    if cpu_temp_celsius is not None:
        table.add_row("CPU Temperature", f"{cpu_temp_celsius:.1f}°C / {cpu_temp_fahrenheit:.1f}°F", f"{'█' * int(cpu_temp_celsius / 5)}{' ' * (20 - int(cpu_temp_celsius / 5))}", "")
    else:
        table.add_row("CPU Temperature", "N/A", "", "")

    table.add_row("Main Storage Usage", f"{used_storage_percent:.2f}%", f"[{'█' * int(used_storage_percent / 5)}{' ' * (20 - int(used_storage_percent / 5))}]", "")
    table.add_row("Total Storage", "", f"{total_storage_gb} GB", "")
    table.add_row("Used Storage", "", f"{used_storage_gb} GB", "")
    table.add_row("Available Storage", "", f"{free_storage_gb} GB", "")
    table.add_row("Network Sent", f"{sent_mb:.2f} MB", "", "")
    table.add_row("Network Received", f"{recv_mb:.2f} MB", "", "")
    table.add_row("Active Users", ", ".join(active_users), "", "")

    # Print the table
    console.print(table)

def main():
    console = Console()
    render_live_graph(console)

if __name__ == "__main__":
    main()
