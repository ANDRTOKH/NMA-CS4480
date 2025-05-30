import subprocess
import argparse

def run_setup_script():
    print("[*] Running setup script...")
    try:
        subprocess.run(["chmod", "+x", "setup"], check=True)
        subprocess.run(["./setup"], check=True)
        print("[+] Setup script completed.")
    except subprocess.CalledProcessError as e:
        print(f"[ERR] Failed to run setup script: {e}")

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

def set_north_path():
    print("[*] Switching to NORTH path (via R2)...")
    set_ospf_cost("part15-r1-1", "eth0", 10)
    set_ospf_cost("part15-r2-1", "eth0", 10)
    set_ospf_cost("part15-r2-1", "eth1", 10)
    set_ospf_cost("part15-r3-1", "eth0", 10)

    set_ospf_cost("part15-r1-1", "eth1", 100)
    set_ospf_cost("part15-r3-1", "eth1", 100)
    set_ospf_cost("part15-r4-1", "eth0", 100)
    set_ospf_cost("part15-r4-1", "eth1", 100)
    print("[+] Path switched to NORTH")

def set_south_path():
    print("[*] Switching to SOUTH path (via R4)...")
    set_ospf_cost("part15-r1-1", "eth0", 100)
    set_ospf_cost("part15-r2-1", "eth0", 100)
    set_ospf_cost("part15-r2-1", "eth1", 100)
    set_ospf_cost("part15-r3-1", "eth0", 100)

    set_ospf_cost("part15-r1-1", "eth1", 10)
    set_ospf_cost("part15-r3-1", "eth1", 10)
    set_ospf_cost("part15-r4-1", "eth0", 10)
    set_ospf_cost("part15-r4-1", "eth1", 10)
    print("[+] Path switched to SOUTH")

def show_routes():
    routers = ["r1", "r2", "r3", "r4"]
    for r in routers:
        print(f"\n--- OSPF Routes on {r.upper()} ---")
        try:
            subprocess.run(["docker", "exec", r, "vtysh", "-c", "show ip route ospf"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERR] Could not get routes for {r}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dynamic OSPF Traffic Rerouter"
    )
    parser.add_argument(
        "path",
        nargs="?",
        choices=["north", "south", "setup"],
        help="Select OSPF path or run setup"
    )
    parser.add_argument(
        "--show", action="store_true",
        help="Show current OSPF routes on all routers"
    )

    args = parser.parse_args()

    if args.show:
        show_routes()
    elif args.path == "north":
        set_north_path()
    elif args.path == "south":
        set_south_path()
    elif args.path == "setup":
        run_setup_script()
    else:
        parser.print_help()
