import os
import sys
import json
import subprocess
import requests

with open('.settings.json', 'r') as set:
    data = json.load(set)
SYSTEM_PROMPT = "\n".join(data.get('SYSTEM_PROMPT'))
MODEL = data.get('MODEL')
BASE_URL = data.get('BASE_URL')

def ask_ai(messages: list, api_key: str, tools: list = None) -> dict:
    """
    Send messages to OpenRouter and return the API response JSON.
    Raises requests.RequestException on network/API errors.
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    resp = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
