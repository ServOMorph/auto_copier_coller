import json
import sys
import subprocess

def main():
    try:
        data = json.load(sys.stdin)
        transcript_path = data.get("transcript_path")

        if not transcript_path:
            return

        last_assistant_content = None

        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("type") == "assistant":
                        message = entry.get("message", {})
                        content_parts = message.get("content", [])
                        text_parts = []
                        for part in content_parts:
                            if isinstance(part, dict) and part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                            elif isinstance(part, str):
                                text_parts.append(part)
                        if text_parts:
                            last_assistant_content = "\n".join(text_parts)
                except json.JSONDecodeError:
                    continue

        if last_assistant_content:
            process = subprocess.Popen(
                ["clip"],
                stdin=subprocess.PIPE,
                shell=True
            )
            process.communicate(input=last_assistant_content.encode("utf-8"))

    except Exception:
        pass

if __name__ == "__main__":
    main()
