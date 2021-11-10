from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
import time
import os
from urllib import request, parse
import json, pycurl
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import base64
import nacl.secret

mnemonic = os.environ['MNEMONIC_SEED']
keypair = Keypair.create_from_mnemonic(mnemonic, ss58_format=32)
seed = keypair.seed_hex
b = bytes(seed[0:32], "utf8")
box = nacl.secret.SecretBox(b)

def connect():
    try:
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
    except ConnectionRefusedError:
        print("?? No local Substrate node running, try running 'start_local_substrate_node.sh' first")
        exit()
        
def request_sender(command: dict, url: str):
    data = json.dumps(command)
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
        c.setopt(pycurl.VERBOSE, 1)
        c.perform()
    except Exception as e:
        print(e)

def listener():
    substrate = connect()
    agents = [
        "4Hd5Zkcu1qubGBi6Lxn59eoZ88osfN53TzxXTVTKUBaEeAuM"
        ]
    agent_public_keys = []
    for a in agents:
        agent_public_keys.append({'type': 'AccountId', 'value': a})
    while True:
            ch = substrate.get_chain_head()
            print(f"Chain head: {ch}")
            events = substrate.get_events(ch)
            for e in events:
                if e.value["event_id"] == "NewRecord":
                    if any(x in e.params for x in agent_public_keys):
                        print(f"new record {e}")
                        for p in e.params:
                            print(p)
                            if p["type"] == "Record":
                                decrypted = box.decrypt(base64.b64decode(p["value"]))
                                print(f"decrypted {decrypted}")
                                try:
                                    order = json.loads(decrypted)
                                    agent = order["agent"]
                                    del order["agent"]
                                    request_sender(order, "http://localhost:8123/api/webhook/" + agent)  
                                except Exception as e:
                                    print(f"Exception: {e}")
            time.sleep(12)

listener()
