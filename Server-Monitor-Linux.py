import os
import time

import psutil
from psutil._common import suser
from rich.console import Console, JustifyMethod
from rich.live import Live
from rich.table import Table


def get_cpu_info():
    try:
        cpu_info = os.popen("lscpu | grep 'Model name'").read().strip().split(":")[1].strip()
        return cpu_info
    except Exception as e:
        print(f"Error getting CPU information: {e}")
        return "N/A"

def get_gpu_info():
    try:
        gpu_info = os.popen("nvidia-smi --query-gpu=name --format=csv,noheader").read().strip()
        return gpu_info.split("\n")
    except Exception as e:
        print(f"Error getting GPU information: {e}")
        return ["N/A"]

def get_gpu_usage():
    try:
        gpu_usage = os.popen("nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits").read().strip()
        return [float(usage) for usage in gpu_usage.split("\n")]
    except Exception as e:
        print(f"Error getting GPU usage: {e}")
        return []

def get_cpu_cores():
    try:
        cpu_cores = psutil.cpu_count(logical=False)
        return cpu_cores
    except Exception as e:
        print(f"Error getting CPU cores: {e}")
        return 0

def get_cpu_threads():
    try:
        cpu_threads = psutil.cpu_count(logical=True)
        return cpu_threads
    except Exception as e:
        print(f"Error getting CPU threads: {e}")
        return 0

def get_cpu_usage():
    try:
        cpu_percent = psutil.cpu_percent(percpu=True)
        return cpu_percent
    except Exception as e:
        print(f"Error getting CPU usage: {e}")
        return []

def get_cpu_temperature():
    try:
        temperatures = psutil.sensors_temperatures()
        if 'coretemp' in temperatures:
            core_temp_celsius = temperatures['coretemp'][0].current
            core_temp_fahrenheit = celsius_to_fahrenheit(core_temp_celsius)
            return core_temp_celsius, core_temp_fahrenheit
    except Exception as e:
        print(f"Error getting CPU temperature: {e}")
    return None, None

def get_gpu_temperature():
    try:
        gpu_temperatures = os.popen("nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits").read().strip()
        return [float(temp) for temp in gpu_temperatures.split("\n")]
    except Exception as e:
        print(f"Error getting GPU temperatures: {e}")
        return []

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

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
        active_users: list[suser] = [user.name for user in psutil.users()]
        return active_users
    except Exception as e:
        print(f"Error getting active users: {e}")
        return []

def get_usage():
    try:
        cpu_percent, ram_percent, cpu_cores, cpu_threads, gpu_percent, total_ram, cpu_temp_celsius, cpu_temp_fahrenheit, gpu_temperatures, total_storage_gb, used_storage_gb, free_storage_gb, used_storage_percent, sent_mb, recv_mb, active_users, gpu_models = (
            get_cpu_usage(),
            psutil.virtual_memory().percent,
            get_cpu_cores(),
            get_cpu_threads(),
            get_gpu_usage(),
            round(psutil.virtual_memory().total / (1024.0 ** 3), 2),
            *get_cpu_temperature(),
            get_gpu_temperature(),
            *get_main_storage_usage(),
            *get_network_usage(),
            get_active_users(),
            get_gpu_info()
        )
        return (
            cpu_percent, ram_percent, cpu_cores, cpu_threads, gpu_percent, total_ram, cpu_temp_celsius, 
            cpu_temp_fahrenheit, gpu_temperatures, total_storage_gb, used_storage_gb, free_storage_gb, 
            used_storage_percent, sent_mb, recv_mb, active_users, gpu_models
        )
    except Exception as e:
        print(f"Error getting system usage: {e}")
        return [], 0, 0, 0, [], 0, None, None, [], 0, 0, 0, 0, 0, 0, [], []


def generate_table():
    table = Table(
        show_header=True, 
        header_style="bold magenta", 
        width = os.get_terminal_size().columns, 
        title="System Information", 
        title_style="bold", 
        expand=True, 
        show_lines=False
    )
    table.add_column("Component", justify="left", min_width=20, max_width=40)
    table.add_column("Info", justify="left", min_width=15, max_width=40)
    table.add_column("Usage", justify="left", min_width=10, max_width=40)

    cpu_percent, ram_percent, cpu_cores, cpu_threads, gpu_percent, total_ram, cpu_temp_celsius, cpu_temp_fahrenheit, gpu_temperatures, total_storage_gb, used_storage_gb, free_storage_gb, used_storage_percent, sent_mb, recv_mb, active_users, gpu_models = get_usage()

    table.add_row("== CPU Usage ==", "== CPU Usage ==", "== CPU Usage ==")
    if cpu_cores:
        table.add_row("Cores", "", f"{cpu_cores} (Threads: {cpu_threads})")
        for i, cpu_percent_core in enumerate(cpu_percent):
            table.add_row(f"Core {i + 1}", f"{cpu_percent_core:.2f}%", f"[{'█' * int(cpu_percent_core / 5)}{' ' * (20 - int(cpu_percent_core / 5))}]")
        overall_cpu_percent = sum(cpu_percent) / len(cpu_percent)
        table.add_row("Overall CPU Usage", f"{overall_cpu_percent:.2f}%", f"[{'█' * int(overall_cpu_percent / 5)}{' ' * (20 - int(overall_cpu_percent / 5))}]", end_section=True)
        table.add_section()

    table.add_row("== GPU Usage ==", "== GPU Usage ==", "== GPU Usage ==")
    for i, gpu_model in enumerate(gpu_models):
        table.add_row(f"GPU {i + 1} Model", gpu_model, gpu_model)
        gpu_percent_val = gpu_percent[i] if gpu_percent else 0
        gpu_temperature_val = gpu_temperatures[i] if gpu_temperatures else None
        table.add_row(f"GPU {i + 1} Usage", f"{gpu_percent_val:.2f}%", f"[{'█' * int(gpu_percent_val / 5)}{' ' * (20 - int(gpu_percent_val / 5))}]")
        table.add_row(f"GPU {i + 1} Temperature", f"{gpu_temperature_val:.1f}°C" if gpu_temperature_val is not None else "N/A", f"[{'█' * int(gpu_temperature_val / 5)}{' ' * (20 - int(gpu_temperature_val / 5))}]" if gpu_temperature_val is not None else "")
    table.add_row(end_section=True)
    table.add_section()

    table.add_row("== RAM & CPU Temp ==", "== RAM & CPU Temp ==", "== RAM & CPU Temp ==")
    if ram_percent:
        table.add_row("Total RAM", "", f"{total_ram} GB")
        table.add_row("Used RAM", f"{ram_percent:.2f}%", f"[{'█' * int(ram_percent / 5)}{' ' * (20 - int(ram_percent / 5))}]")
    if cpu_temp_celsius is not None:
        table.add_row("CPU Temperature", f"{cpu_temp_celsius:.1f}°C / {cpu_temp_fahrenheit:.1f}°F", f"{'█' * int(cpu_temp_celsius / 5)}{' ' * (20 - int(cpu_temp_celsius / 5))}")
    else:
        table.add_row("CPU Temperature", "N/A", "", end_section=True)
    table.add_section()

    if used_storage_percent:
        table.add_row("== Disk Usage ==", "== Disk Usage ==", "== Disk Usage ==")
        table.add_row("Main Storage Usage", f"{used_storage_percent:.2f}%", f"[{'█' * int(used_storage_percent / 5)}{' ' * (20 - int(used_storage_percent / 5))}]")
        table.add_row("Total Storage", "", f"{total_storage_gb} GB")
        table.add_row("Used Storage", "", f"{used_storage_gb} GB")
        table.add_row("Available Storage", "", f"{free_storage_gb} GB", end_section=True)
        table.add_section()

    if sent_mb:
        table.add_row("Network Sent", f"{sent_mb:.2f} MB", "")
        table.add_row("Network Received", f"{recv_mb:.2f} MB", "", end_section=True)
        table.add_section()

    if active_users and isinstance(active_users, list):
        table.add_row()
        active_users_str: str = ", ".join([str(ea.name) for ea in active_users if isinstance(ea, suser)])
        table.add_row("Active Users", active_users_str, "", end_section=True)

    return table

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    console = Console()

    with Live(generate_table(), console=console, refresh_per_second=2, auto_refresh=True, transient=True) as live:
        while True:
            live.update(generate_table())
            time.sleep(0.4)

if __name__ == "__main__":
    main()
