# Installation of the OCA compatible NATS server on Docker

This instruction is suitable for both server and developer machine.

## Clone the repository

```bash
    git clone  https://github.com/araucaria-project/oca_nats_config.git
    cd oca_nats_config
```

## Run the server manually (e.g. local, developer machine)
Suppose you are in the `oca_nats_config` - the project root directory.

```bash
    cd docker/nats
    docker-compose up -d
    cd ../..
```

## Run the server as a service (e.g. server machine)
Suppose you are in the `oca_nats_config` - the project root directory.

```bash
    sudo ln -s $PWD/docker/nats/nats.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable nats.service
    sudo systemctl start nats.service
```


## Update NATS streams
Suppose you are in the `oca_nats_config` - the project root directory.

You should have `poetry` installed. (Recommended way is to install `pipx` nad then poetry with `pipx`)

```bash
    poetry install
    poetry run build
```

