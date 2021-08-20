#!/usr/bin/python3

import base64
import binascii
import sys
import argparse
from typing import BinaryIO
from io import BytesIO
import io


def open_key(file_path: str, stream: bool) -> BinaryIO:
    file_handler = open(file_path, 'rb')

    if stream:
        return file_handler

    key = file_handler.read()

    return BytesIO(key)


def open_binary_file(file_path: str, mode: str, default: BinaryIO) -> BinaryIO:
    if file_path is None:
        return default
    else:
        if mode == 'w':
            return open(file_path, 'wb')
        elif mode == 'r':
            return open(file_path, 'rb')
    raise ValueError(f'invalid mode: \'{mode}\'')


def parse_arguments():
    arg_parser = argparse.ArgumentParser(description='Cipher file using xor.')

    arg_parser.add_argument('-k', '--key', help='Specify a binary key file. '
                                                'If --base64 specified, key will be interpreted as base64 encoded.',
                            action='store', required=True, type=str)

    arg_parser.add_argument('-b', '--base64', help='Interpret --key file as base64 encoded key.',
                            action='store_true', required=False)

    arg_parser.add_argument('-s', '--stream_key', help='Should you to stream a key. '
                                                       'In case if you\'re using key that is larger than RAM.',
                            action='store_true', required=False)

    arg_parser.add_argument('-i', '--input', help='File to encrypt. If not specified, stdin used instead.',
                            required=False, type=str)

    arg_parser.add_argument('-o', '--output', help='Specify output file name. If not specified, stdout used instead.',
                            required=False, type=str)

    return arg_parser.parse_args()


def read_key_buffer(key_buffer: BinaryIO, chunk_size: int, use_base64: bool) -> bytes:
    chunk = key_buffer.read(chunk_size)

    if len(chunk) < chunk_size - 1:
        key_buffer.seek(0, io.SEEK_SET)
    if use_base64:
        return base64.decodebytes(chunk)

    return chunk


def buffer_length(buffer: BinaryIO) -> int:
    current_position = buffer.tell()

    buffer.seek(0, io.SEEK_END)

    length = buffer.tell()

    buffer.seek(current_position, io.SEEK_SET)

    return length


def encrypt(output_buffer: BinaryIO, input_buffer: BinaryIO, key_buffer: BinaryIO, use_base64: bool):
    chunk_size = 1024

    while True:
        key_buffer_chunk = read_key_buffer(key_buffer, chunk_size, use_base64)
        input_buffer_chunk = input_buffer.read(len(key_buffer_chunk))

        if len(input_buffer_chunk) == 0:
            break

        output_chunk = bytearray(len(input_buffer_chunk))
        index = 0

        while index < len(input_buffer_chunk):
            output_chunk[index] = input_buffer_chunk[index] ^ key_buffer_chunk[index]
            index += 1

        output_buffer.write(output_chunk)


def main():
    args = parse_arguments()

    input_filename = args.input
    output_filename = args.output
    key_filename = args.key
    use_base64 = args.base64
    stream_key = args.stream_key

    try:
        output_buffer = open_binary_file(output_filename, 'w', sys.stdout.buffer)
    except OSError as e:
        print(f'Cannot write to \'{output_filename}\': {e.strerror}', file=sys.stderr)
        return 1

    try:
        input_buffer = open_binary_file(input_filename, 'r', sys.stdin.buffer)
    except OSError as e:
        print(f'Cannot open output file \'{output_filename}\': {e.strerror}', file=sys.stderr)
        return 1

    try:
        key_buffer = open_key(key_filename, use_base64)
    except OSError as e:
        print(f'Cannot open key file \'{key_filename}\': {e.strerror}', file=sys.stderr)
        return 1

    if buffer_length(key_buffer) == 0:
        print(f'Key file \'{key_filename}\' is empty', file=sys.stderr)
        return 1

    try:
        encrypt(output_buffer, input_buffer, key_buffer, use_base64)
    except binascii.Error as e:
        print(f'Invalid base64 key: {e}', file=sys.stderr)
        return 1

    if output_buffer != sys.stdout.buffer:
        output_buffer.close()

    if input_buffer != sys.stdin.buffer:
        input_buffer.close()

    if stream_key:
        key_buffer.close()


if __name__ == '__main__':
    sys.exit(main())
