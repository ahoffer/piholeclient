from enum import Enum


class ListType(Enum):
    whitelist = 0
    blacklist = 1
    regex_whitelist = 2
    regex_blacklist = 3

    def __repr__(self):
        return self.name
