import time
import json, pycurl
import base64
from utils import read_config, connect_robonomics, encrypt, decrypt

def request_sender(command: dict, url: str) -> None:
    data = json.dumps(command)
    try:
        c = pycurl.Curl()
        c.setopt(pycurl.POST, 1)
        c.setopt(pycurl.POSTFIELDS, data)
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
        c.perform()
    except Exception as e:
        print(e)

def listener(seed: str, address: str) -> None:
    substrate = connect_robonomics()
    while True:
        ch = substrate.get_chain_head()
        print(f"Chain head: {ch}")
        events = substrate.get_events(ch)
        for e in events:
            if e.value["event_id"] == "NewRecord":
                print(f"new record {e}")
                print(e.params[1]["value"])
                if e.params[0]["value"] == address:
                    print(f"new record {e}")
                    for p in e.params:
                        print(p)
                        if p["type"] == "Record":
                            try:
                                data = bytes.fromhex(p['value'][2:]).decode('utf-8')
                                print(f"data: {data}")
                                decrypted = decrypt(seed, data)
                                print(f"decrypted {decrypted}")
                                order = json.loads(decrypted)
                                agent = order["agent"]
                                del order["agent"]
                                request_sender(order, "http://localhost:8123/api/webhook/" + agent)
                            except Exception as e:
                                print(f"Exception: {e}")
        time.sleep(12)

if __name__ == '__main__':
    keypair = read_config('python_scripts/config.config')
    seed = keypair.seed_hex
    address = keypair.ss58_address
    listener(seed, address)

