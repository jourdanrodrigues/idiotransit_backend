import os
import re


def read_dot_env(dot_env_path):
    try:
        with open(dot_env_path) as f:
            content = f.read()
    except IOError:
        content = ''

    for line in content.splitlines():
        match = re.match(r'\A(?P<key>[A-Za-z_0-9]+)=(?P<value>.*)\Z', re.sub(r'( +)?#(.+)?', '', line))
        if match:
            os.environ.setdefault(*match.groupdict().values())
