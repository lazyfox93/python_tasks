import asyncio
import argparse


async def task(host, command):
    cmd =  ["ssh", host]
    args = command.split()
    cmd.extend(args)
    proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE)
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()


async def main(hosts, cmd):
    for host in args.ips:
        command = asyncio.create_task(task(host, cmd))
        tasks.append(command)
    
    res = await asyncio.gather(*tasks)
    return res
   

if __name__ == "__main__":
    tasks = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--IPs", dest='ips', nargs='+')
    parser.add_argument("--exec", dest="cmd")
    args = parser.parse_args()
    outs = asyncio.run(main(args.ips, args.cmd))
    print(outs)
