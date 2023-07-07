import contextlib
import io
import traceback
import types
from typing import Any, Dict

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ==========[ ENVIRONMENT ]==========
class Environment:
    def __init__(self, headless: bool = False):
        # Set Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        if headless:
            self.chrome_options.add_argument("--headless")

        # Set driver
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def reset(self):
        # Closes the driver and start a new one
        self.driver.quit()
        self.driver = webdriver.Chrome(options=self.chrome_options)

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
                if isinstance(value, types.FunctionType):
                    # Invoke the function, passing the driver as the first argument.
                    try:
                        code_output = value(self.driver, **arguments)
                    except Exception as e:
                        execution_errors = traceback.format_exc()

        # Add the printed text to the log
        log.extend(string_io.getvalue().splitlines())

        return {"output": code_output, "errors": execution_errors, "log": log}
