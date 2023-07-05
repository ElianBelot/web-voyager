# ==========[ IMPORTS ]==========
...


# ==========[ ENVIRONMENT ]==========
class Environment:
    def __init__(self):
        pass

    def reset(self):
        # Resets the environment to its initial state.
        pass

    def step(self, code):
        # 1. Execute the provided code as action, optionally with a semantic layer.
        # 2. Capture any execution errors.
        # 3. Capture code output.
        # 4. Generate feedback based on the execution.

        code_output = None
        execution_errors = None

        return code_output, execution_errors
