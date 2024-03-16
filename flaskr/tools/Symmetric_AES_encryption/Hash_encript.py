from Crypto.Hash import SHA256

str1 = 'First'
hash256 = SHA256.new(data=str1.encode())
# hash256.update('message')
digest = hash256.digest()
print(digest)

hash256_2 = SHA256.new(data=str1.encode())
print("is msg not change: ", digest == hash256_2.digest())
