from Crypto.Hash import SHA256

msg = 'First'
hash256 = SHA256.new(data=msg.encode())
# hash256.update('message')
digest = hash256.digest()
print("bin digest", digest)
print("hex digest", hash256.hexdigest())

hash256_2 = SHA256.new(data=msg.encode())
print("is msg not change: ", digest == hash256_2.digest())
