import argparse
import os

from agent_container import AgentContainer

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise Exception(
            "OPENAI_API_KEY environment variable not set. Please set it to your OpenAI API key."
        )

    # TODO: Implement this parallel argument so that an agent with access to multiple
    # agents can run them in parallel. Or build some dependency graph and run them in
    # parallel if they don't depend on each other.
    parser = argparse.ArgumentParser(
        description="Parallelizes the agent conversations."
    )
    parser.add_argument(
        "--parallel", action="store_true", help="Parallelizes the agent conversations."
    )
    args = parser.parse_args()

    agent_container = AgentContainer()
    brain_agent = agent_container.brain_agent

    user_input = input("Enter your message: ")
    brain_agent.run(user_input, parallel=args.parallel)
