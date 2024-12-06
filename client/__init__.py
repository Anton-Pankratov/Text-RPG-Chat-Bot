from pyrogram import Client
from telethon import TelegramClient

from utils.parser_env_properties import get_client_api_credentials

api_credentials = get_client_api_credentials()

client_pyrogram = Client(name=api_credentials[0], api_id=api_credentials[1], api_hash=api_credentials[2])
client_telethon = TelegramClient(session=api_credentials[0], api_id=api_credentials[1], api_hash=api_credentials[2])