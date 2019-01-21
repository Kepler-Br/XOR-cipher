class XorCipher(object):
    def __init__(self, key: bytes, bitshift: int, chunk_size: int):
        self.key = key
        self.bitshift = bitshift
        self.chunk_size = chunk_size

    def cycle_right_shift(self, val, r_bits, max_bits):
        return ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
        (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))

    def cycle_left_shift(self, val, r_bits, max_bits):
        return (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
        ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

    def encrypt(self, output_filename, source_file):
        output_file = open(output_filename, "wb")
        source_file = open(source_file, "rb")

        while source_file:
            chunk = source_file.read(self.chunk_size)
            # if EOF
            if len(chunk) == 0:
                break

            for source_byte, key_byte in zip(chunk, self.key):
                encoded_byte = source_byte ^ key_byte
                if self.bitshift > 0:
                    encoded_byte = self.cycle_right_shift(encoded_byte, self.bitshift, 8)
                if self.bitshift < 0:
                    encoded_byte = self.cycle_left_shift(encoded_byte, abs(self.bitshift), 8)
                output_file.write(encoded_byte.to_bytes(1, byteorder="big"))

    def decrypt(self, output_filename, source_file):
        output_file = open(output_filename, "wb")
        source_file = open(source_file, "rb")

        while source_file:
            chunk = source_file.read(self.chunk_size)
            # if EOF
            if len(chunk) == 0:
                break

            for source_byte, key_byte in zip(chunk, self.key):
                encoded_byte = source_byte
                if self.bitshift > 0:
                    encoded_byte = self.cycle_right_shift(encoded_byte, self.bitshift, 8)
                elif self.bitshift < 0:
                    encoded_byte = self.cycle_left_shift(encoded_byte, abs(self.bitshift), 8)
                encoded_byte = encoded_byte ^ key_byte
                output_file.write(encoded_byte.to_bytes(1, byteorder="big"))
