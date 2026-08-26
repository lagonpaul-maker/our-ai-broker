


import subprocess


def send_to_opencode(prompt: str) -> str:
    try:
        result = subprocess.run(
            [
                "proot-distro",
                "login",
                "debian",
                "--",
                "/usr/local/bin/opencode",
                "run",
                prompt
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            error = result.stderr.strip()
            return f"[OpenCode Error]: {error}"

        return result.stdout.strip()

    except FileNotFoundError:
        return "[Bridge Error]: proot-distro not found."

    except subprocess.TimeoutExpired:
        return "[Bridge Error]: OpenCode request timed out."

    except Exception as e:
        return f"[Bridge Error]: {e}"
