from substrateinterface import SubstrateInterface, Keypair
import time
import sys
import binascii
import nacl.secret
import base64
import configparser
from utils import read_config, connect_robonomics, encrypt, decrypt


if __name__ == '__main__':
    keypair = read_config('python_scripts/config.config')
    substrate = connect_robonomics()
    seed = keypair.seed_hex
    data = ' '.join(sys.argv[1:])
    text = encrypt(seed, data)

    print(f"Got message: {data}")
    call = substrate.compose_call(
            call_module="Datalog",
            call_function="record",
            call_params={
                'record': text
            }
        )
    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print(f"Datalog created with extrinsic hash: {receipt.extrinsic_hash}")
