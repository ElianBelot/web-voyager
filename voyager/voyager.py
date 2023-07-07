# ==========[ IMPORTS ]==========
from voyager.agents.action import ActionAgent
from voyager.agents.critic import CriticAgent
from voyager.agents.curriculum import CurriculumAgent
from voyager.agents.skill import SkillManager
from voyager.config import MAX_STEPS, MAX_TASK_ATTEMPTS
from voyager.environment.environment import Environment
from voyager.helpers import title


# ==========[ VOYAGER ]==========
class Voyager:
    def __init__(self):
        self.environment = Environment()
        self.curriculum_agent = CurriculumAgent()
        self.action_agent = ActionAgent()
        self.critic_agent = CriticAgent()
        self.skill_manager = SkillManager()

    # ==========[ RUN ]==========
    def run(self, goal: str):
        # TODO: Initialize environment when running, not at initialization
        # TODO: Get rid of goal, adapt curriculum for internet browsing
        # TODO: Bring back "agent_state", which env.step() writes to and is used for the critique
        self.curriculum_agent.goal = goal
        for step in range(MAX_STEPS):
            title(f"STEP {step + 1}/{MAX_STEPS}")

            # TODO: We'll manually set tasks for now, before having the AI do it
            task = self.curriculum_agent.propose_next_task()
            print(f"[TASK] {task}")

            # Attempt task
            code = None
            code_output = None
            execution_errors = None
            critique = None
            success = False
            for _ in range(MAX_TASK_ATTEMPTS):
                # Generate code
                skills = self.skill_manager.retrieve_skills(task, code_output)
                code = self.action_agent.generate_code(task, code, code_output, execution_errors, critique, skills)

                # Run code
                code_output, execution_errors = self.environment.step(code)

                # Get feedback
                success, critique = self.critic_agent.check_task_success(task)
                if success:
                    break

            # Update skill library
            if success:
                self.skill_manager.add_skill(code)
                self.curriculum_agent.add_completed_task(task)
            else:
                self.curriculum_agent.add_failed_task(task)
