import base64

user = '05107472990'
senhaCod = 'anJiYXcyODE2JA=='

senha = base64.b64decode(senhaCod).decode('utf-8')