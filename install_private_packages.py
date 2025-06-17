import os
import sys
import subprocess
from importlib.util import find_spec
from dotenv import load_dotenv

TOKENS = {"lcrcode": ("GITHUB_TOKEN", "GITHUB_USER")}
# load variables from .env file
load_dotenv()
# local installation directory
package_dir = os.path.join(os.path.dirname(__file__), "external_packages")
os.makedirs(package_dir, exist_ok=True)
# add the package directory to sys.path
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)


# function to install a package from GitHub
def install_package_from_github(repo_name: str):
    """Instala un paquete privado desde GitHub usando pip."""
    token = os.getenv(TOKENS[repo_name][0])
    user = os.getenv(TOKENS[repo_name][1])
    if not token or not user:
        raise EnvironmentError("Faltan GITHUB_TOKEN o GITHUB_USER en el archivo .env")
    repo_url = f"git+https://{token}@github.com/{user}/{repo_name}.git#egg={repo_name}"
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--target", package_dir, repo_url]
    )
    sys.path.insert(0, package_dir)


# loop through the repositories and install them
for repo in TOKENS.keys():
    install_package_from_github(repo)
