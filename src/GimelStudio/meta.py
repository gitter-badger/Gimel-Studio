## ----------------------------------------------------------------------------
## Gimel Studio Copyright 2020 Noah Rahm, Correct Syntax. All rights reserved.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##
## FILE: meta.py
## AUTHOR(S): Noah Rahm
## PURPOSE: Define program meta info
## ----------------------------------------------------------------------------

# Program name
APP_NAME = "Gimel Studio"

# Program author
APP_AUTHOR = "Noah Rahm, Correct Syntax"

# Release version: [major].[minor].[build]
APP_VERSION = (0, 5, 0)
APP_VERSION_TAG = "beta"

# Whether this program is in development mode
# USAGE: Switch to False before building as .exe or similar package to
# enable/disable some end-user features that would otherwise hinder
# development and/or testing of the program.
APP_DEBUG = True

# Title string
APP_TITLE = "{0} v{1}.{2}.{3} {4}".format(
    APP_NAME,
    APP_VERSION[0],
    APP_VERSION[1],
    APP_VERSION[2],
    APP_VERSION_TAG
    )
