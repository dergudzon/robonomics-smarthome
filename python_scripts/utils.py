from substrateinterface import SubstrateInterface, Keypair
import nacl.secret
import base64
import configparser

def read_config(path: str) -> Keypair:
    config = configparser.ConfigParser()
    config.read(path)
    mnemonic = config.get('secrets', 'MNEMONIC_SEED')
    keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=32)
    return keypair

def connect_robonomics() -> SubstrateInterface:
    substrate = SubstrateInterface(
            url="wss://main.frontier.rpc.robonomics.network",
            ss58_format=32,
            type_registry_preset="substrate-node-template",
            type_registry= {
                "types": {
                    "Record": "Vec<u8>",
                    "Parameter": "Bool",
                    "LaunchParameter": "Bool",
                    "<T as frame_system::Config>::AccountId": "AccountId",
                    "RingBufferItem": {
                        "type": "struct",
                        "type_mapping": [["timestamp", "Compact<u64>"], ["payload", "Vec<u8>"]],
                    },
                    "RingBufferIndex": {
                        "type": "struct",
                        "type_mapping": [["start", "Compact<u64>"], ["end", "Compact<u64>"]],
                    },
                }
            }
            )
    return substrate

def encrypt(seed: str, data: str) -> str:
    b = bytes(seed[0:32], "utf8")
    box = nacl.secret.SecretBox(b)
    data = bytes(data, 'utf-8')
    encrypted = box.encrypt(data)
    text = base64.b64encode(encrypted).decode("ascii")
    return text

def decrypt(seed: str, encrypted_data: str) -> str:
    b = bytes(seed[0:32], "utf8")
    box = nacl.secret.SecretBox(b)
    decrypted = box.decrypt(base64.b64decode(encrypted_data))
    return decrypted