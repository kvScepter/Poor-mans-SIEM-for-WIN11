import psutil
import requests
import time
from metadata_helper import get_file_info

def check_reputation(ip, key):
    if not key: return "No API Key"
    try:
        url = 'https://api.abuseipdb.com/api/v2/check'
        headers = {'Accept': 'application/json', 'Key': key}
        res = requests.get(url, headers=headers, params={'ipAddress': ip}, timeout=3).json()
        return f"Abuse Score: {res['data']['abuseConfidenceScore']}%"
    except: return "Check Failed"

def monitor_network(config, callback):
    known_ips = set()
    while True:
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr:
                    ip = conn.raddr.ip
                    if ip not in known_ips:
                        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
                        country = res.get('country', 'Unknown')
                        
                        if country in config['blocked_countries']:
                            try:
                                proc = psutil.Process(conn.pid)
                                exe_path = proc.exe()
                                proc_name = proc.name()
                                f_desc, f_comp = get_file_info(exe_path)
                            except:
                                proc_name, f_desc, f_comp = "Unknown", "Unknown", "Unknown"
                            
                            rep = check_reputation(ip, config.get('abuseipdb_key'))
                            callback("NETWORK", f"Maa: {country} | Ohjelma: {proc_name} ({f_desc} - {f_comp}) | IP: {ip} | {rep}")
                        known_ips.add(ip)
        except: pass
        time.sleep(5)
