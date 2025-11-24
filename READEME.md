# 一生 detector
A toy Discord bot that detects keywords like 一生（いっしょう） from messages,
do some useless reaction to them.

The keyword 一生（いっしょう） comes from the *Bang Dream! It's MyGO!!!!!*.

# System Requirement
- Python 3.12 is used on development.
  Later versions may or may not work.
- Discord bot permissions:
    - (None)
- Discord Guild (a.k.a. Server) permission:
    - View Channels (for detecting messages sent)
    - Send Messages (for forwarding messages detected)
    - Read Message History (for referencing the message detected)

# How to use
1. Prepare dotenv file from [.env.template](./.env.template).
    Most of configurations are provided from the dotenv file.
2. Prepare `logging.configure.yaml` from [logging-config.yaml](./logging-config.yaml.template).
3. Run the main script [issyou-detector.py](./issyou-detector.py) ...
    - run barely
    ```shell
    python issyou-detector.py
    ```
    - run with container
    ```shell
    docker compose up
    ```
