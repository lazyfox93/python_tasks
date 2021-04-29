import asyncio


size = "1MB"
file_count = 10
file_dir = "./test/"


async def cmd_run(size, file_dir, index):  
    path_to_file = file_dir + str(index)
    cmd =  ["dd", "if=/dev/urandom", f"of={path_to_file}", f"bs={size}", "count=1"]
    await asyncio.create_subprocess_exec(*cmd)
 
async def main():
    tasks = []
    for i in range(file_count):
        task = asyncio.create_task(cmd_run(size, file_dir, i))
        tasks.append(task)

    await asyncio.gather(*tasks)

asyncio.run(main())
