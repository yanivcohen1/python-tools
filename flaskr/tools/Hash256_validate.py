from Crypto.Hash import SHA256

msg = 'First'
hash256 = SHA256.new(data=msg.encode())
# hash256.update('message')
digest = hash256.digest()
print("bin digest:", digest)
print("hex digest:", hash256.hexdigest())

hash256_2 = SHA256.new(data=msg.encode())
print("is msg not change: ", digest == hash256_2.digest())

# --------- test from const--------------------
hash256 = SHA256.new(data=b'yaniv')
digest = hash256.hexdigest()
print("\nhex digest calc:", digest)
hexToValidate = "c7b18ad0447f947c2a4304951a624a599f61d66e1b62c36a43e4a4091e4e11c6"
print("hex digest orig:", hexToValidate)
print("hex digest valid:", digest == hexToValidate)
