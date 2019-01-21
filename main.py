#!/usr/bin/python3
import base64
import random
import sys
import argparse

from XorCipher import XorCipher
from misc import is_file_exists


def generate_key(key_length: int) -> bytes:
    return bytes([random.randint(0, 255) for _ in range(key_length)])


def save_key(key: bytes, file_name: str = "key.txt"):
    base64_key = base64.encodebytes(key)
    with open(file_name, "wb") as key_file:
        key_file.write(base64_key)


def read_key(file_name: str) -> bytes:
    with open(file_name, "rb") as key_file:
        key = key_file.read()
        return base64.decodebytes(key)


def main():
    arg_parser = argparse.ArgumentParser(description='Encode and decode file using xor and byteshift.')

    arg_parser.add_argument("file", help="File to encrypt.", type=str)

    arg_parser.add_argument("-k", "--key", help="Specify key value file in base64. If none automatically generated "
                                                "will be used and saved in key.txt."
                            , action="store", default="",
                            required=False, type=str)

    arg_parser.add_argument("-b", "--bit-shift", help="Specify bit shift. Positive numbers means right shift, "
                                                      "negative - left shift. Default: 0"
                            , action="store", default=0,
                            required=False, type=int)

    arg_parser.add_argument("-c", "--chunk-size", help="Specify chunk size of file to encrypt in bytes. Default: 1"
                            , action="store", default=1,
                            required=False, type=int)

    arg_parser.add_argument("-o", "--output", help="Specify output file name."
                            , action="store", default="file.out",
                            required=False, type=str)

    arg_parser.add_argument('-d', "--decrypt", dest='decrypt', action='store_const',
                            const=True, default=False,
                            help='Decrypt file.')

    args = arg_parser.parse_args()
    chunk_size = args.chunk_size
    bit_shift = args.bit_shift
    file_name = args.file
    key_file = args.key
    output_filename = args.output
    is_decrypting = args.decrypt

    if len(key_file) == 0:
        print(f"Generating random key with size of {chunk_size} bytes...")
        key = generate_key(chunk_size)
        save_key(key)
    else:
        if not is_file_exists(key_file):
            print("Key file is not existing/error reading it.")
            return -1
        key = read_key(key_file)

    if not is_file_exists(file_name):
        print("Target file is not existing/error reading it.")
        return -1

    if len(key) < chunk_size:
        print(f"Key length({len(key)}) should be greater or equal to chunk size({chunk_size})")

    xor_cipher = XorCipher(key=key, bitshift=bit_shift, chunk_size=chunk_size)
    if is_decrypting:
        xor_cipher.decrypt(output_filename, file_name)
    else:
        xor_cipher.encrypt(output_filename, file_name)


if __name__ == "__main__":
    sys.exit(main())
