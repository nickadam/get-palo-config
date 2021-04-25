# get-palo-config
Get config of Palo Alto device using ssh and config-output-format=set

## Requirements
- python 3.9

## Getting started

These instructions were written for bash. You may have to adapt for windows, or use WSL.

Clone this repo

```
git clone https://github.com/nickadam/get-palo-config.git
cd get-palo-config
```

Start a python virtual environment (optional)

```
python -m venv env
source env/bin/activate
```

Install python requirements

```
pip install -r requirements.txt
```

Run `get_config.sh` with your username and hostname or IP. You will be prompted for your password

```
./get_config.sh admin 10.0.0.1 > config.txt
```
