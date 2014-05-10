# -*- coding: utf-8 -*-

import os.path
import gettext

import config

TRANSLATION_DOMAIN = "kerberus"
LOCALE_DIR = os.path.join(config.PATH_COMMON, "locale")

gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)
