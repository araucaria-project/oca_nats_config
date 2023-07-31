# oca_nats_config

## Description

The main task of the project is to maintain information about existing 
streams in the nats network, and to update them.

## Usage

Configuration of streams on the server is done by editing the `oca_nats_config/config.yaml` 
file in the main project directory. The oca nats server update should happen 
automatically after upload to git.


## Develop
It is possible to have your own local streams configuration and nats server 
password by creating a `config.yaml` file in the `oca_nats_config/configuration` 
directory.

To update the nats server with new streams, run the command:
```bash
  poetry run build
```

