import os, time, pathlib, tempfile, subprocess, binascii
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

ENC_KEY_HEX = os.getenv("ENC_KEY_HEX","").strip()
IPNS_KEY = os.getenv("IPNS_KEY","self")
EVENT_LOG = pathlib.Path(os.path.expanduser(os.getenv("EVENT_LOG","~/.adult_replica/events.jsonl")))
assert ENC_KEY_HEX, "ENC_KEY_HEX not set"
KEY = binascii.unhexlify(ENC_KEY_HEX)
assert len(KEY) in (16,24,32), "ENC_KEY_HEX must be 16/24/32 bytes (hex)"

def encrypt(data: bytes) -> bytes:
    iv = get_random_bytes(12)
    cipher = AES.new(KEY, AES.MODE_GCM, nonce=iv)
    ct, tag = cipher.encrypt_and_digest(data)
    return b"v1"+iv+tag+ct

def ipfs_add_bytes(payload: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(payload); f.flush()
        cid = subprocess.check_output(["ipfs","add","-Q",f.name]).decode().strip()
    return cid

def ipns_publish(cid: str):
    subprocess.check_call(["ipfs","name","publish",f"/ipfs/{cid}","--key",IPNS_KEY,"--lifetime","8760h"])

def main():
    last = -1
    EVENT_LOG.parent.mkdir(parents=True, exist_ok=True)
    while True:
        if EVENT_LOG.exists():
            data = EVENT_LOG.read_bytes()
            if len(data) != last and len(data) > 0:
                cid = ipfs_add_bytes(encrypt(data))
                ipns_publish(cid)
                print(f"[ok] published CID {cid}", flush=True)
                last = len(data)
        time.sleep(5)

if __name__ == "__main__":
    main()
