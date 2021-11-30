# Pi-hole Python Client

Simple Python HTTP interface to pi-hole

## To Build

`python3 -m build`


## To Install From Files

`pip3 install dist/py_hole-0.0.1-py3-none-any.whl`

## API
Pi-hole does include a PHP script `admin/api.ph`.
It allows authentication with a `GET` request by adding a query parameter `auth` whose value is the double SHA-256 hash of the password.
However, the API offered limited functionality as of AdminLTE v5.8