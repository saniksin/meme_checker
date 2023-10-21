#### Install required packages
```bash
sudo apt update && \
sudo apt install python3 wget git -y
```
#### Clone the repo
```
git clone https://github.com/saniksin/meme_checker
```
#### Install python packages with pip
```bash
cd $HOME/meme_checker && \
pip3 install -r requirements.txt
```
### Edit tokens.txt which is located in $HOME/meme_checker/tokens.txt 
#### Make it look like this (one Bearer token = one line):
```
Bearer eyJ10eXAiOiJKV1QiLCbGciOiJIUzI21NiJ9.....
Bearer eyJ10eXAiOiJKV1QiLCbGciOiJIUzI21NiJ9.....
Bearer eyJ10eXAiOiJKV1QiLCbGciOiJIUzI21NiJ9.....
Bearer eyJ10eXAiOiJKV1QiLCbGciOiJIUzI21NiJ9.....
```
### Edit proxys.txt which is located in $HOME/meme_checker/proxys.txt 
#### Make it look like this (one proxy = one line):
```
http://user:login@ip:port
http://user:login@ip:port
http://user:login@ip:port
http://user:login@ip:port
```

> Note: if you don't specify a proxy, the requests will be sent from a single IP, which is not highly recommended.
 
### Run the script
```python
python3 $HOME/meme_checker/main.py
```
### Output will look like::
```bash
+----------------------+----------------+
| InviteCode           |   Count Result |
+======================+================+
| captainz#xxxx        |             21 |
+----------------------+----------------+
| captainz#xxxx        |             31 |
+----------------------+----------------+
| Tokens in tokens.txt |             52 |
+----------------------+----------------+
| Unique tokens        |             52 |
+----------------------+----------------+
```
### Failed tokens
#### All tokens that resulted in an error will be written to failed_tokens.txt.

```
Number token of tokens.txt, Token
3, Bearer eyJ10eXAiOiJKV1QiLCbGciOiJIUzI21NiJ9....
```