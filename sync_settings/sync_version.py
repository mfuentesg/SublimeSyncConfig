# -*- coding: utf-8 -*

import sublime

from .libs import path, settings
from .libs.gist import Gist

file_path = path.join(os.path.expanduser('~'), '.sync_settings', 'sync.json')


def get_local_version():
    if not path.exists(file_path):
        return {}
    try:
        with open(file_path) as f:
            return sublime.decode_value(f.read())
    except:
        pass
    return {}


def get_remote_version():
    try:
        commit = Gist(
            http_proxy=settings.get('http_proxy'),
            https_proxy=settings.get('https_proxy')
        ).commits(settings.get('gist_id'))[0]
        return {
            'hash': commit['version'],
            'created_at': commit['committed_at'],
        }
    except:
        pass
    return {}


def update_config_file(info):
    with open(file_path, 'w') as f:
        f.write(sublime.encode_value(info, True))


def show_update_dialog(on_yes=None):
    msg = (
        'Sync Settings:\n\n'
        'Your settings seem out of date.\n\n'
        'Do you want to download the latest version?'
    )
    if sublime.yes_no_cancel_dialog(msg) == sublime.DIALOG_YES:
        # call download command
        if on_yes:
            on_yes()


def upgrade():
    local = get_local_version()
    if not local.get('hash', ''):
        show_update_dialog()
        return
    remote = get_remote_version()
    if local['hash'] == remote.get('hash', ''):
        return
    # TODO: check if get remote version failed
    if local['created_at'] < remote.get('created_at', ''):
        show_update_dialog(
            on_yes=lambda: update_config_file(remote)
        )
