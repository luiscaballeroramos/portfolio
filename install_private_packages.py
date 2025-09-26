import os
import sys
import subprocess
from importlib.util import find_spec
from dotenv import load_dotenv
import logging

TOKENS = {"lcrcode": ("GITHUB_TOKEN", "GITHUB_USER")}
# load variables from .env file
load_dotenv()
# local installation directory
package_dir = os.path.join(os.path.dirname(__file__), "external_packages")
os.makedirs(package_dir, exist_ok=True)
# add the package directory to sys.path
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# Cache file to store installed packages info
CACHE_FILE = os.path.join(package_dir, ".package_cache.txt")


def is_package_installed_and_current(repo_name: str) -> bool:
    """Check if package is already installed and up to date."""
    try:
        # Check if package is importable
        if find_spec(repo_name) is None:
            return False

        # Check cache file for version info
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                cached_packages = f.read().splitlines()
                if repo_name in cached_packages:
                    logging.info(
                        f"Package {repo_name} found in cache, skipping installation"
                    )
                    return True

        return False
    except Exception:
        return False


def update_package_cache(repo_name: str):
    """Update the package cache file."""
    try:
        existing_packages = set()
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                existing_packages = set(f.read().splitlines())

        existing_packages.add(repo_name)

        with open(CACHE_FILE, "w") as f:
            f.write("\n".join(sorted(existing_packages)))
    except Exception as e:
        logging.warning(f"Could not update cache: {e}")


# function to install a package from GitHub
def install_package_from_github(repo_name: str):
    """Instala un paquete privado desde GitHub usando pip."""
    token = os.getenv(TOKENS[repo_name][0])
    user = os.getenv(TOKENS[repo_name][1])
    if not token or not user:
        raise EnvironmentError("Faltan GITHUB_TOKEN o GITHUB_USER en el archivo .env")

    repo_url = f"git+https://{token}@github.com/{user}/{repo_name}.git#egg={repo_name}"

    # Use --no-deps and --no-cache-dir for faster installation
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--target",
            package_dir,
            "--no-cache-dir",  # Skip pip cache
            "--quiet",  # Reduce output
            repo_url,
        ]
    )

    # Update cache
    update_package_cache(repo_name)

    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)


# loop through the repositories and install them
def install_all_packages(local: bool = False, force_reinstall: bool = False):
    if local:
        local_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../lcrcoding")
        )
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--force-reinstall",
                "-e",
                local_path,
            ]
        )
        if local_path not in sys.path:
            sys.path.insert(0, local_path)
    else:
        packages_to_install = []

        # First, check which packages actually need installation
        for repo in TOKENS.keys():
            if force_reinstall or not is_package_installed_and_current(repo):
                packages_to_install.append(repo)
            else:
                logging.info(f"Skipping {repo} - already installed")

        # Install only needed packages
        if packages_to_install:
            logging.info(f"Installing packages: {packages_to_install}")
            for repo in packages_to_install:
                install_package_from_github(repo)
        else:
            logging.info("All packages already installed, skipping installation")
