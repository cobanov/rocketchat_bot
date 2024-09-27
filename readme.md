# Rocket App

This repository contains multiple bots designed to integrate with Rocket.Chat. Follow the instructions below to install dependencies and run the services.

## Installation

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Rename the `.env-sample` file to `.env`:

```bash
mv .env-sample .env
```

Open the `.env` file and modify the necessary variables (API keys, server URLs, etc.) according to your setup.

```bash
ROCKET_CHAT_USERNAME=<bot-username>
ROCKET_CHAT_PASSWORD=<bot-password>
ROCKET_CHAT_SERVER_URL=<https://server.url>
LLAMA_HOST=<http://llamahost.url>
LLAMA_MODEL=llama3.1
TAILSCALE_API_KEY=<tailscale-api-key>
TAILNET_NAME=<tailnet-name>
```

## Starting Rocket.Chat

To start the Rocket.Chat service using Docker Compose:

```bash
docker compose up -d
```

## Running Ollama Server

```bash
ollama run llama3.1
```

## Running Bots

To run the Llama bot:

```bash
cd rocketchat_bot
python -m llama_bot.bot
```

To run the Tailscale bot:

```bash
cd rocketchat_bot
python -m tailscale_bot.bot
```
