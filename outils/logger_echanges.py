import os
import json
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).parent.parent / "logs" / "sessions"


class LoggerEchanges:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.session_id = None
        self.session_file = None
        self.messages = []
        LOGS_DIR.mkdir(exist_ok=True)

    def start_session(self):
        now = datetime.now()
        self.session_id = now.strftime("%Y%m%d_%H%M%S")
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H-%M-%S")
        filename = f"{date_str}_{time_str}_session.md"
        self.session_file = LOGS_DIR / filename
        self.messages = []

        header = f"""# Session d'echange IA
**Date**: {now.strftime("%Y-%m-%d %H:%M:%S")}
**Session ID**: {self.session_id}

---

"""
        self.session_file.write_text(header, encoding="utf-8")
        return self.session_id

    def log_message(self, source: str, destination: str, content: str, msg_type: str = "MESSAGE"):
        if not self.session_file:
            self.start_session()

        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")

        entry = {
            "timestamp": timestamp,
            "source": source,
            "destination": destination,
            "type": msg_type,
            "content": content
        }
        self.messages.append(entry)

        source_icon = self._get_icon(source)
        dest_icon = self._get_icon(destination)

        md_entry = f"""
## [{timestamp}] {source_icon} {source} -> {dest_icon} {destination}

**Type**: `{msg_type}`

```
{content[:2000]}{"..." if len(content) > 2000 else ""}
```

---
"""
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(md_entry)

    def _get_icon(self, agent: str) -> str:
        icons = {
            "COMET": "[O1]",
            "CLAUDE": "[W1]",
            "CHATGPT": "[W2]",
            "USER": "[U]",
            "SYSTEM": "[SYS]"
        }
        return icons.get(agent.upper(), "[?]")

    def _count_messages_by_agent(self) -> dict:
        stats = {}
        for msg in self.messages:
            dest = msg.get("destination", "").upper()
            if dest:
                stats[dest] = stats.get(dest, 0) + 1
        return stats

    def end_session(self):
        if not self.session_file:
            return

        now = datetime.now()
        agent_stats = self._count_messages_by_agent()

        stats_lines = "\n".join(
            f"- **{agent}**: {count} message(s)"
            for agent, count in sorted(agent_stats.items())
        )

        footer = f"""
---

## Fin de session

**Heure de fin**: {now.strftime("%H:%M:%S")}
**Nombre total de messages**: {len(self.messages)}

### Prompts par agent

{stats_lines if stats_lines else "Aucun message enregistré"}
"""
        with open(self.session_file, "a", encoding="utf-8") as f:
            f.write(footer)

        self.session_file = None
        self.session_id = None
        self.messages = []

    @staticmethod
    def get_all_sessions():
        if not LOGS_DIR.exists():
            return []

        sessions = []
        for f in sorted(LOGS_DIR.glob("*.md"), reverse=True):
            stat = f.stat()
            sessions.append({
                "filename": f.name,
                "path": str(f),
                "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                "size": stat.st_size
            })
        return sessions

    @staticmethod
    def read_session(filepath: str) -> str:
        return Path(filepath).read_text(encoding="utf-8")


logger = LoggerEchanges()
