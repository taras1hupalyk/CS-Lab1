import base64

import Base64Coder


class Base64(object):
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    def chunk(self, data, length):
        return [data[i:i + length] for i in range(0, len(data), length)]

    def encode(self, data):
        override = 0
        if len(data) % 3 != 0:
            override = (len(data) + 3 - len(data) % 3) - len(data)
        data += b"\x00" * override

        threechunks = self.chunk(data, 3)

        binstring = ""
        for chunk in threechunks:
            for x in chunk:
                binstring += "{:0>8}".format(bin(x)[2:])

        sixchunks = self.chunk(binstring, 6)

        outstring = ""
        for element in sixchunks:
            outstring += self.CHARS[int(element, 2)]

        outstring = outstring[:-override] + "=" * override
        return outstring


if __name__ == "__main__":
    b64 = Base64()
    print(b64.encode(b"Hello"))
    print(base64.b64encode(b"Hello").decode('utf-8'))
