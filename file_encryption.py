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
    def encode(**params):
        input_file = params.get("input_file", "file")
        output_file = params.get("output_file", f"{input_file}.out")
        key_file = params.get("key_file", "None")
        keyfile_name = params.get("key_name", f"{input_file}.key")
        raw_key = b''
        result = ''
        try:
            raw_data = open(input_file, "rb").read()
        except IOError:
            result = f"input-file '{input_file}' not found."
        else:
            file_size = len(raw_data)
            if key_file == "None":
                key_file = f"{input_file}.key"
                raw_key = Crypter.generate_key(file_size)
                with open(keyfile_name, "wb") as key_out:
                    key_out.write(raw_key)
            else:
                try:
                    raw_key = open(key_file, "rb").read()
                except IOError:
                    result = f"key-file '{key_file}' not found"
                else:
                    key_size = len(raw_key)
                    if key_size < file_size:
                        raw_key += Crypter.generate_key(file_size - key_size)
                        with open(key_file, "wb") as key_out:
                            key_out.write(raw_key)
            if len(raw_key) > 0:
                encrypted = bytes(a ^ b for (a, b) in zip(raw_data, raw_key))
                with open(output_file, "wb") as encrypted_out:
                    encrypted_out.write(encrypted)
                result = f"encrypted '{input_file}' with '{key_file}' to '{output_file}'"
        return result
