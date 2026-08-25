import subprocess

def send_to_opencode(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["opencode", "run", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return result.stdout.strip() or "OpenCode returned no text."

        return f"[OpenCode Error]: {result.stderr.strip()}"

    except FileNotFoundError:
        return "[Bridge Error]: OpenCode command not found."

    except subprocess.TimeoutExpired:
        return "[Bridge Error]: OpenCode request timed out."

    except Exception as e:
        return f"[Bridge Error]: {e}"
