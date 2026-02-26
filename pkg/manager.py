from .config import PackageConfig
from .installer import PackageInstaller
from .resolver import DependencyResolver


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
        import os
        return os.listdir(self.config.packages_dir)