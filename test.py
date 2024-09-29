import json 

file_token = "b35b13fa14a2ecab2aef58e4d47449ccf918d52a46d79035d764f0d399dd79f4"
file_token = file_token.encode('utf-8')
val = json.loads(file_token.decode())
print(val)