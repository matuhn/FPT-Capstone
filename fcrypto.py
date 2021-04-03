from Crypto.Cipher import AES
from Crypto.PublicKey import ECC
from Crypto.Random import get_random_bytes
from Crypto.Math.Numbers import Integer
import os
import hashlib
import function
import config


def add_file(parent_dir, filename, key, nonce):
    try:
        query = "INSERT INTO Crypto(DIR, FILENAME, KEY, NONCE) " \
                "VALUES (:dir, :filename, :key, :nonce)"
        conn = function.get_connection()
        conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename, 'key': key, 'nonce': nonce})
        conn.commit()
    except Exception as ex:
        print(ex)

def delete_file(parent_dir, filename):
    try:
        query = "DELETE FROM Crypto WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'filename': filename, 'dir': parent_dir})
        conn.commit()
    except Exception as ex:
        print(ex)

def edit_file_name(parent_dir, filename, new_name):
    try:
        query = "UPDATE Crypto SET FILENAME = :new_name WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        conn.cursor().execute(query, {'new_name': new_name, 'filename': filename, 'dir': parent_dir})
        conn.commit()
    except Exception as ex:
        print(ex)

def get_key_and_nonce(parent_dir, filename):
    try:
        query = "SELECT KEY, NONCE FROM Crypto WHERE DIR = :dir AND FILENAME = :filename"
        conn = function.get_connection()
        c = conn.cursor().execute(query, {'dir': parent_dir, 'filename': filename})
        for row in c:
            if row is not None:
                #decrypt ECC
                return row[0], row[1]
    except Exception as ex:
        print(ex)

def aes_encrypt(plain_text):
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_CTR)
    nonce = cipher.nonce
    cipher_text = cipher.encrypt(plain_text)
    return cipher_text, key, nonce

def aes_decrypt(cipher_text, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    plain_text = cipher.decrypt(cipher_text)
    return plain_text

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

def encrypt_file(parent_dir, filename, content, ecc_public_key):
    path = os.path.join(function.make_file_path(parent_dir), filename)
    cipher_text, key, nonce = ecc_encrypt(content, ecc_public_key)
    with open(path,'wb') as f:
        f.write(cipher_text)
    add_file(parent_dir, filename, key, nonce)

def decrypt_file(parent_dir, filename, key, nonce, ecc_private_key):
    path = os.path.join(function.make_file_path(parent_dir), filename)
    with open(path, 'rb') as f:
        data = f.read()
    plain_text = ecc_decrypt(data, ecc_private_key, key, nonce)
    # download_name = function.make_unique(filename)
    # download_path = os.path.join(config.DOWNLOAD_DIR, download_name)
    # with open(download_path,'wb') as f:
    #     f.write(plain_text)
    # return download_name
    return path, plain_text

# key, nonce = encrypt_file("3408b253f823adf5d4e659e20b78a174","test.jpg")
# decrypt_file("./","test.enc", key, nonce)
