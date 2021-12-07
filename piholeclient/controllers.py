from piholeclient.models import DomainItem, ListType


class YouTubeRule:

    def __init__(self, pihole):
        self.pihole = pihole

    def _get_youtube_rule(self):
        domainlist = self.pihole.get_domains()
        yt_rules = [x for x in domainlist if 'youtube' in x.domain and x.type is ListType.regex_blacklist]
        return next(iter(yt_rules), None)

    def youtube_is_blocked(self):
        rule = self._get_youtube_rule()
        return rule is not None and rule.enabled

    def flip(self):
        rule = self._get_youtube_rule()
        if rule:
            rule.flip()
            self.pihole.edit_domain(rule)
        else:
            new_rule = DomainItem({})
            new_rule.type = ListType.regex_blacklist
            new_rule.enabled = True
            new_rule.comment = 'Added by piholeclient python package'
            new_rule.domain = '.*youtube.*'
            self.pihole.add_domain(new_rule)

    def block(self):
        if not self.youtube_is_blocked():
            self.flip()
            
    def unblock(self):
        if self.youtube_is_blocked():
            self.flip()
