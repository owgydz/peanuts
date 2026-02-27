from .config import PackageConfig
from .installer import PackageInstaller
from .resolver import DependencyResolver

import os
import shutil
import json


class PackageManager:
    def __init__(self):
        self.config = PackageConfig()
        self.installer = PackageInstaller(self.config)
        self.resolver = DependencyResolver(self.config, self.installer)


    def install(self, owner_repo):
        self.installer.install_from_github(owner_repo)

        package_name = owner_repo.split("/")[-1]
        package_path = f"{self.config.packages_dir}/{package_name}"

        self.resolver.resolve_dependencies(package_path)

    def list_installed(self):
        if not os.path.exists(self.config.packages_dir):
            return []

        return os.listdir(self.config.packages_dir)

    def remove(self, package_name):
        package_path = os.path.join(
            self.config.packages_dir,
            package_name
        )

        if not os.path.exists(package_path):
            print(f"Package '{package_name}' is not installed.")
            return

        # Remove package directory
        shutil.rmtree(package_path)

        # Update installed.json if your config defines it
        installed_file = getattr(self.config, "installed_file", None)

        if installed_file and os.path.exists(installed_file):
            with open(installed_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if package_name in data:
                del data[package_name]

                with open(installed_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

        print(f"Removed package '{package_name}'. 🥜")