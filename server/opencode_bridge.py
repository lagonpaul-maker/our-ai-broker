import subprocess


def send_to_opencode(prompt: str) -> str:
    """
    Sends the user message to the local OpenCode CLI.
    """
    try:
        result = subprocess.run(
            ["opencode", "run", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()

        error_msg = result.stderr.strip() or "OpenCode returned no output."
        return f"[OpenCode Error]: {error_msg}"

    except FileNotFoundError:
        return "[Bridge Error]: 'opencode' command not found in PATH."

    except subprocess.TimeoutExpired:
        return "[Bridge Error]: OpenCode request timed out."

    except Exception as e:
        return f"[Bridge Error]: {str(e)}"
