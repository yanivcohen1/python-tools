import rsa
import base64

# Generate a new RSA key pair of 2048 bits
public_key, private_key = rsa.newkeys(2048)

def load_public_key(pub_key_string: str):
    return rsa.PublicKey.load_pkcs1(pub_key_string.encode(), "PEM")

pem_rsa_pub_key = public_key.save_pkcs1("PEM")
print("publicKeyPem:", pem_rsa_pub_key)
public_key = load_public_key(pem_rsa_pub_key.decode())
print("publicKey:", public_key)

# Encrypt a message with the public key
message = 'This is a secret message.'
encrypted_message = rsa.encrypt(message.encode(), public_key)

# Decrypt the message with the private key
decrypted_message = rsa.decrypt(encrypted_message, private_key).decode()

print(f'Original message: {message}')
print(f'Encrypted message: {base64.b64encode(encrypted_message)}')
print(f'Decrypted message: {decrypted_message}')
