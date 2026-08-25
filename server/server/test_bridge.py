from opencode_bridge import send_to_opencode


if __name__ == "__main__":
    print("Testing local OpenCode connection...")

    test_prompt = "Say hello from OpenCode!"

    print(f"Sending prompt: '{test_prompt}'")

    response = send_to_opencode(test_prompt)

    print("\nResult:")
    print(response)
