# -*- coding: utf-8 -*-
"""
    la la la
"""

from os import environ as oenv


def get(*env_keys, **settings):
    """Grab strings from the operating system environment

    :param settings: one of:
        * default
        * convert
        * config_key

    :returns: a dictionary of the config you asked for.
    """

    config = {}
    convert = settings.get('convert', lambda thing: thing)
    config_key = settings.get('config_key')
    if config_key:
        assert len(env_keys) == 1, 'mapping to a new key only makes sense for'\
            ' a single environment variable. or my imagination failed, sorry.'

    for env_key in env_keys:
        try:
            env_string = oenv[env_key]
            value = convert(env_string)
        except KeyError as env_keyerror:
            try:
                value = settings['default']
            except KeyError:
                raise env_keyerror

        key = config_key or env_key
        config.update({key: value})

    return config


def collect(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged


word_for_true = lambda word: word.lower() in ['true', 'yes', 'on' '1']
