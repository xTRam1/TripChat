import argparse
import os

from agent_container import AgentContainer


def validate_api_keys() -> None:
    import os

    if (
        not os.environ["GPLACES_API_KEY"]
        or not os.environ["OPENAI_API_KEY"]
        or not os.environ["GOOGLE_CSE_ID"]
        or not os.environ["GOOGLE_API_KEY"]
        or not os.environ["OPENWEATHERMAP_API_KEY"]
    ):
        raise Exception("One or more API keys are not set. Please set them.")


if __name__ == "__main__":
    validate_api_keys()

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
