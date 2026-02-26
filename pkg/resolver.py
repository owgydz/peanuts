import os
import tomllib
from .versioning import Version


class DependencyResolver:
    def __init__(self, config, installer):
        self.config = config
        self.installer = installer
        self.installed = set()

    def resolve_dependencies(self, package_path):
        config_path = os.path.join(package_path, "peanut.toml")

        if not os.path.exists(config_path):
            return

        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        dependencies = data.get("dependencies", {})

        for name, constraint in dependencies.items():
            if name in self.installed:
                continue

            print(f"Resolving dependency {name} {constraint}")
            self.installer.install_from_github(name)

            dep_path = os.path.join(self.config.packages_dir, name.split("/")[-1])
            self.installed.add(name)

            # recursive resolve
            self.resolve_dependencies(dep_path)