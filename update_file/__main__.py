import logging
import subprocess
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    github_repository: str
    github_event_path: Path
    github_event_name: Optional[str] = None
    input_script_file: Path = Path("update.py")
    input_update_file: Path = Path("README.md")


logging.basicConfig(level=logging.INFO)
settings = Settings()

logging.info("Running script")
logging.info(subprocess.run(["ls"], capture_output=True))
content = subprocess.run(
    ["python", "-m", settings.input_script_file.resolve()],
    capture_output=True,
    check=True,
)
logging.info("Writting content")
with open(settings.input_update_file, "w") as f:
    f.write(content)

logging.info("Setting up GitHub Actions git user")
subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
subprocess.run(["git", "add", str(settings.input_update_file)], check=True)
subprocess.run(
    ["git", "commit", "-m", f"📝 Update {settings.input_update_file}"], check=True
)
logging.info(f"Pushing changes: {settings.input_update_file}")
subprocess.run(["git", "push"], check=True)
logging.info("Finished")
