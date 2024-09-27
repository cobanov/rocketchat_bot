import asyncio

import requests

from tailscale_bot import load_config
from tailscale_bot.ping_util import ping
from tailscale_bot.rocketchat_util import (initialize_api,
                                           send_status_change_message)

config = load_config()

# Initialize RocketChatAPI
api = initialize_api(
    config["ROCKET_CHAT_USERNAME"],
    config["ROCKET_CHAT_PASSWORD"],
    config["ROCKET_CHAT_SERVER_URL"],
)

# Use the tailnet name in the API URL
url = f"https://api.tailscale.com/api/v2/tailnet/{config['TAILNET_NAME']}/devices"
headers = {"Authorization": f"Bearer {config['TAILSCALE_API_KEY']}"}

# Store the previous statuses of the devices
device_statuses = {}


# Function to check and compare status changes
async def check_device_status():
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        devices = response.json().get("devices", [])
    except requests.RequestException as e:
        print(f"Error fetching devices from Tailscale API: {e}")
        return

    tasks = []
    for device in devices:
        hostname = device.get("hostname", "Unknown hostname")
        address = device.get("addresses", ["Unknown address"])[0]
        tasks.append((hostname, address, ping(address)))

    results = await asyncio.gather(*(task[2] for task in tasks))

    for i, result in enumerate(results):
        hostname, address = tasks[i][0], tasks[i][1]
        current_status = "Online" if result else "Offline"

        if hostname in device_statuses:
            if device_statuses[hostname] != current_status:
                message = f"Status change detected: Hostname: {hostname}, Address: {address}, Status: {current_status}"
                send_status_change_message(api, message, "tailscale")
        else:
            message = f"Status detected: Hostname: {hostname}, Address: {address}, Status: {current_status}"
            print(message)

        device_statuses[hostname] = current_status


# Main loop to check device status repeatedly
async def main():
    while True:
        await check_device_status()
        await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
