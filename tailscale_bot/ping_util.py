import asyncio
import subprocess


# Async function to ping a machine
async def ping(address):
    try:
        # Execute the ping command asynchronously
        process = await asyncio.create_subprocess_shell(
            f"ping -c 1 {address}",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        # Check the return code. 0 means the ping was successful
        return process.returncode == 0
    except Exception as e:
        print(f"Error pinging {address}: {e}")
        return False
