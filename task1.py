import argparse
import asyncio
import time
import psutil

start_time = time.time()


def check_space(mountpoint, size):
    disk_mem = psutil.disk_usage(mountpoint)
    size_int = int(size)
    if disk_mem.free > size_int:
        res = True
    else:
        res = False
    return res


def find_disk(size):
    fs_types = ['ext4', 'ext3', 'xfs']
    for part in psutil.disk_partitions():
        if part.fstype in fs_types and part.device.startswith('/dev/'):
            if check_space(part.mountpoint, size):
                res = part.mountpoint
                break
    else:
        res = False
    return res


async def task(size, file_dir, index):
    path_to_file = file_dir + str(index)
    cmd = [
        "dd", "if=/dev/urandom", f"of={path_to_file}", f"bs={size}", "count=1"
        ]
    proc = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
    stdout, stderr = await proc.communicate()
    return path_to_file, proc.returncode, stdout.decode(), stderr.decode()


async def run_all(path, file_count, size):
    tasks = []
    for i in range(int(file_count)):
        comand = asyncio.create_task(task(size, path, i))
        tasks.append(comand)
    res = await asyncio.gather(*tasks)
    return res

parser = argparse.ArgumentParser()
parser.add_argument("--file_count", required=True)
parser.add_argument("--file_size", required=True)
parser.add_argument("--req_space", required=True)
args = parser.parse_args()

path = find_disk(args.req_space)
if path:
    out = asyncio.run(run_all(path, args.file_count, args.file_size))
    print(out)
else:
    print("No free space!")

print(time.time() - start_time)
