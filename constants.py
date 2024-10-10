import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")
FORMAT_ASSISTANT_ID = os.getenv("FORMAT_ASSISTANT_ID")
INSTAGRAM_ASSISTANT_ID = os.getenv("INSTAGRAM_ASSISTANT_ID")
COMPANY_MISSION_ASSISTANT_ID = os.getenv("COMPANY_MISSION_ASSISTANT_ID")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

ASSISTANTS = [
    {"name": "Editor in Chief Advisor", "id": OPENAI_ASSISTANT_ID},
    {"name": "Text Formatter", "id": FORMAT_ASSISTANT_ID},
    {"name": "Build Instagram Content", "id": INSTAGRAM_ASSISTANT_ID},
    {"name": "Validate with UActuality Mission", "id": COMPANY_MISSION_ASSISTANT_ID},
]