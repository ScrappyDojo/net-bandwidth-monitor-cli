from pathlib import Path
import os, sys, traceback, pip

#check if psutil is installed in device
#if not, install via pip
try:
    from psutil import net_io_counters
except ImportError:
    print("Installing psutil via pip...")
    pip.main(['install', 'psutil'])
    from psutil import net_io_counters

# constants
KB = float(1024)
MB = float(KB) ** 2 #1024 * 1024
GB = float(KB) ** 3 #1024 * 1024 * 1024
TB = float(KB) ** 4 #1024 * 1024 * 1024

# conversion and formatting of data sent/received over the network
def size(B):
    B = float(B)

    if B < KB: return f"{B} Bytes"
    if KB <= B < MB: return f"{B/KB:.2f} KB"
    if MB <= B < GB: return f"{B/MB:.2f} MB"
    if GB <= B < TB: return f"{B/GB:.2f} GB"
    if B >= TB: return f"{B/TB:.2f} TB"

# prints values of data sent and data received
def update():
    global upload, download, total
    counters = net_io_counters()

    upload = counters.bytes_sent
    download = counters.bytes_recv
    total = upload + download

    #format before printing
    print("Upload: {0} Download: {1} Total: {2}".format(size(upload), size(download), size(total)),
        end = "\r")

#check if directory exists
def check_dir(dir):
    return Path(dir).is_dir()

#check if file exists
def check_file(filename):
    return Path(filename).is_file()

#write to file
def write_to_file(file):
    global upload, download, total

    file.write("{0}, {1}, {2}\n".format(upload, download, total))

def __main__():
    upload, download, total = 0, 0, 0
    dir = "./data"
    filename = "./data/net_use_stat.txt"

    if (check_dir(dir)) == False:
        os.mkdir(dir)

    if check_file(filename):
        file = open(filename, "a")
    else:
        file = open(filename, "w+")

    try:
        while True:
            update()
    except KeyboardInterrupt:
        print("\nShutting down... saving consumption data...")
        write_to_file(file)
    except Exception:
        traceback.print_exc(file=sys.stdout)
    file.close()
    sys.exit(0)

__main__()
