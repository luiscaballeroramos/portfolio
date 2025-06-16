import os
import sys
import subprocess
from dotenv import load_dotenv

TOKENS = {"lcr_code": ("GITHUB_TOKEN", "GITHUB_USER")}
PACKAGES_MODULES = {"lcr_code": ["lcr-code"]}
# Load environment variables
load_dotenv()
# local installation directory
package_dir = os.path.join(os.path.dirname(__file__), "external_packages")
os.makedirs(package_dir, exist_ok=True)
sys.path.append(package_dir)


# reusable function to ensure private package is installed
def ensure_private_package(module_name: str, repo_name: str):
    token = os.getenv(TOKENS[repo_name][0])
    user = os.getenv(TOKENS[repo_name][1])
    if not token or not user:
        raise EnvironmentError("Missing GITHUB_TOKEN or GITHUB_USER in .env file")
    try:
        __import__(module_name)
    except ImportError:
        repo_url = (
            f"git+https://{token}@github.com/{user}/{repo_name}.git#egg={module_name}"
        )
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--target", package_dir, repo_url]
        )
        __import__(module_name)


# ensure private packages are installed
for repo, modules in PACKAGES_MODULES.items():
    for module in modules:
        ensure_private_package(module, repo)
