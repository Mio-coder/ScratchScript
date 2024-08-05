class Meta:
    def __init__(self, semver, vm, agent):
        self.semver = semver
        self.vm = vm
        self.agent = agent

    def to_dict(self):
        return {
            "semver": self.semver,
            "vm": self.vm,
            "agent": self.agent
        }
