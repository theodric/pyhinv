#!/usr/bin/env python3
import os
import platform
import subprocess

def get_cpu_info():
    """Retrieve CPU information."""
    cpu_info = {
        "model_name": None,
        "cores": None,
        "threads": None,
    }
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    cpu_info["model_name"] = line.split(":")[1].strip()
                elif "cpu cores" in line:
                    cpu_info["cores"] = int(line.split(":")[1].strip())
                elif "siblings" in line:
                    cpu_info["threads"] = int(line.split(":")[1].strip())
    except Exception as e:
        cpu_info["error"] = str(e)
    return cpu_info

def get_memory_info():
    """Retrieve memory information."""
    mem_info = {
        "total": None,
    }
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if "MemTotal" in line:
                    mem_info["total"] = int(line.split()[1]) // 1024  # Convert kB to MB
                    break
    except Exception as e:
        mem_info["error"] = str(e)
    return mem_info

def get_storage_info():
    """Retrieve storage information."""
    storage_info = []
    try:
        result = subprocess.run(["lsblk", "-o", "NAME,SIZE,TYPE"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines()[1:]:
                name, size, type_ = line.split()
                if type_ == "disk":
                    storage_info.append({"name": name, "size": size})
    except Exception as e:
        storage_info.append({"error": str(e)})
    return storage_info

def get_network_info():
    """Retrieve network interface information."""
    network_info = []
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f.readlines()[2:]:  # Skip headers
                iface = line.split()[0].strip(":")
                network_info.append(iface)
    except Exception as e:
        network_info.append({"error": str(e)})
    return network_info

def get_gpu_info():
    """Retrieve GPU information."""
    gpu_info = []
    try:
        result = subprocess.run(["lspci"], capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "VGA compatible controller" in line or "3D controller" in line:
                    gpu_info.append(line.strip())
    except Exception as e:
        gpu_info.append({"error": str(e)})
    return gpu_info

def get_os_info():
    """Retrieve OS and kernel information."""
    return {
        "os": platform.system(),
        "version": platform.version(),
        "release": platform.release(),
        "architecture": platform.architecture()[0],
    }

def main():
    """Main function to display hardware inventory."""
    inventory = {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "storage": get_storage_info(),
        "network": get_network_info(),
        "gpu": get_gpu_info(),
        "os": get_os_info(),
    }

    print("Hardware Inventory:\n")
    print("CPU:")
    print(f"  Model: {inventory['cpu'].get('model_name', 'Unknown')}")
    print(f"  Cores: {inventory['cpu'].get('cores', 'Unknown')}")
    print(f"  Threads: {inventory['cpu'].get('threads', 'Unknown')}\n")

    print("Memory:")
    print(f"  Total: {inventory['memory'].get('total', 'Unknown')} MB\n")

    print("Storage:")
    for disk in inventory['storage']:
        if "error" in disk:
            print(f"  Error: {disk['error']}")
        else:
            print(f"  Disk: {disk['name']} - {disk['size']}")
    print()

    print("Network Interfaces:")
    for iface in inventory['network']:
        if isinstance(iface, dict) and "error" in iface:
            print(f"  Error: {iface['error']}")
        else:
            print(f"  Interface: {iface}")
    print()

    print("GPU:")
    for gpu in inventory['gpu']:
        if "error" in gpu:
            print(f"  Error: {gpu['error']}")
        else:
            print(f"  {gpu}")
    print()

    print("OS:")
    print(f"  Name: {inventory['os']['os']}")
    print(f"  Version: {inventory['os']['version']}")
    print(f"  Release: {inventory['os']['release']}")
    print(f"  Architecture: {inventory['os']['architecture']}\n")

if __name__ == "__main__":
    main()
