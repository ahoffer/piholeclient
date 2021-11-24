from DomainItem import DomainItem
from ListType import ListType


class YouTubeRule:

    def __init__(self, pyhole):
        self.pyhole = pyhole

    def _getYouTubeRule(self):
        domainlist = self.pyhole.get_domains()
        yt_rules = [x for x in domainlist if 'youtube' in x.domain and x.type is ListType.regex_blacklist]
        return next(iter(yt_rules), None)

    def youtube_is_blocked(self):
        rule = self._getYouTubeRule()
        return rule is not None and rule.enabled

    def flip(self):
        rule = self._getYouTubeRule()
        if rule:
            rule.flip()
            r = self.pyhole.edit_domain(rule)
            print(r.text)
        else:
            new_rule = DomainItem({})
            new_rule.type = ListType.regex_blacklist
            new_rule.enabled = True
            new_rule.comment = 'Added by Py-hole'
            new_rule.domain = '.*youtube.*'
            r = self.pyhole.add_domain(new_rule)
            print(r.text)
