import json
from enum import Enum
from urllib.parse import urlunsplit, urljoin

import requests
from bs4 import BeautifulSoup


class ListType(Enum):
    whitelist = 0
    blacklist = 1
    regex_whitelist = 2
    regex_blacklist = 3

    def __repr__(self):
        return self.name


class Pihole:
    def __init__(self, host, password):
        assert host, "Host is missing"
        # Assumes authentication is enabled.
        assert password, "Password is missing"
        self.host = host
        self.password = password
        self.session = requests.Session()
        self.token = None
        self.url_base = urlunsplit(('http', self.host, '', '', ''))
        self.url_index = urljoin(self.url_base, 'admin/index.php')
        self.url_groups = urljoin(self.url_base, 'admin/scripts/pi-hole/php/groups.php')

    def _post(self, url, params, **kwargs):
        # First time through the token is uninitialized.
        response = self._post_with_token(url, params, **kwargs)
        # FYI: Pi-hole returns a 200 even if user is unauthenticated. :-(
        if 'expired' in response.text:
            self.authenticate()
            return self._post_with_token(url, params, **kwargs)
        return response

    def _post_with_token(self, url, params, **kwargs):
        params['token'] = self.token
        return self.session.post(url, data=params, **kwargs)

    def authenticate(self):
        response = self.session.post(self.url_index,
                                     data={'pw': self.password},
                                     allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        object = soup.find(id='token')
        assert object, 'Token was not returned. Bad password?'
        self.token = object.text

    def get_domains(self):
        params = {"action": "get_domains", "type": ListType.whitelist}
        response = self._post(self.url_groups, params)
        # Convert JSON response to model objects
        items = response.json()['data']
        return [DomainItem(x) for x in items]

    def edit_domain(self, model):
        return self._action('edit_domain', model)

    def replace_domain(self, model):
        return self._action('replace_domain', model)

    def add_domain(self, model):
        return self._action('add_domain', model)

    def _action(self, action, model):
        data = model.as_pihole_form_data()
        data.update({'action': action})
        return self._post(self.url_groups, data)


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
