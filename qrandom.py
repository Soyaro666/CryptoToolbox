import json
import random
import requests
import string
import secrets


class QRandom:
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

    def _set(self):
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
            raise Exception("error in QRandom._set(): success = False")
        self.index = 0
        return True

    @staticmethod
    def alphabet():
        """returns a full _set of printable characters"""
        characters = []
        remove = ['\n', '\r', '\t', '\x0b', '\x0c']
        for i in range(len(string.printable)):
            if string.printable[i] not in remove:
                characters.append(string.printable[i])
        return characters

    def generate_pwd(self, **params):
        """generates a password based on a quantum random generator

        possible params:
        num (optional) defines the length of the password
        defaults to 16 if not specified

        charset (optional) a list of characters you want to generate a password from
        defaults to the QRandom-method alphabet() if not specified"""

        pwd = ''
        num = params.get("num", 16)
        characters = params.get("charset", self.alphabet())
        while num > 1024:
            pwd += self.generate_pwd(num=1024, charset=characters)
            num -= 1024
        random.shuffle(characters)
        for i in range(num):
            rng = int(round(self.get(max=len(characters)-1)))
            pwd += characters[rng]
        return pwd

    def get(self, **params):
        """generates a random float-type number between two given numbers

        possible params:
        min: integer or float
        max: integer or float
        if one is specified the random number will be between (including) 0 and the given number
        if both are specified the random number will be between (including) both given numbers"""
        start = float(params.get("min", 0))
        end = float(params.get("max", 0))
        num_range = end - start
        encoding_max = {"uint8": 255, "uint16": 65535}[self.encoding]
        digits = len(str(encoding_max)) * 2
        count = 1
        if start > end:
            start, end = end, start
        rng = round(float(self), digits)
        total_max = num_range - encoding_max
        while total_max > encoding_max:
            rng += round(float(self), digits)
            count += 1
            total_max = num_range - (encoding_max * count)
        rng = round(rng / (encoding_max * count), digits)
        result = round(rng * num_range, digits)
        result += start
        return result

    def __int__(self):
        result = int(self._data[self.index])
        self.index += 1
        if self.index >= len(self._data):
            self._set()
        return result

    def __float__(self):
        result = float(self._data[self.index])
        self.index += 1
        if self.index >= len(self._data):
            self._set()
        return result

    def __str__(self):
        result = str(self._data[self.index])
        self.index += 1
        if self.index >= len(self._data):
            self._set()
        return result

    def __repr__(self):
        result = self._data[self.index]
        self.index += 1
        if self.index >= len(self._data):
            self._set()
        return result

    def __init__(self, **params):
        """creates a QRandom-Object that can be used to create quantum-random numbers

        possible parameters:
        length (optional, can be 1 to 1024, defaults to 1024)
        defines the amount of random values the object prepares

        encoding: (optional, can be 'uint8', 'uint16' or 'hex16', defaults to 'uint16')
        if value is 'uint8' the object will generate random values between 0 and 255
        if value is 'uint16' the object will generate random values between 0 and 65535
        if value is 'hex16' the object will generate [size] random values between 00 and ff per number

        size: (optional, can be 1 to 1024)
        defaults to 1 if encoding is hex16
        is ignored if encoding is not hex16

        if at any given time the QRNG-api isn't available the code defaults to using
        pythons secrets-module to generate random values according to the given parameters"""
        self.index = 0
        self._data = []
        codings = ["uint8", "uint16", "hex16"]
        self.length = params.get("length", 1024)
        if self.length > 1024:
            self.length = 1024
        self.encoding = "uint16"
        encoding = params.get("encoding", "uint16")
        self.size = params.get("size", 1)
        if encoding not in codings:
            raise ValueError(f"encoding must be one of: {str(codings)}")
        else:
            self.encoding = encoding
        self._set()
