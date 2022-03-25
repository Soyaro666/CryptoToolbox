import json
import random
import requests
import string


class QRandom:
    def generate_pwd(self, **params):
        pwd = ''
        num = params.get("num", 16)
        characters = params.get("charset", QRandom._alphabet())
        random.shuffle(characters)
        for i in range(num):
            rng = int(round(self.get(max=len(characters) - 1)))
            pwd += characters[rng]
        return pwd

    def get(self, **params):
        if not isinstance(self.seed, QRandom):
            self.seed = QRandom(length=self.length,
                                encoding=self.encoding,
                                size=self.size)
        start = params.get("min", 0)
        end = params.get("max", 0)
        if start > end:
            start, end = end, start
        rng = round(float(int(self.seed)), 5)
        rng = round(rng / 65535, 5)
        tmp = end - start
        result = round(rng * tmp, 5)
        result += start
        return result

    @staticmethod
    def _alphabet():
        characters = []
        remove = ['\n', '\r', '\t', '\x0b', '\x0c']
        for i in range(len(string.printable)):
            if string.printable[i] not in remove:
                characters.append(string.printable[i])
        return characters

    @staticmethod
    def _quantum(**params):
        length = str(params.get("length", 16))
        encoding = params.get("encoding", "uint8")
        size = params.get("size", 1)
        url = f"https://qrng.anu.edu.au/API/jsonI.php?length={length}&type={encoding}"
        if encoding == "hex16":
            size = str(params.get("size", 6))
            url = url + f"&size={size}"
        data = requests.get(url).text
        result = json.loads(data)
        return result

    def __int__(self):
        self.index += 1
        if self.index >= len(self._data):
            self.index -= len(self._data)
        return int(self._data[self.index])

    def __repr__(self):
        self.index += 1
        if self.index >= len(self._data):
            self.index -= len(self._data)
        return self._data[self.index]

    def __str__(self):
        self.index += 1
        if self.index >= len(self._data):
            self.index -= len(self._data)
        return str(f"random number: {self._data[self.index]}")

    def __init__(self, **params):
        self.index = 0
        self.seed = 0
        self._data = []
        codings = ["uint8", "uint16", "hex16"]
        self.length = params.get("length", 1024)
        if self.length > 1024:
            self.length = 1024
        self.encoding = params.get("encoding", "uint16")
        if self.encoding not in codings:
            raise ValueError(f"encoding must be one of: {str(codings)}")
        self.size = params.get("size", 1)
        tmp_data = QRandom._quantum(length=self.length,
                                    encoding=self.encoding,
                                    size=self.size)
        if tmp_data["success"]:
            self._data = tmp_data["data"]
        else:
            raise Exception("error in contacting qrng.anu.edu.au")
