import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROFILE = os.getenv("PROFILE")
    ACCOUNT = os.getenv("ACCOUNT")
    PASSWORD = os.getenv("PASSWORD")
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")