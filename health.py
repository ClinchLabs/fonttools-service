import psutil, datetime

def getHealth():
    memory = psutil.virtual_memory()
    uptime = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    return memory, uptime, cpu
