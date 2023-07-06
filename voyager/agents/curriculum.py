# ==========[ IMPORTS ]==========
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


# ==========[ CURRICULUM AGENT ]==========
class CurriculumAgent:
    def __init__(self):
        # Hyperparameters
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.mode = "auto"
        self.goal = ""

        # Track tasks
        self.completed_tasks = []
        self.failed_tasks = []

    # ==========[ PROPOSE NEXT TASK ]==========
    def propose_next_task(self, goal_progress):
        # This either generates a new task or selects an existing one
        return self.propose_next_manual_task(goal_progress)

    def propose_next_manual_task(self, goal_progress):
        # TODO: This will ask the user for input
        pass

    def propose_next_ai_task(self, goal_progress):
        # TODO: This will run the AI
        pass

    # ==========[ TASK TRACKING ]==========
    # TODO: Simplify
    def get_completed_tasks(self):
        return self.completed_tasks

    def get_failed_tasks(self):
        return self.failed_tasks

    def add_completed_task(self, task):
        self.completed_tasks.append(task)

    def add_failed_task(self, task):
        self.failed_tasks.append(task)
