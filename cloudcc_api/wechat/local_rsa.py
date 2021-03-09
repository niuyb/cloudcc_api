#!/usr/bin/env python
# encoding: utf-8
# 作者：Ksar4
# 日期：2021/3/9 15:40
# 工具：PyCharm
# Python版本：3.7.0

import base64

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA


class RSACipher(object):
    _private_pem ="""MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQC/M6P6gHc4/+L+
                     Is7k3ekYYRdYvJBsHR4C0IbtW760hMrubRKxguc03N0khQRYkjXtZwB9F3tMNOb3
                     s/AJybDX1qYleCEdy2UoudjcJel4LpCxRMkKFmO/j3U4lavT1TnJ2Sw77KeMS8+U
                     BL/oo9ZpunZ7ZuFdcJ0O6OHbYnPirarls5B6z0TwYWy1vMtnPMw92QQpXJOaazcj
                     sRwKnKmFOTdUxwIwxIIiEFdFIewoZltXMttH3FfpxTITjOgmNbyCTcNvsjTHRr63
                     DM1r3OWvIDGNYa81ClQLV6G/9w/J5FkY3eOI9DfftGh582EM4oJ3YDyyYrNCZcz9
                     xbOGya7bAgMBAAECggEBAL6K2QyIP8f3AiCfUa21FFluUJTm/cowTjsh0oTynB9M
                     AuwOmMV8HauJu3xsbwNRWhqnPk5rOz2brt0FXd5zOCAw0kye5enKS5qFcv8ZbQyO
                     4zU1xl+eJnO9pGTqi11Erh1gpvtlASgIWOo6vYE63S9qWi7qPQcgdfRo0sQN3kzz
                     ak5X1JcyzaB3wuUe5tr9ZgnO5XenLCQzsYptLr8sXnExfLEbVNVkGYvxlcHf5XZE
                     Os0OOo4E2SfxfrEesiDqHeLKkwVmC8UK9qlAn4LklSMZDIsif3EhmmD+dyHZwyC7
                     wNpuVcrcyRaAcu8a5ssCN3uoW7LIVGIGhZjhxxblC9kCgYEA4Dtxfi2cg/j/Zin/
                     +zUeVKvhOEYVWidtnsP//6bVj6WVsjFuBRpIE6Qa2nYL7xVeI3cyClPIeDtQgzHy
                     q46+pwhkKw1V7V0viB2/H/Za40F3R6BZ1TZTGjAcTXW9yQ+TbD315oDDoRXcNahG
                     2j4trqQfuDPY/in2BxVkWJt7g/0CgYEA2ko7iaALLFp+v21ZTsN39jMOcYRNG9OU
                     p2XGvDjmTK26uaXntpbNRpvco0Rtd5+UDbWokchPAHl8ehiYLomAkQKUQJAzgGgX
                     uVf//2wHlcyBFkfUnWLRKSPxZC3fdtAVLMDh7XtTNEL2HKyoKBGHjIm5DRNwjNGu
                     rpN4Wij3ObcCgYBSDM5Zunz0Oa/TBXlaxbQkjYRrIBH+HEFbgCLzvGuXFaMyQi4d
                     BeHr9fexitKRGMOKvLn912yaujGa4DMJHcGbw1FMA6Q2qAuVhjUCkBXv5GuuNPnK
                     MAe2pHYmzfe1U9LBH+cUAngTQLmElN/gSjJTHlFRCP/U+SvCqcw/NB29TQKBgQDF
                     b5biJ8tzVnaFldXNE6cRG6TYr50+qeQudDOIUr6aZBgbih9GWqdYUekCEwYfyEoV
                     DFVnZhFukHMxy8T5cozCm96TdtneLkgm750v3PoPV2T6TgXURGiCGWxf+82+nP5J
                     +DtgnMbo4hfQX6nIc/Jx/q9NUGPgOlcQt3mHsr3JiQKBgQDHTw6ol8JBao9m1etx
                     VFwF2iu0e9oTs8Bi9n5YgS0D2mAuxzUs9kBVzDMuvS2NArZGuxY1RCrDlJKp+8Hu
                     RtC7e6hJEJoOat7QivNjAO95I3gfrlVbR5XVtJ51Bve+Eh71rhEQd7X6CrErhpbz
                     aIqA/AS1LKRDU2AltvTDCx9eSA=="""

    _public_pem = """MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvzOj+oB3OP/i/iLO5N3p
                     GGEXWLyQbB0eAtCG7Vu+tITK7m0SsYLnNNzdJIUEWJI17WcAfRd7TDTm97PwCcmw
                     19amJXghHctlKLnY3CXpeC6QsUTJChZjv491OJWr09U5ydksO+ynjEvPlAS/6KPW
                     abp2e2bhXXCdDujh22Jz4q2q5bOQes9E8GFstbzLZzzMPdkEKVyTmms3I7EcCpyp
                     hTk3VMcCMMSCIhBXRSHsKGZbVzLbR9xX6cUyE4zoJjW8gk3Db7I0x0a+twzNa9zl
                     ryAxjWGvNQpUC1ehv/cPyeRZGN3jiPQ337RoefNhDOKCd2A8smKzQmXM/cWzhsmu
                     2wIDAQAB"""

    def __init__(self):
        _random_generator = Random.new().read
        _rsa = RSA.generate(1024, _random_generator)
        self._private_pem = _rsa.exportKey()
        self._public_pem = _rsa.publickey().exportKey()

    def get_public_key(self):
        return self._public_pem

    def get_private_key(self):
        return self._private_pem

    # def load_keys(self):
    #     with open('master-public.pem', "r") as f:
    #         self._public_pem = f.read()
    #     with open('master-private.pem', "r") as f:
    #         self._private_pem = f.read()
    #
    # def save_keys(self):
    #     with open('master-public.pem', 'wb') as f:
    #         f.write(self._public_pem)
    #     with open('master-private.pem', 'wb') as f:
    #         f.write(self._private_pem)

    def decrypt_with_private_key(self, _cipher_text):
        _rsa_key = RSA.importKey(self._private_pem)
        _cipher = Cipher_pkcs1_v1_5.new(_rsa_key)
        _text = _cipher.decrypt(base64.b64decode(_cipher_text), "ERROR")
        return _text.decode(encoding="utf-8")

    def encrypt_with_public_key(self, _text):
        _rsa_key = RSA.importKey(self._public_pem)
        _cipher = Cipher_pkcs1_v1_5.new(_rsa_key)
        _cipher_text = base64.b64encode(_cipher.encrypt(_text.encode(encoding="utf-8")))
        return _cipher_text

    # encrypt with private key & decrypt with public key is not allowed in Python
    # although it is allowed in RSA
    def encrypt_with_private_key(self, _text):
        _rsa_key = RSA.importKey(self._private_pem)
        _cipher = Cipher_pkcs1_v1_5.new(_rsa_key)
        _cipher_text = base64.b64encode(_cipher.encrypt(_text.encode(encoding="utf-8")))
        return _cipher_text

    def decrypt_with_public_key(self, _cipher_text):
        _rsa_key = RSA.importKey(self._public_pem)
        _cipher = Cipher_pkcs1_v1_5.new(_rsa_key)
        _text = _cipher.decrypt(base64.b64decode(_cipher_text), "ERROR")
        return _text.decode(encoding="utf-8")


if __name__ == "__main__":
    cipher = RSACipher()
    # cipher.save_keys()
    # cipher.load_keys()

    text = 'Encrypt with public key, and decrypt with private key'

    # 公钥加密
    cipherText = cipher.encrypt_with_public_key(text)
    print(cipherText)

    # 私钥解密
    plainText = cipher.decrypt_with_private_key(cipherText)
    print(plainText)

    # # RSA算法本身允许私钥加密公钥解密，实际python不允许
    # # raise TypeError("No private key")
    # cipherText = cipher.encrypt_with_private_key(text)
    # plainText = cipher.decrypt_with_public_key(cipherText)