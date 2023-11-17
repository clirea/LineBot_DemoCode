from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from ..environment import ChannelSecret

key = ChannelSecret.encode()

class AESCipher:
    def __init__(self):
        self.key = key

    def encrypt(self, text: str) -> str:
        if text is None:
            return None
        cipher = AES.new(self.key, AES.MODE_ECB)
        padded_text = pad(text.encode('utf-8'), AES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        return encrypted_text.hex()

    def decrypt(self, encrypted_text: str) -> str:
        if encrypted_text is None:
            return None
        cipher = AES.new(self.key, AES.MODE_ECB)
        decrypted_text = cipher.decrypt(bytes.fromhex(encrypted_text))
        unpadded_text = unpad(decrypted_text, AES.block_size)
        return unpadded_text.decode('utf-8')