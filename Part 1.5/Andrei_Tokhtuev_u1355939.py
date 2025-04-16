import subprocess
import argparse

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
    set_ospf_cost("r1", "eth0", 10)   # r1 → r2
    set_ospf_cost("r1", "eth1", 100)  # r1 → r4
    set_ospf_cost("r3", "eth0", 10)   # r3 ← r2
    set_ospf_cost("r3", "eth1", 100)  # r3 ← r4
    print("[+] Path switched to NORTH")

def set_south_path():
    print("[*] Switching to SOUTH path (via R4)...")
    set_ospf_cost("r1", "eth0", 100)  # r1 → r2
    set_ospf_cost("r1", "eth1", 10)   # r1 → r4
    set_ospf_cost("r3", "eth0", 100)  # r3 ← r2
    set_ospf_cost("r3", "eth1", 10)   # r3 ← r4
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
        choices=["north", "south"],
        help="Select OSPF path to activate"
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
    else:
        parser.print_help()
