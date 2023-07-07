# ==========[ IMPORTS ]==========
import concurrent.futures
import contextlib
import io
import re
import time
import traceback
import types
from typing import Any, Dict, List, Optional

import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from unidecode import unidecode


# ==========[ ENVIRONMENT ]==========
class Environment:
    def __init__(self, headless: bool = False):
        # Set Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        if headless:
            self.chrome_options.add_argument("--headless")

    def start(self):
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.state = {}

    def reset(self):
        # Closes the driver and start a new one
        self.driver.quit()
        self.start()

    # TODO: Add all functions in skill library AND control primitives to be ran in the environment
    def step(self, code, arguments: Dict[str, Any] = {}):
        # Generate a namespace for the code to be executed in
        code_output = None
        execution_errors = None
        log = []
        namespace = {"selenium": selenium}

        # Redirect standard output to a string stream
        string_io = io.StringIO()
        with contextlib.redirect_stdout(string_io):
            # Execute the code
            try:
                exec(code, namespace)
            except Exception as e:
                execution_errors = traceback.format_exc()

            # Extract the function defined in the code, which should be the only top-level item.
            for value in namespace.values():
                # Invoke the function, passing the driver as the first argument.
                if isinstance(value, types.FunctionType):
                    try:
                        code_output = value(self.driver, **arguments)
                    except Exception as e:
                        execution_errors = traceback.format_exc()

        # Add the printed text to the log
        log.extend(string_io.getvalue().splitlines())

        # Get the current state
        self.state = self.current_state()

        return {"output": code_output, "errors": execution_errors, "log": log, "observation": self.state}

    # ==========[ STATE ]==========
    def prettify_text(self, text: str, limit: Optional[int] = None) -> str:
        """Prettify text by removing extra whitespace and converting to lowercase."""
        text = re.sub(r"\s+", " ", text)
        text = text.strip().lower()
        text = unidecode(text)
        if limit:
            text = text[:limit]
        return text

    def get_all_text_elements(self):
        # get all text from body excluding script and style tags
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = [t.strip() for t in text.splitlines() if t.strip()]
        return lines[:100]  # Limit to maximum 100 elements

    def get_interactable_elements(self):
        # get only interactable elements text and id
        interactable_elements = self.driver.find_elements(
            By.XPATH,
            "//button | //div[@role='button'] | //a | //input[@type='submit'] | //input[@type='button']",
        )
        interactables = []
        for element in interactable_elements:
            if element.text.strip() or element.get_attribute("id"):
                interactables.append({"id": element.get_attribute("id"), "text": element.text.strip()})
        return interactables

    def find_form_fields(self):
        """Find form fields on the website."""
        fields = []
        for element in self.driver.find_elements(By.XPATH, "//textarea | //input"):
            if element.get_attribute("type") not in ["hidden", "submit", "button", "image"]:
                label_txt = (
                    element.get_attribute("id") or element.get_attribute("name") or element.get_attribute("aria-label")
                )
                if label_txt:
                    fields.append(self.prettify_text(label_txt))
        return fields

    # HACK: This is a primitive solution, look into better ways to do fast scraping.
    # NOTE: Eventually, the agent can figure out how to best describe the website as a first task, and iterate on this as it needs more information.
    def current_state(self, time_limit=10):
        # Let driver wait for the website to load
        time.sleep(1)
        state = {}

        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit tasks to the executor
            future_to_task = {
                executor.submit(task): task_name
                for task_name, task in {
                    "main_content": self.get_all_text_elements,
                    "interactable_elements": self.get_interactable_elements,
                    "form_fields": self.find_form_fields,
                }.items()
            }

            # Get results as they become available
            completed_futures = []
            for future in concurrent.futures.as_completed(future_to_task, timeout=time_limit):
                task_name = future_to_task[future]
                try:
                    result = future.result()
                    state[task_name] = result
                    completed_futures.append(future)
                except Exception as e:
                    state[task_name] = str(e)
                    print(f"Task {task_name} did not complete successfully: {str(e)}")

                # Check time limit
                if time.time() - start_time > time_limit:
                    print("Time limit exceeded. Returning partial state description.")
                    break

            # Cancel unfinished futures
            for future in future_to_task:
                if future not in completed_futures:
                    future.cancel()

        return state
