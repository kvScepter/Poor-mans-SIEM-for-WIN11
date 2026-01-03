import win32evtlog
import time
from datetime import datetime, timezone
from metadata_helper import get_file_info

EVENT_MAP = {
    4625: ("EPÄONNISTUNUT KIRJAUTUMINEN", 5),
    4720: ("UUSI KÄYTTÄJÄ LUOTU", 0),
    4732: ("LISÄTTY ADMIN-RYHMÄÄN", 0),
    4688: ("UUSI PROSESSI KÄYNNISTETTY", 5),
    1102: ("AUDIT-LOKI TYHJENNETTY", None)
}

def monitor_events(config, callback):
    from datetime import timedelta
    last_event_time = datetime.now(timezone.utc) - timedelta(seconds=10)
    
    server = 'localhost'
    logtype = 'Security'
    
    while True:
        try:
            hand = win32evtlog.OpenEventLog(server, logtype)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if events:
                batch_newest = events[0].TimeGenerated.replace(tzinfo=timezone.utc)
                
                for event in events:
                    event_time = event.TimeGenerated.replace(tzinfo=timezone.utc)
                    if event_time <= last_event_time:
                        break
                    
                    eid = event.EventID
                    if eid in config['watched_event_ids']:
                        data = event.StringInserts
                        desc, index = EVENT_MAP.get(eid, ("Tapahtuma", None))
                        
                        try:
                            if eid == 4688 and len(data) > 6:
                                full_path = data[5]
                                parent_proc = data[6].split('\\')[-1].lower() # Käynnistävä ohjelma
                                proc_name = full_path.split('\\')[-1]
                                
                                if proc_name in config.get('whitelist_processes', []): continue
                                
                                # TUNNISTUS: Jos käynnistäjä on explorer.exe, se on Win+R tai Työpöytä
                                source_tag = "[KÄYTTÄJÄ]" if parent_proc == "explorer.exe" else "[SYSTEM/APP]"
                                
                                cmd = "Ei komentoriviä"
                                for i in [8, 9, 10]:
                                    if len(data) > i and data[i] and not data[i].startswith('S-1-'):
                                        cmd = data[i].strip()
                                        break
                                
                                f_desc, f_comp = get_file_info(full_path)
                                detail = f"{source_tag} {proc_name} ({f_desc}) | Komento: {cmd[:150]}"
                                callback("SECURITY", f"{desc} | {detail}")
                                
                            elif index is not None and len(data) > index:
                                detail = f"Kohde: {data[index]}"
                                callback("SECURITY", f"{desc} | {detail}")
                        except: pass
                
                last_event_time = batch_newest
            win32evtlog.CloseEventLog(hand)
        except: pass
        time.sleep(2)
