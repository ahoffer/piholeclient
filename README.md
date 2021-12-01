# Pi-hole Python Client

Simple Python HTTP interface to pi-hole

## Package

### Build

    python3 -m build

### Install From File

    pip3 install dist/piholeclient-0.0.1-py3-none-any.whl

#### Upload to PyPi Test

    python3 -m twine upload --repository testpypi dist/*

    Username: __token__
    Password: API token


#### Install from PyPi Test

    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps piholeclient-ahoffer

### Import

    from piholeclient.models import Pihole

## Pi-hole's api.php

Pi-hole does include a PHP script `admin/api.ph`. It allows authentication with a `GET` request by adding a query
parameter `auth` whose value is the double SHA-256 hash of the password. However, the API offered limited functionality
as of AdminLTE v5.8