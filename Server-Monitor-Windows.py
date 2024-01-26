import os
import psutil
from rich.console import Console
from rich.table import Table
import wmi
import time

def get_cpu_info():
    try:
        cpu_info = os.popen("wmic cpu get caption").read().strip().split("\n")[1].strip()
        core_count = psutil.cpu_count(logical=False)
        return f"{cpu_info} (Cores: {core_count})"
    except Exception as e:
        print(f"Error getting CPU information: {e}")
        return "N/A"

def get_gpu_info():
    try:
        gpu_info = os.popen("nvidia-smi --query-gpu=name --format=csv,noheader").read().strip()
        return gpu_info
    except Exception as e:
        print(f"Error getting GPU information: {e}")
        return "N/A"

def get_gpu_usage():
    try:
        gpu_usage = os.popen("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits").read().strip()
        return float(gpu_usage)
    except Exception as e:
        print(f"Error getting GPU usage: {e}")
        return 0.0

def get_cpu_temperature():
    try:
        w = wmi.WMI(namespace="root\OpenHardwareMonitor")
        temperature_infos = w.Sensor()
        for sensor in temperature_infos:
            if sensor.SensorType == "Temperature" and "cpu" in sensor.Name.lower():
                return float(sensor.Value)
        return None  # temperature not found
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
        return None

def get_gpu_temperature():
    try:
        gpu_temperature = os.popen("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits").read().strip()
        return float(gpu_temperature)
    except Exception as e:
        print(f"Error getting GPU temperature: {e}")
        return None

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def get_storage_info():
    try:
        partitions = psutil.disk_partitions(all=True)  # Include all partitions including network drives
        storage_info = []
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            total_gb = round(usage.total / (1024.0 ** 3), 2)
            used_gb = round(usage.used / (1024.0 ** 3), 2)
            free_gb = round(usage.free / (1024.0 ** 3), 2)
            used_percent = usage.percent
            storage_info.append((partition.device, partition.device.split(":")[0], total_gb, used_gb, free_gb, used_percent))
        return storage_info
    except Exception as e:
        print(f"Error getting storage information: {e}")
        return []

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
        gpu_percent = get_gpu_usage()
        total_ram = round(psutil.virtual_memory().total / (1024.0 ** 3), 2)
        cpu_temp_celsius = get_cpu_temperature()
        gpu_temp_celsius = get_gpu_temperature()
        storage_info = get_storage_info()
        sent_mb, recv_mb = get_network_usage()
        active_users = get_active_users()
        return cpu_percent, ram_percent, gpu_percent, total_ram, cpu_temp_celsius, gpu_temp_celsius, storage_info, sent_mb, recv_mb, active_users
    except Exception as e:
        print(f"Error getting system usage: {e}")
        return [], 0, 0, 0, None, None, [], 0, 0, []

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
    gpu_model = get_gpu_info()
    console.print(f"{'CPU Model':<25}: {cpu_model}")
    console.print(f"{'GPU Model':<25}: {gpu_model}")

def display_live_graph(console):
    # Create a new table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", justify="left")
    table.add_column("Info", justify="left")
    table.add_column("Usage", justify="left")
    table.add_column("Graph", justify="left")

    # Add rows to the table dynamically based on live data
    cpu_percent, ram_percent, gpu_percent, total_ram, cpu_temp_celsius, gpu_temp_celsius, storage_info, sent_mb, recv_mb, active_users = get_usage()

    table.add_row("Cores", "", f"{len(cpu_percent)}", "")
    table.add_row("Overall CPU Usage", f"{cpu_percent[0]:.2f}%", f"[{'█' * int(cpu_percent[0] / 5)}{' ' * (20 - int(cpu_percent[0] / 5))}]", "")
    for i in range(1, len(cpu_percent) + 1):
        table.add_row(f"Core {i}", f"{cpu_percent[i-1]:.2f}%", f"[{'█' * int(cpu_percent[i-1] / 5)}{' ' * (20 - int(cpu_percent[i-1] / 5))}]", "")
    
    table.add_row("GPU Model", "", get_gpu_info(), "")
    table.add_row("GPU Usage", f"{gpu_percent:.2f}%", f"[{'█' * int(gpu_percent / 5)}{' ' * (20 - int(gpu_percent / 5))}]", "")
    table.add_row("Total RAM", "", f"{total_ram} GB", "")
    table.add_row("Used RAM", f"{ram_percent:.2f}%", f"[{'█' * int(ram_percent / 5)}{' ' * (20 - int(ram_percent / 5))}]", "")

    if cpu_temp_celsius is not None:
        table.add_row("CPU Temperature", f"{cpu_temp_celsius:.1f}°C", f"{'█' * int(cpu_temp_celsius / 5)}{' ' * (20 - int(cpu_temp_celsius / 5))}", "")
    else:
        table.add_row("CPU Temperature", "N/A", "", "")

    if gpu_temp_celsius is not None:
        table.add_row("GPU Temperature", f"{gpu_temp_celsius:.1f}°C", f"{'█' * int(gpu_temp_celsius / 5)}{' ' * (20 - int(gpu_temp_celsius / 5))}", "")
    else:
        table.add_row("GPU Temperature", "N/A", "", "")

    for storage in storage_info:
        device, partition_name, total, used, free, percent = storage
        table.add_row(f"{device} ({partition_name}) Storage Usage", f"{percent:.2f}%", f"[{'█' * int(percent / 5)}{' ' * (20 - int(percent / 5))}]", "")
        table.add_row(f"{device} ({partition_name}) Total Storage", "", f"{total} GB", "")
        table.add_row(f"{device} ({partition_name}) Used Storage", "", f"{used} GB", "")
        table.add_row(f"{device} ({partition_name}) Available Storage", "", f"{free} GB", "")

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
