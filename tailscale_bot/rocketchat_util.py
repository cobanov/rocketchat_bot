from rocketchat.api import RocketChatAPI


# Initialize RocketChatAPI
def initialize_api(username, password, domain):
    return RocketChatAPI(settings={
        'username': username,
        'password': password,
        'domain': domain
    })

# Send message to RocketChat
def send_status_change_message(api, message, channel):
    try:
        api.send_message(message, channel)
    except Exception as e:
        print(f"Error sending message to RocketChat: {e}")
