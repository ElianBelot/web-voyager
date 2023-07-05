# ==========[ IMPORTS ]==========
from voyager.agents.action import ActionAgent
from voyager.agents.critic import CriticAgent
from voyager.agents.curriculum import CurriculumAgent
from voyager.agents.skill import SkillManager
from voyager.environment.environment import Environment
from config import MAX_STEPS, MAX_TASK_ATTEMPTS


# ==========[ VOYAGER ]==========
class Voyager:
    # ==========[ INITIALIZATION ]==========
    def __init__(self, goal: str):
        self.goal = goal
        self.environment = Environment()
        self.curriculum_agent = CurriculumAgent()
        self.action_agent = ActionAgent()
        self.critic_agent = CriticAgent()
        self.skill_manager = SkillManager()

    # ==========[ RUN ]==========
    def run(self):
        # Set goal
        self.environment.reset()
        self.curriculum_agent.set_goal(self.goal)

        # TODO: Run until goal is achieved (all tasks completed OR goal-critic satisfied)
        for step in range(MAX_STEPS):
            # Get next task
            goal_progress = self.curriculum_agent.get_goal_progress(
                self.curriculum_agent.get_completed_tasks(), self.curriculum_agent.get_failed_tasks()
            )
            task = self.curriculum_agent.propose_next_task(goal_progress)

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
