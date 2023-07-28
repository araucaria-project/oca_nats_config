# oca_nats_config

## Description

The main task of the project is to maintain information about existing 
streams in the nats network, and to update them.

## Usage

To update the nats server with new streams, run the command:
```bash
  poetry run build
```

The list of existing streams is in the `DefinedStreams` class which
also serves as an enum class for other projects.