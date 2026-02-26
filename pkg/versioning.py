class Version:
    def __init__(self, version_str):
        parts = version_str.split(".")
        if len(parts) != 3:
            raise ValueError("Version must be MAJOR.MINOR.PATCH")
        self.major = int(parts[0])
        self.minor = int(parts[1])
        self.patch = int(parts[2])

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        return (
            self.major == other.major and
            self.minor == other.minor and
            self.patch == other.patch
        )

    def __lt__(self, other):
        return (
            (self.major, self.minor, self.patch) <
            (other.major, other.minor, other.patch)
        )

    def satisfies(self, constraint):
        if constraint.startswith(">="):
            required = Version(constraint[2:])
            return self >= required

        if constraint.startswith("^"):
            required = Version(constraint[1:])
            return (
                self.major == required.major and
                self >= required
            )

        # exact
        return self == Version(constraint)

    def __ge__(self, other):
        return not self < other