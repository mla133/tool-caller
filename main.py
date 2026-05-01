# main.py

import argparse

from agent.agent import Agent
from tools.registry import TOOL_SCHEMAS

from llm.ollama import OllamaAdapter
from llm.llamaserver import LlamaServerAdapter


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tool-calling agent (Ollama / llama-server)"
    )

    subparsers = parser.add_subparsers(
        dest="backend",
        required=True,
    )

    # ---------- Ollama ----------
    ollama = subparsers.add_parser("ollama", help="Use Ollama backend")
    ollama.add_argument(
        "--model",
        required=True,
        help="Ollama model name (e.g. qwen2.5:7b)",
    )

    # ---------- llama-server ----------
    llama_server = subparsers.add_parser("llama-server", help="Use llama-server HTTP")
    llama_server.add_argument(
        "--url",
        default="http://localhost:8123",
        help="Base URL of llama-server",
    )

    # ---------- Common ----------
    for p in (ollama, llama_cli, llama_server):
        p.add_argument(
            "--temperature",
            type=float,
            default=0.1,
        )
        p.add_argument(
            "--n-predict",
            type=int,
            default=512,
            dest="n_predict",
        )

    return parser.parse_args()


def create_llm(args):
    if args.backend == "ollama":
        return OllamaAdapter(model=args.model)

    if args.backend == "llama-server":
        return LlamaServerAdapter(
            base_url=args.url,
            temperature=args.temperature,
            n_predict=args.n_predict,
        )

    raise RuntimeError("Unreachable")


def main():
    args = parse_args()
    llm = create_llm(args)

    agent = Agent(
        llm=llm,
        tools=TOOL_SCHEMAS,
    )

    print(f"Agent ready (backend = {args.backend}). Type 'exit' to quit.")

    while True:
        user_input = input("> ").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            break

        agent.add_user_message(user_input)
        response = agent.step()
        print(response)


if __name__ == "__main__":
    main()
