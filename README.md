# XOR-cipher

Simple XOR file encryption with ability of generating keys in base64 of nothing provided and bit shift.

  **-h, --help** - show help message  
  **-k KEY, --key KEY** - Specify key value file in base64. If none automatically generated will be used and saved in key.txt.  
  **-b BIT_SHIFT, --bit-shift BIT_SHIFT** - Specify bit shift. Positive numbers means right shift, negative - left shift. Default: 0  
  **-c CHUNK_SIZE, --chunk-size CHUNK_SIZE** - Specify chunk size of file to encrypt in bytes. Default: 1  
  **-o OUTPUT, --output OUTPUT** - Specify output file name.  
  **-d, --decrypt** - Decrypt file.  
Example:  
`python3 main.py --key=key.txt --output=encrypted.txt --chunk-size=10 --bit-shift=10 ./target.txt`  
`python3 main.py --key=key.txt --output=decrypted.txt --chunk-size=10 --bit-shift=-10 --decrypt ./encrypted.txt`  