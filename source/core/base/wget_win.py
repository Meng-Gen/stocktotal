# coding: utf-8import osdef wget(cmdline):    wget = os.path.abspath('./core/thirdparty/wget/wget.exe')    assert os.path.isfile(wget)      wget_cmdline = '''{wget} {cmdline}'''.format(wget=wget, cmdline=cmdline)    os.system(wget_cmdline)