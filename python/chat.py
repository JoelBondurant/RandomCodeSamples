import requests, json

HIP_CHAT_API_KEY = os.getenv('HIP_CHAT_API_KEY')
HIP_CHAT_ROOM_ID = os.getenv('HIP_CHAT_ROOM_ID')

def hipchat(msg, auth_key = HIP_CHAT_API_KEY, room_id = HIP_CHAT_ROOM_ID):
	room = 'https://api.hipchat.com/v2/room/%s/notification' % room_id
	headers = {'Authorization':'Bearer %s' % auth_key, 'Content-type':'application/json', 'Accept':'text/plain'}
	requests.post(url = room, data = json.dumps({'message':msg}), headers = headers)

