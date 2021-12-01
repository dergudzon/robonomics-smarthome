from substrateinterface import SubstrateInterface, Keypair
import time
import sys
import binascii
import nacl.secret
import base64
import configparser

config = configparser.ConfigParser()
config.read('/srv/homeassistant/python_scripts/config.config')
mnemonic = config.get('secrets', 'MNEMONIC_SEED')

substrate = SubstrateInterface(
                    url="wss://main.frontier.rpc.robonomics.network",
                    ss58_format=32,
                    type_registry_preset="substrate-node-template",
                    type_registry={
                        "types": {
                            "Record": "Vec<u8>",
                            "<T as frame_system::Config>::AccountId": "AccountId",
                            "RingBufferItem": {
                                "type": "struct",
                                "type_mapping": [
                                    ["timestamp", "Compact<u64>"],
                                    ["payload", "Vec<u8>"],
                                ],
                            },
                        }
                    }
                )

keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=32)
seed = keypair.seed_hex
b = bytes(seed[0:32], "utf8")
box = nacl.secret.SecretBox(b)
data = ' '.join(sys.argv[1:])
data = bytes(data, 'utf-8')

encrypted = box.encrypt(data)
text = base64.b64encode(encrypted).decode("ascii")
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
