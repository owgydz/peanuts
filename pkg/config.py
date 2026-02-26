import os


class PackageConfig:
    def __init__(self):
        self.base_dir = os.path.abspath(".peanuts")
        self.packages_dir = os.path.join(self.base_dir, "packages")
        self.cache_dir = os.path.join(self.base_dir, "cache")

        os.makedirs(self.packages_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)