# coding: utf-8import platformos = platform.system()if os == 'Windows':    from . import wget_win as wget_privateelif os == 'Darwin':    from . import wget_mac as wget_privateelse:    raise Exception('Please add support for your platform')def wget(cmdline):    wget_private.wget(cmdline)    