def load_prompt(prompt_path: str):
    """
    Load a prompt from a file.
    """
    with open(prompt_path, "r") as f:
        prompt = f.read()
    return prompt
