import subprocess
import argparse
import sys

# Run setup scripts before anything else
def run_setup():
    try:
        print("[*] Running setup scripts...")
        subprocess.run(["chmod", "+x", "dockersetup"], check=True)
        subprocess.run(["chmod", "+x", "setup"], check=True)
        subprocess.run(["./setup"], check=True)
        print("[+] Setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERR] Setup failed: {e}")
        sys.exit(1)

# Set OSPF cost on a specific interface of a router container
def set_ospf_cost(container, interface, cost):
    try:
        cmd = [
            "docker", "exec", container,
            "vtysh", "-c", "configure terminal",
            "-c", f"interface {interface}",
            "-c", f"ip ospf cost {cost}",
            "-c", "end",
            "-c", "write memory"
        ]
        subprocess.run(cmd, check=True)
        print(f"[OK] Set cost {cost} on {container}:{interface}")
    except subprocess.CalledProcessError as e:
        print(f"[ERR] Failed to set cost on {container}:{interface}: {e}")

# Switch to north path: r1→r2→r3
def set_north_path():
    print("[*] Switching to NORTH path (via R2)...")
    set_ospf_cost("r1", "eth0", 10)
    set_ospf_cost("r1", "eth1", 100)
    set_ospf_cost("r3", "eth0", 10)
    set_ospf_cost("r3", "eth1", 100)
    print("[+] Path switched to NORTH")

# Switch to south path: r1→r4→r3
def set_south_path():
    print("[*] Switching to SOUTH path (via R4)...")
    set_ospf_cost("r1", "eth0", 100)
    set_ospf_cost("r1", "eth1", 10)
    set_ospf_cost("r3", "eth1", 100)
    set_ospf_cost("r3", "eth1", 10)
    print("[+] Path switched to SOUTH")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dynamic OSPF Traffic Rerouter with automatic setup execution"
    )
    parser.add_argument(
        "path",
        choices=["north", "south"],
        help="Select OSPF path to activate: 'north' for R1→R2→R3, 'south' for R1→R4→R3"
    )

    args = parser.parse_args()

    run_setup()

    if args.path == "north":
        set_north_path()
    elif args.path == "south":
        set_south_path()
