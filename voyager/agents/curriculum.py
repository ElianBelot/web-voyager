# ==========[ IMPORTS ]==========
...


# ==========[ CURRICULUM AGENT ]==========
class CurriculumAgent:
    # ==========[ GOAL ]==========
    def set_goal(self, goal):
        # Implement this method.
        pass

    def get_goal_progress(self, completed_tasks, failed_tasks):
        # Implement this method.
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
