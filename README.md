# oca_nats_config

## Description

The main task of the project is to maintain information about existing 
streams in the OCA observatory NATS network, and to update them on either
OCA server `nats.oca.lan` or developer machine.

The stream configuration for developers is stored in the `oca_nats_config/configuration`

## Usage

Configuration of streams on the server is done by editing the `oca_nats_config/config.yaml` 
file in the main project directory. The oca nats server update should happen 
automatically after upload to git.

## NATS servers
Starting from version 1.1.0, the project supports multiple nats servers (as serverish started to support).
Default, in the `oca_nats_config/config.yaml` are two servers:
* `nts.oca.lan` - the main server for the OCA observatory
* `localhost` - the developer server
This means, that in observatory, the `nts.oca.lan` server will be updated, 
and on the developer machine, the `localhost` server will be updated.


### Develop usage
It is possible to have your own local streams configuration and nats server 
password by creating a `config.yaml` file in the `oca_nats_config/configuration` 
directory.

To update the nats server with new streams, run the command:
```bash
  poetry run build
```

## Installation

### Docker
For the installation on Docker (OCA server or local developer machine)
follow the instructions in [Docker](docker/nats/NOTES.md) section.

### Manual installation
First you need to clone the repository from git.
```bash
git clone https://github.com/araucaria-project/oca_nats_config.git
```
Then go to the project folder and install it.
WARNING the `poetry` package is required for installation.

```bash
cd oca_nats_config
poetry install
```
For a single update, follow the instructions in [Develop usage](#develop-usage) section. 

### Automatic update

Attention. The service is configured to run as a `poweruser`. This means that a user with this name must exist in 
the environment and must be the owner of the project. Therefore, the installation process should be done as `poweruser`.

To run the auto-update service on linux you need to first complete installation 
(see [installation](#installation) section).

Go to the `/etc/systemd/system/` directory in the project and make symlinks to service scripts.
WARNING `[path-to-project]` is the project path
```bash
cd /etc/systemd/system/
sudo ln -s [path-to-project]/oca_nats_config/scripts/oca_nats_config_update.service oca_nats_config_update.service
sudo ln -s [path-to-project]/oca_nats_config/scripts/oca_nats_config_update.timer oca_nats_config_update.timer
```
Next go to and make symlink to auto update script:
```bash
cd /usr/bin/
sudo ln -s [path-to-project]/oca_nats_config/scripts/auto_update.sh auto_update.sh
```

Now start the services.

```bash
sudo systemctl daemon-reload
sudo systemctl enable oca_nats_config_update.timer
sudo systemctl start oca_nats_config_update.timer
```

At the end, you can check status nev service by:

```bash
sudo systemctl status oca_nats_config_update.timer
```
