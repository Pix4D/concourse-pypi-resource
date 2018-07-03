#!/usr/bin/env python

# Copyright (c) 2016-Present Pivotal Software, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from . import common, pypi
import json
import sys

import requests

def truncate_before(lst, value):
    for index, val in enumerate(lst):
        if val == value:
            return lst[index:]
    return [lst[-1]]

def check(instream):
    input = json.load(instream)
    common.merge_defaults(input)
    versions = pypi.get_package_versions(input)
    versions = [{'version': version} for version in versions]
    if input.get('version', None):
        version = input['version']['version']
        versions = truncate_before(versions, version)
    return versions

def main():
    print(json.dumps(check(sys.stdin)))

if __name__ == '__main__':
    main()
