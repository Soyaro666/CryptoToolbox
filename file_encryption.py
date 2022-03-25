from qrandom import QRandom
import json

class Crypter:
    @staticmethod
    def generate_key(data_amount):
        tmp_key = []
        key = []
        call_amount = 0
        max_string_amount = 1024
        max_string_size = 1024
        string_size = 0
        max_call_size = max_string_amount * max_string_size
        # rng = QRandom(encoding="hex16", size=key_size)
        while data_amount > max_call_size:
            call_amount += 1
            data_amount -= max_call_size
        while data_amount > max_string_amount:
            string_size += 1
            data_amount -= max_string_amount
        while call_amount > 0:
            call_amount -= 1
            rng = QRandom(encoding="hex16", size=max_string_size, length=max_string_amount)
            for i in range(max_string_amount):
                tmp_key.append(repr(rng))
        if string_size > 0:
            rng = QRandom(encoding="hex16", size=string_size, length=max_string_amount)
            for i in range(max_string_amount):
                tmp_key.append(repr(rng))
        if data_amount > 0:
            rng = QRandom(encoding="hex16", length=data_amount)
            for i in range(data_amount):
                tmp_key.append(repr(rng))
        for string in tmp_key:
            for i in range(0, len(string), 2):
                key.append(string[i:i + 2])
        return key

    @staticmethod
    def encrypt(filename):
        raw_data = open(filename, "rb").read()

        file_size = len(raw_data)
        print(f"required values: {file_size}")
        raw_key = Crypter.generate_key(file_size)
        key_file = json.dumps(raw_key)
        with open(filename + ".key", "w") as key_out:
            key_out.write(key_file)
        encrypted = bytes(a ^ b for (a, b) in zip(raw_data, raw_key))
        with open(filename + ".dat", "wb") as encrypted_out:
            encrypted_out.write(encrypted)

    @staticmethod
    def decrypt(filename):
        encrypted_data = open(filename + ".dat", "rb").read()
        key_file = open(filename + ".key", "r").read()
        raw_key = json.loads(key_file)
        raw_data = bytes(a ^ b for (a, b) in zip(encrypted_data, raw_key))
        with open("d_" + filename, "wb") as decrypted_out:
            decrypted_out.write(raw_data)


Crypter.encrypt("qrandom.py")
Crypter.decrypt("qrandom.py")
