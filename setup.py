#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-vtc.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum-vtc.png'])
    ]

setup(
    name="Electrum-VTC",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    packages=[
        'electrum_vtc',
        'electrum_vtc_gui',
        'electrum_vtc_gui.qt',
        'electrum_vtc_plugins',
        'electrum_vtc_plugins.audio_modem',
        'electrum_vtc_plugins.cosigner_pool',
        'electrum_vtc_plugins.email_requests',
        'electrum_vtc_plugins.greenaddress_instant',
        'electrum_vtc_plugins.hw_wallet',
        'electrum_vtc_plugins.keepkey',
        'electrum_vtc_plugins.labels',
        'electrum_vtc_plugins.ledger',
        'electrum_vtc_plugins.trezor',
        'electrum_vtc_plugins.digitalbitbox',
        'electrum_vtc_plugins.trustedcoin',
        'electrum_vtc_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_vtc': 'lib',
        'electrum_vtc_gui': 'gui',
        'electrum_vtc_plugins': 'plugins',
    },
    package_data={
        'electrum_vtc': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-vtc'],
    data_files=data_files,
    description="Lightweight Vertcoin Wallet",
    author="pknight",
    author_email="pknight@vertcoin.org",
    license="MIT Licence",
    url="https://electrum.vertcoin.org/",
    long_description="""Lightweight Vertcoin Wallet"""
)

# Optional modules (not required to run Electrum)
import pip
opt_modules = requirements_hw + ['pycryptodomex']
[ pip.main(['install', m]) for m in opt_modules ]
