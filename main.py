import jwt
  
header = {  
  "alg": "HS256",  
  "typ": "JWT"  
}  
  
payload = {  
  "userid": "nikhil@gmail.com",  
  "pwd": "1516299022",  
}  
  
secret = "Ravipass"  
  
encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)  
print(encoded_jwt)  
decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=['HS256'])  
print(decoded_jwt)  