<!--- Banner -->
<br />
<p align="center">
<a href="#"><img src="https://i.ibb.co/7pKLTjw/image.png"></a>
<h3 align="center">Web Voyager</h3>
<p align="center">A continuously learning web-browsing AI agent generalizing the Voyager architecture.</p>


<!--- About --><br />
## About

This project aims to extend the Voyager architecture described in [Wang et al. (2023)](https://arxiv.org/abs/2305.16291) to generic environments such as web browsing.
Similar to the original Minecraft implementation, the Voyager agent uses code as an action space and autonomously builds an ever-expanding library of skills while continuously exploring its environment. This is a **work in progress**.

<!--- The agents --><br />
## How it works
<a href="#"><img src="https://github.com/MineDojo/Voyager/blob/main/images/pull.png?raw=true"></a>

The architecture consists of four main agents:

- **CurriculumAgent**: Proposes what task the main Voyager agent should attempt next, drawing from a dynamic task pool.-
-  **ActionAgent**: Generates executable code as actions based on the given task and previous execution feedback. This is the agent that interacts with web elements like buttons, forms, and navigational elements.
- **CriticAgent**: Determines the success or failure of a performed task, offering critiques that inform future actions.
- **SkillManager**: Maintains a library of skills, or pieces of code, that have been proven effective in previous tasks. This becomes a valuable resource for ActionAgent in future tasks.

<!--- The process --><br />
## The process
Web Voyager initializes by loading an environment that mimics a web browser. From here, the CurriculumAgent proposes a task to the Voyager, based on the current state or the list of previously failed or completed tasks.

The ActionAgent then steps in, generating Python code to perform the task. It consults the SkillManager to reuse any existing code snippets that could be useful for the task at hand.
The code is executed in the browser environment, and the changes are monitored.

The CriticAgent evaluates the result of the task. If the task was successful, the new skill is added to the SkillManager, and the task is marked as complete in the CurriculumAgent.
If it fails, the task is sent back to the CurriculumAgent's pool for future attempts.
