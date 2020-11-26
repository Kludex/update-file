import logging
import subprocess
import sys
from pathlib import Path
from subprocess import CalledProcessError

from pydantic import BaseSettings


class Settings(BaseSettings):
    github_ref: str
    input_script_file: Path = Path("update.py")
    input_update_file: Path = Path("README.md")
    input_requirements: Path = Path("requirements.txt")


logging.basicConfig(level=logging.INFO)
settings = Settings()
if not settings.input_script_file.is_file():
    logging.error(f"Script file doesn't exist: {settings.input_script_file}")
    sys.exit(1)
if not settings.input_update_file.is_file():
    logging.error(f"Update file doesn't exist: {settings.input_update_file}")
    sys.exit(1)

logging.info("Running script")
logging.info(subprocess.run(["ls"], capture_output=True))
subprocess.run(["pip", "install", "-r", settings.input_requirements])
content = subprocess.run(
    ["python", str(settings.input_script_file)], capture_output=True, check=True,
).stdout.decode("utf-8")
logging.info("Writting content")
with open(settings.input_update_file, "w") as f:
    f.write(content)

logging.info("Setting up GitHub Actions git user")
subprocess.run(["git", "config", "user.name", "github-actions"], check=True)
subprocess.run(["git", "config", "user.email", "github-actions@github.com"], check=True)
subprocess.run(["git", "add", str(settings.input_update_file)], check=True)
try:
    subprocess.run(
        ["git", "commit", "-m", f"📝 Update {settings.input_update_file}"], check=True
    )
except CalledProcessError:
    logging.info("File already up-to-date")
logging.info(f"Pushing changes: {settings.input_update_file}")
logging.info(f"Current branch: {settings.github_ref}")
subprocess.run(["git", "push", "origin", settings.github_ref], check=True)
logging.info("Finished")
