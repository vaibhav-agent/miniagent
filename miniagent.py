import sys
from agent import ask


def main():
    if len(sys.argv) < 2:
        print("Usage: python miniagent.py <question>")
        return

    question = sys.argv[1]

    result = ask(question)

    print("\nQuestion:", question)
    print("Tool Used:", result.tool_used)
    print("Answer:", result.answer)
    print("Confident:", result.confident)


if __name__ == "__main__":
    main()