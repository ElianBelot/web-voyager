# ==========[ IMPORTS ]==========
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

from voyager.helpers import load_prompt


# ==========[ CURRICULUM AGENT ]==========
class CurriculumAgent:
    def __init__(self):
        # Hyperparameters
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.mode = "auto"

        # Track tasks
        self.completed_tasks = []
        self.failed_tasks = []

    # ==========[ PROPOSE NEXT TASK ]==========
    def propose_next_task(self):
        if self.mode == "auto":
            return self.propose_next_ai_task()
        else:
            return self.propose_next_manual_task()

    def propose_next_manual_task(self):
        return input("[TASK] ")

    def propose_next_ai_task(self):
        # Load prompt
        template = load_prompt("curriculum")
        prompt = template.format(
            completed_tasks="- \n".join(self.completed_tasks),
            failed_tasks="- \n".join(self.failed_tasks),
        )

        # Generate task
        messages = [HumanMessage(content=prompt)]
        task = self.llm(messages).content.split("[TASK]")[1].strip()

        return task

    # ==========[ TASK TRACKING ]==========
    def add_completed_task(self, task):
        self.completed_tasks.append(task)

    def add_failed_task(self, task):
        self.failed_tasks.append(task)
