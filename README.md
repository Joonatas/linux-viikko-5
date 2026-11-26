# Viikko 5 LLM Chat

Flask + Ollama + MariaDB chat application.

## Features

- Local TinyLlama model
- MariaDB conversation storage
- Nginx reverse proxy
- Gunicorn
- Systemd service
- GitHub Actions CI

## URLs

- /viikko5/
- /viikko5/health

## Technologies

- Python
- Flask
- Ollama
- TinyLlama
- MariaDB
- Nginx
- Gunicorn
- GitHub Actions
- Deployment test

---

## Application Overview

The application allows users to chat with a local TinyLlama language model running through Ollama.

Messages are stored in MariaDB so that chat history is preserved.

---

## Architecture

Browser
↓
Nginx
↓
Gunicorn
↓
Flask
↓
Ollama (TinyLlama)

Flask
↓
MariaDB

---

## CI/CD

GitHub Actions automatically:

- Runs pytest tests
- Deploys changes to the server
- Restarts viikko5.service
- Verifies the health endpoint

---

## Linux User

Service user:

viikko5

## Database User

Database user:

viikko5user

The database user only has access to viikko5db.

---

## Model Selection

Model used:

TinyLlama 1B

Reason:

- Lightweight
- Suitable for limited server resources
- Runs locally without external APIs

---

## What I Learned

During this assignment I learned:

- Running local LLMs with Ollama
- Managing services with systemd
- Using Gunicorn and Nginx together
- Creating CI/CD pipelines with GitHub Actions
- Deploying applications automatically with SSH
- Storing chat history in MariaDB
