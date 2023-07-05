# ==========[ IMPORTS ]==========
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env", override=True)

# ==========[ CONFIG ]==========
# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Voyager
MAX_STEPS = 20
MAX_TASK_ATTEMPTS = 3
