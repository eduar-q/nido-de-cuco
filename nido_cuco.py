#!/usr/bin/env python3
import os
import sys
import json
import getpass
from datetime import datetime
from inotify_simple import INotify, flags

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DECOY_DIR = os.path.join(BASE_DIR, "decoys")
LOG_FILE = os.path.join(BASE_DIR, "events.json")

def log_event(filename, event_type):
    event_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": filename,
        "event": event_type,
        "user": getpass.getuser()
    }
    
    events = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                events = json.load(f)
        except json.JSONDecodeError:
            pass
            
    events.append(event_data)
    with open(LOG_FILE, "w") as f:
        json.dump(events, f, indent=4)

def notify_alert(filename, event_type):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getpass.getuser()
    
    print(f"\n[⚠️ ALERTA DE SEÑUELO] {timestamp}")
    print(f" 📁 Archivo: {filename}")
    print(f" ⚡ Evento:  {event_type}")
    print(f" 👤 Usuario: {username}")
    print(" [!] Interacción detectada — Requiere revisión de contexto.\n")
    
    log_event(filename, event_type)

def start_watch():
    if not os.path.exists(DECOY_DIR):
        print(f"[!] Error: La carpeta {DECOY_DIR} no existe.")
        sys.exit(1)

    inotify = INotify()
    watch_flags = flags.ACCESS | flags.OPEN
    inotify.add_watch(DECOY_DIR, watch_flags)

    print(f"[*] Nido de Cuco activo en: {DECOY_DIR}")
    print("[*] Esperando eventos... (Presiona Ctrl+C para salir)\n")

    try:
        while True:
            for event in inotify.read():
                for flag in flags.from_mask(event.mask):
                    notify_alert(event.name, flag.name)
    except KeyboardInterrupt:
        print("\n[!] Sensor detenido.")

if __name__ == "__main__":
    start_watch()
