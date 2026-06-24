import sys
from agent import ask

def main():
    if len(sys.argv) < 2:
        print("Usage: python miniagent.py \"<question>\"")
        return
    question = " ".join(sys.argv[1:])
    print(f'\n🤔 thinking… "{question}"')
    result = ask(question)
    
    if result.confident:

        print(f"\n✅ Answer: {result.answer}")

        if result.tool_used == "calculator" and result.expression:
            print(f"   How I got it: calculator(\"{result.expression}\") = {result.answer}")

        elif result.tool_used == "notes_lookup" and result.source:
            print(f"   Source: {result.source}")

    else:
        print(f"\n🛑 {result.answer}")
        if result.tool_used != "none":
            print(f"   (tool attempted: {result.tool_used})")

if __name__ == "__main__":
    main()