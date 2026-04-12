import nmap
import socket
import sys
import json
import time

nm = nmap.PortScanner()

# 🌐 resolve domain/IP
def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except:
        return None


# 🔥 MAIN ENGINE
def full_scan(target):
    output = {
        "target": target,
        "ip": "",
        "state": "",
        "ports": [],
        "os": "",
        "services": [],
        "summary": {}
    }

    ip = resolve_host(target)
    if not ip:
        return {"error": "Host not reachable"}

    output["ip"] = ip

    try:
        # 🚀 FULL SAFE ADVANCED SCAN
        nm.scan(ip, arguments="""
            -sS        # SYN scan
            -sV        # service/version detection
            -O         # OS detection
            -F         # fast scan
            -T4        # speed
        """)

        for host in nm.all_hosts():
            output["state"] = nm[host].state()

            # OS detection
            try:
                output["os"] = nm[host]["osmatch"][0]["name"]
            except:
                output["os"] = "Unknown"

            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()

                for port in sorted(ports):
                    port_data = nm[host][proto][port]

                    output["ports"].append({
                        "port": port,
                        "state": port_data["state"],
                        "service": port_data["name"],
                        "product": port_data.get("product", ""),
                        "version": port_data.get("version", "")
                    })

                    output["services"].append(port_data["name"])

        # 📊 summary
        output["summary"] = {
            "total_ports": len(output["ports"]),
            "open_ports": len([p for p in output["ports"] if p["state"] == "open"]),
            "services_found": list(set(output["services"]))
        }

        return output

    except Exception as e:
        return {"error": str(e)}


# 🖥 CLI MODE (for testing)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script2.py <target>")
        sys.exit()

    result = full_scan(sys.argv[1])
    print(json.dumps(result, indent=4))
