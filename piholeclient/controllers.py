from models import ListType, DomainItem


class YouTubeRule:

    def __init__(self, pihole):
        self.pihole = pihole

    def _getYouTubeRule(self):
        domainlist = self.pihole.get_domains()
        yt_rules = [x for x in domainlist if 'youtube' in x.domain and x.type is ListType.regex_blacklist]
        return next(iter(yt_rules), None)

    def youtube_is_blocked(self):
        rule = self._getYouTubeRule()
        return rule is not None and rule.enabled

    def flip(self):
        rule = self._getYouTubeRule()
        if rule:
            rule.flip()
            r = self.pihole.edit_domain(rule)
            print(r.text)
        else:
            new_rule = DomainItem({})
            new_rule.type = ListType.regex_blacklist
            new_rule.enabled = True
            new_rule.comment = 'Added by piholeclient python package'
            new_rule.domain = '.*youtube.*'
            r = self.pihole.add_domain(new_rule)
            print(r.text)
