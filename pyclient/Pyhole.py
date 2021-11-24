from urllib.parse import urlunsplit, urljoin

import requests
from bs4 import BeautifulSoup

from DomainItem import DomainItem
from ListType import ListType


class Pyhole:
    def __init__(self, host, password):
        self.host = host
        self.password = password
        self.session = requests.Session()
        self.token = None
        self.url_base = urlunsplit(('http', self.host, '', '', ''))
        self.url_groups = urljoin(self.url_base, 'admin/scripts/pi-hole/php/groups.php')

    def _post(self, url, params, **kwargs):
        if not self.token:
            self.authenticate()
        response = self._primitive_post(url, params, **kwargs)
        # FYI: Pi-hole returns a 200 even if user is unauthenticated. :-(
        if 'expired' in response.text:
            self.authenticate()
            return self._primitive_post(url, params, **kwargs)
        return response

    def _primitive_post(self, url, params, **kwargs):
        params['token'] = self.token
        return self.session.post(url, data=params, **kwargs)

    def authenticate(self):
        response = self.session.post(urljoin(self.url_base, 'admin/index.php'),
                                     {'pw': self.password},
                                     allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        # TODO: Throw exception if token is not present in body. Could be bad password.
        self.token = soup.find(id="token").text

    def get_domains(self):
        params = {"action": "get_domains", "type": ListType.whitelist}
        response = self._post(self.url_groups, params)
        items = response.json()['data']
        return [DomainItem(x) for x in items]

    def edit_domain(self, item):
        return self._action('edit_domain', item)

    def replace_domain(self, item):
        return self._action('replace_domain', item)

    def add_domain(self, item):
        return self._action('add_domain', item)

    def _action(self, action, item):
        data = item.as_pihole_form_data()
        data.update({'action': action})
        return self._post(self.url_groups, data)
