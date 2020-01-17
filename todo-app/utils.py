from basicauth import encode, decode

username, password = 'abc', 'abc'
encoded_str = encode(username, password)
print(encoded_str)