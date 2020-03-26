import base64
import boto3


# Decrypt in 'different account'
kmsclient = boto3.client('kms', region_name="us-west-2")
ciphertext = "xxxxxxxxxxx"
decrypted_value = kmsclient.decrypt(CiphertextBlob=base64.b64decode(ciphertext))['Plaintext'].decode('utf-8')
print(decrypted_value)

# Encrypt in 'different account'
kmsclient = boto3.client('kms', region_name="us-east-2")
key_id = 'arn:aws:kms:us-east-2:XXXXXXXXXXXXXX:key/7c4533c0'
stuff = kmsclient.encrypt(KeyId=key_id, Plaintext=decrypted_value)
binary_encrypted = stuff[u'CiphertextBlob']
encrypted_password = base64.b64encode(binary_encrypted)
print(encrypted_password.decode())

# Encrypt in 'different account'
decrypted_value = "xyz"
kmsclient = boto3.client('kms', region_name="us-east-2")
key_id = 'arn:aws:kms:us-east-2:XXXXXXXXXXXXXX:key/6bedafac'
stuff = kmsclient.encrypt(KeyId=key_id, Plaintext=decrypted_value)
binary_encrypted = stuff[u'CiphertextBlob']
encrypted_password = base64.b64encode(binary_encrypted)
print(encrypted_password.decode())
