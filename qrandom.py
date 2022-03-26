import json
import random
import requests
import string
import secrets


class QRandom:
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
        url = f"https://qrng.anu.edu.au/API/jsonI.php?length={length}&type={encoding}"
        if encoding == "hex16":
            size = str(params.get("size", 1))
            url = f"{url}&size={size}"
        data = requests.get(url).text
        result = json.loads(data)
        return result

    def generate_pwd(self, **params):
        pwd = ''
        num = params.get("num", 16)
        characters = params.get("charset", QRandom._alphabet())
        random.shuffle(characters)
        for i in range(num):
            rng = int(round(self.get(max=len(characters)-1)))
            pwd += characters[rng]
        return pwd

    def get(self, **params):
        start = int(params.get("min", 0))
        end = int(params.get("max", 0))
        if start > end:
            start, end = end, start
        rng = round(float(self), 5)
        rng = round(rng / 65535, 5)
        tmp = end - start
        result = round(rng * tmp, 5)
        result += start
        return result

    def set(self):
        tmp_data = {"success": False}
        try:
            tmp_data = QRandom._quantum(length=self.length,
                                        encoding=self.encoding,
                                        size=self.size)
        except (ConnectionError, TimeoutError):
            tmp_rng = []
            if self.encoding == "hex16":
                for i in range(self.length):
                    tmp_rng.append([])
                    for j in range(self.size):
                        tmp_rng[-1].append(secrets.token_hex(1))
            elif self.encoding == "uint16":
                for i in range(self.length):
                    tmp_rng.append(secrets.randbelow(65535))
            elif self.encoding == "uint8":
                for i in range(self.length):
                    tmp_rng.append(secrets.randbelow(255))
            tmp_data = {"success": True, "data": tmp_rng}
        if tmp_data["success"]:
            self._data = tmp_data["data"]
        else:
            raise Exception("error in QRandom.set(): success = False")
        self.index = 0
        return True

    def __int__(self):
        result = int(self._data[self.index])
        self.index += 1
        if self.index > len(self._data):
            self.set()
        return result

    def __float__(self):
        result = float(self._data[self.index])
        self.index += 1
        if self.index > len(self._data):
            self.set()
        return result

    def __repr__(self):
        result = self._data[self.index]
        self.index += 1
        if self.index > len(self._data):
            self.set()
        return result

    def __str__(self):
        result = str(f"random number: {self._data[self.index]}")
        self.index += 1
        if self.index > len(self._data):
            self.set()
        return result

    def __init__(self, **params):
        self.index = 0
        self._data = []
        codings = ["uint8", "uint16", "hex16"]
        self.length = params.get("length", 1024)
        if self.length > 1024:
            self.length = 1024
        self.encoding = params.get("encoding", "uint16")
        if self.encoding not in codings:
            raise ValueError(f"encoding must be one of: {str(codings)}")
        self.size = params.get("size", 1)
        self.set()
