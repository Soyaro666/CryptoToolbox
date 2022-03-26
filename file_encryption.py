from qrandom import QRandom


class Crypter:
    @staticmethod
    def generate_key(data_amount):
        tmp_key = []
        key = b''
        call_amount = 1
        max_string_amount = 1024
        max_string_size = 1024
        string_size = 1
        max_call_size = max_string_amount * max_string_size
        while data_amount > max_call_size:
            call_amount += 1
            data_amount -= max_call_size
        while data_amount > max_string_amount:
            string_size += 1
            data_amount -= max_string_amount
        while call_amount > 1:
            call_amount -= 1
            rng = QRandom(encoding="hex16", size=max_string_size, length=max_string_amount)
            for i in range(max_string_amount):
                tmp_key.append(repr(rng))
        if string_size > 1:
            string_size -= 1
            rng = QRandom(encoding="hex16", size=string_size, length=max_string_amount)
            for i in range(max_string_amount):
                tmp_key.append(repr(rng))
        if data_amount > 0:
            rng = QRandom(encoding="hex16", length=data_amount)
            for i in range(data_amount):
                tmp_key.append(repr(rng))
        for string in tmp_key:
            for i in range(0, len(string), 2):
                key += (bytes.fromhex(string[i:i + 2]))
        return key

    @staticmethod
    def encrypt(filename):
        try:
            raw_data = open(filename, "rb").read()
        except IOError:
            print(f"file {filename} not found.")
        else:
            file_size = len(raw_data)
            raw_key = Crypter.generate_key(file_size)
            with open(filename + ".key", "wb") as key_out:
                key_out.write(raw_key)
            encrypted = bytes(a ^ b for (a, b) in zip(raw_data, raw_key))
            with open(filename + ".dat", "wb") as encrypted_out:
                encrypted_out.write(encrypted)

    @staticmethod
    def decrypt(**params):
        filename = params.get("filename", "file")
        crypt_file = params.get("crypt_file", f"{filename}.dat")
        key_file = params.get("keyfile", f"{filename}.key")
        try:
            encrypted_data = open(crypt_file, "rb").read()
        except IOError:
            print(f"encrypted file '{crypt_file}' not found.")
        else:
            try:
                raw_key = open(key_file, "rb").read()
            except IOError:
                print(f"key-file '{key_file}' not found")
            else:
                raw_data = bytes(a ^ b for (a, b) in zip(encrypted_data, raw_key))
                with open("d_" + filename, "wb") as decrypted_out:
                    decrypted_out.write(raw_data)
