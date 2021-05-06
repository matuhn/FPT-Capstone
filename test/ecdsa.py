from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Math.Numbers import Integer

m = b'khongcogi'
h = SHA256.new(m)

ecc_private_key = ECC.generate(curve='P-256')
ecc_public_key = ecc_private_key.public_key()

sign = DSS.new(ecc_private_key, 'fips-186-3').sign(h)

h = SHA256.new(b'khong')
h.update(b'cogi')
h.digest()

try:
    DSS.new(ecc_public_key, 'fips-186-3').verify(h, sign)
    print("The message is authentic.")
except ValueError:
    print("The message is not authentic.")
