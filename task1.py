import asyncio
import time
import psutil

start_time = time.time()

size = "256000"
file_count = 2


def check_space(mountpoint, size):
    disk_mem = psutil.disk_usage(mountpoint)
    if disk_mem.free > int(size)*file_count:
        res = True
    else:
        res = False
    return res    

def find_disk(size):
    for part in psutil.disk_partitions():
        if part.fstype == 'ext4' and part.device.startswith('/dev/'):
            if check_space (part.mountpoint, size):
                res =  part.mountpoint
    else:
        res = False
    return res

async def task(size, file_dir, index):  
    path_to_file = file_dir + str(index)
    cmd =  ["dd", "if=/dev/urandom", f"of={path_to_file}", f"bs={size}", "count=1"]
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
    await proc.communicate()

async def run_all(path):
    tasks = []
    for i in range(file_count):
        comand = asyncio.create_task(task(size, path, i))
        tasks.append(comand)
    await asyncio.gather(*tasks)

path =  find_disk(size)
if path:
    asyncio.run(run_all(path))
else:
    print("No free space!")

print(time.time() - start_time)
