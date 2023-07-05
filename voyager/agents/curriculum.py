# ==========[ IMPORTS ]==========
...


# ==========[ CURRICULUM AGENT ]==========
class CurriculumAgent:
    """
    This is about creating system and user messages that will be run to propose the next task.
    This also keeps track of progress and tasks.

    [POC] Run "propose_next_task" successfully (executer in a notebook, we just care about messages).
    [TASKS]
    - Create system to keep track of messages (output of propose_next_task is a list of messages?)
    - Keep track of progress
    """

    # ==========[ GOAL ]==========
    def set_goal(self, goal):
        # This sets the goal in the system prompt
        pass

    def get_goal_progress(self, completed_tasks, failed_tasks):
        #
        pass

    # ==========[ PROPOSE NEXT TASK ]==========
    def propose_next_task(self, goal_progress):
        # This either generates a new task or selects an existing one
        pass

    # ==========[ TASK TRACKING ]==========
    def get_completed_tasks(self):
        # Implement this method.
        pass

    def get_failed_tasks(self):
        # Implement this method.
        pass

    def add_completed_task(self, task):
        # Implement this method.
        pass

    def add_failed_task(self, task):
        # Implement this method.
        pass
