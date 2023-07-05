# ==========[ IMPORTS ]==========
from voyager.agents.action import ActionAgent
from voyager.agents.critic import CriticAgent
from voyager.agents.curriculum import CurriculumAgent
from voyager.agents.skill import SkillManager


# ==========[ VOYAGER ]==========
class Voyager:
    # ==========[ INITIALIZATION ]==========
    def __init__(self, environment):
        self.environment = environment
        self.curriculum_agent = CurriculumAgent()
        self.action_agent = ActionAgent()
        self.critic_agent = CriticAgent()
        self.skill_manager = SkillManager()

    # ==========[ RUN ]==========
    def run(self):
        agent_state = self.environment.reset()

        # Main loop
        while True:
            # Get next task
            exploration_progress = self.curriculum_agent.get_exploration_progress(
                self.curriculum_agent.get_completed_tasks(), self.curriculum_agent.get_failed_tasks()
            )
            task = self.curriculum_agent.propose_next_task(agent_state, exploration_progress)

            # Attempt task
            code = None
            environment_feedback = None
            execution_errors = None
            critique = None
            success = False
            for _ in range(4):
                # Choose action
                skills = self.skill_manager.retrieve_skills(task, environment_feedback)
                code = self.action_agent.generate_code(
                    task, code, environment_feedback, execution_errors, critique, skills
                )

                # Play action and get feedback
                agent_state, environment_feedback, execution_errors = self.environment.step(code)
                success, critique = self.critic_agent.check_task_success(task, agent_state)

                if success:
                    break

            # Update skill library
            if success:
                self.skill_manager.add_skill(code)
                self.curriculum_agent.add_completed_task(task)
            else:
                self.curriculum_agent.add_failed_task(task)
