from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Math.Numbers import Integer

import os
import hashlib

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(point.x.to_bytes())
    sha.update(point.y.to_bytes())
    return sha.digest()

def ecc_encrypt(plain_text, ecc_public_key):
    ecc_shared_key = ECC.generate(curve='P-256')
    aes_key = ecc_point_to_256_bit_key(ecc_public_key.pointQ * ecc_shared_key.d)
    cipher = AES.new(aes_key, AES.MODE_GCM)
    nonce = cipher.nonce
    cipher_text = cipher.encrypt(plain_text)
    return cipher_text, ecc_shared_key.public_key().export_key(format='PEM'), nonce

def ecc_decrypt(cipher_text, ecc_private_key, shared_key, nonce):
    ecc_shared_key = ECC.import_key(shared_key)
    aes_key = ecc_point_to_256_bit_key(ecc_private_key.d * ecc_shared_key.pointQ)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    plain_text = cipher.decrypt(cipher_text)
    return plain_text

ecc_private_key = ECC.generate(curve='P-256')
ecc_public_key = ecc_private_key.public_key()

data = b'kho6ngcogi'
cipher_text, shared, nonce = ecc_encrypt(data, ecc_public_key)
plain_text = ecc_decrypt(cipher_text, ecc_private_key, shared, nonce)

print(data == plain_text)

passphrase = 'hay'

f = open('private.pem', 'wt')
f.write(ecc_private_key.export_key(format='PEM', protection='PBKDF2WithHMAC-SHA1AndAES128-CBC', passphrase=passphrase))
f.close()

f = open('public.pem', 'wt')
f.write(ecc_public_key.export_key(format='PEM'))
f.close()
