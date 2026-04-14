import sys

from agent.loop import run_agent
from schemas.tools import AVAILABLE_TOOLS

def main():
    if len(sys.argv) < 2:
        print("Please provide a prompt.")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])
    print("\n[Prompt]")
    print(prompt)

    run_agent(prompt, AVAILABLE_TOOLS)

if __name__ == "__main__":
    main()
