import subprocess
import argparse

# Set OSPF cost on an interface for a given container
def set_ospf_cost(container, interface, cost):
    cmd = [
        "docker", "exec", container,
        "vtysh", "-c", "configure terminal",
        "-c", f"interface {interface}",
        "-c", f"ip ospf cost {cost}",
        "-c", "end",
        "-c", "write memory"
    ]
    subprocess.run(cmd, check=True)

# North path: R1 -> R2 -> R3
def set_north_path():
    print("Switching to NORTH path (via R2)...")
    set_ospf_cost("r1", "eth0", 10)  # R1 -> R2
    set_ospf_cost("r1", "eth1", 100) # R1 -> R4 (make less attractive)

    set_ospf_cost("r3", "eth0", 10)  # R3 -> R2
    set_ospf_cost("r3", "eth1", 100) # R3 -> R4

# South path: R1 -> R4 -> R3
def set_south_path():
    print("Switching to SOUTH path (via R4)...")
    set_ospf_cost("r1", "eth0", 100) # R1 -> R2 (make less attractive)
    set_ospf_cost("r1", "eth1", 10)  # R1 -> R4

    set_ospf_cost("r3", "eth0", 100) # R3 -> R2
    set_ospf_cost("r3", "eth1", 10)  # R3 -> R4

# Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OSPF Traffic Path Orchestrator")
    parser.add_argument("path", choices=["north", "south"], help="Choose path: north or south")

    args = parser.parse_args()
    
    if args.path == "north":
        set_north_path()
    elif args.path == "south":
        set_south_path()
