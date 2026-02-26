import os
import zipfile
import urllib.request
import shutil
from .registry import github_zip_url


class PackageInstaller:
    def __init__(self, config):
        self.config = config

    def install_from_github(self, owner_repo):
        url = github_zip_url(owner_repo)
        zip_path = os.path.join(self.config.cache_dir, f"{owner_repo.replace('/', '_')}.zip")

        print(f"Downloading {owner_repo}...")
        urllib.request.urlretrieve(url, zip_path)

        extract_dir = os.path.join(self.config.cache_dir, owner_repo.replace("/", "_"))
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        # GitHub adds -main suffix
        extracted_root = os.listdir(extract_dir)[0]
        full_path = os.path.join(extract_dir, extracted_root)

        package_name = owner_repo.split("/")[-1]
        target_dir = os.path.join(self.config.packages_dir, package_name)

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)

        shutil.move(full_path, target_dir)

        print(f"Installed {package_name} successfully.")