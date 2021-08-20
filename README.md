# XOR-cipher

Simple XOR file encryption script.

| Short key     | Long key      | Description                                                                                  | Type          | Required      |
| ------------- | ------------- | -------------                                                                                | ------------- | ------------- |
| -h            | --help        | Show help                                                                                    | Flag          | No            |
| -k            | --key         | Specify a binary key file. If --base64 specified, key will be interpreted as base64 encoded. | String        | Yes           |
| -b            | --base64      | Interpret --key file as base64 encoded key.                                                  | Flag          | No            |
| -s            | --stream_key  | Should you to stream a key. In case if you're using key that is larger than RAM.             | Flag          | No            |
| -i            | --input       | File to encrypt. If not specified, stdin used instead.                                       | String        | No            |
| -o            | --output      | Specify output file name. If not specified, stdout used instead.                             | String        | No            |

Example:  
```shell
python3 xorcipher.py --key=xorcipher.py --input=README.md --output=README-crypted.md
```  
```shell
cat README.md | python3 xorcipher.py --key=xorcipher.py > README-crypted.md
```  
