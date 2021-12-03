from substrateinterface import SubstrateInterface, Keypair
import binascii
import base64
import nacl.secret
import os
import sys

text = str(sys.argv[1])
print(f"Got {text}")
mnemonic = os.environ['MNEMONIC_SEED']
keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=32)
seed = keypair.seed_hex
b = bytes(seed[0:32], "utf8")
box = nacl.secret.SecretBox(b)
decrypted = box.decrypt(base64.b64decode(text))
print(decrypted)
