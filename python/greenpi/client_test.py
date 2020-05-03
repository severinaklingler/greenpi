import requests
import random


headers = {'Authorization': 'Token 1d86170f070d174a03cc1b6d34e13f76c7347bc0'}
server_url = 'https://aqueous-depths-78223.herokuapp.com/'

print('adding random sensor measurement')

data = {'value': random.randint(0,40),'sensor':'test','tree_id':0}
r = requests.post(server_url + 'add_measurement/',data=data, headers=headers)
print(r.headers)
print(r.json())


print('print all sensor measurements')
r = requests.get(server_url + 'measurements/')
print(r.headers)
print(r.json())