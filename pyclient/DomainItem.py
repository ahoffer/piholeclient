import json



# Example instance of DomainItem (JSON representation)
# {
#   "id": 111,
#   "type": 3,
#   "domain": ".*youtube.*",
#   "enabled": 1,
#   "date_added": 1637356294,
#   "date_modified": 1637356294,
#   "comment": "",
#   "groups": [
#     0
#   ]
# }
from ListType import ListType


class DomainItem:
    def __init__(self, pihole_dict):
        self.__dict__.update(pihole_dict)

    @property
    def enabled(self):
        return self.__dict__['enabled'] != 0

    @enabled.setter
    def enabled(self, b):
        self.__dict__['enabled'] = int(b)

    @property
    def type(self):
        return ListType(self.__dict__['type'])

    @type.setter
    def type(self, t):
        self.__dict__['type'] = t.value

    def flip(self):
        self.enabled = not self.enabled

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def as_pihole_form_data(self):
        data = self.__dict__.copy()
        # Pi-hole expects the string 'groups[]', not 'groups'
        if 'groups' in data:
            data['groups[]'] = data.pop('groups')
        # For some reason, enabled has to be renamed to "status"
        data['status'] = data.pop('enabled')
        return data
