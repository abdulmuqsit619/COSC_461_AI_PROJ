from tutor import ask_tutor

def main():
    print("COSC 461 AI Python Tutor (CLI)")
    print("Type 'quit' to exit.\n")

    history = None  # keeps conversation state

    while True:
        user = input("You: ")
        if user.strip().lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        # Get tutor response + metadata (tokens, cost, mode)
        reply, meta, history = ask_tutor(user, conversation_history=history)

        print("\nTutor:\n", reply)
        print("\n--- Meta Information ---")
        print(f"Mode: {meta['mode']}")
        print(f"Prompt Tokens: {meta['prompt_tokens']}")
        print(f"Completion Tokens: {meta['completion_tokens']}")
        print(f"Total Tokens: {meta['total_tokens']}")
        print(f"Estimated Cost: ${meta['estimated_cost']:.6f}")
        print("------------------------\n")

if __name__ == "__main__":
    main()
