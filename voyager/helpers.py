# ==========[ IMPORTS ]==========
from voyager.config import PROMPTS_PATH
from langchain import PromptTemplate
import os


# ==========[ HELPERS ]==========
def load_prompt(prompt_name: str) -> PromptTemplate:
    with open(os.path.join(PROMPTS_PATH, f"{prompt_name}.txt"), "r") as f:
        template = f.read()

    return PromptTemplate.from_template(template)


def title(text: str) -> str:
    print(f"====================[ {text.upper()} ]====================")
