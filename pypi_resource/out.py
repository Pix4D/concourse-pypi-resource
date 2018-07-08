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

import glob
import json
import os
import subprocess
import sys

from . import common, pipio


def find_package(pattern, srcdir):
    files = glob.glob(os.path.join(srcdir, pattern))
    common.msg('Glob {} matched files: {}', pattern, files)
    files = sorted(files, key=common.get_package_version)
    return files[-1]


def upload_package(pkgpath, input):
    repocfg = input['source']['repository']
    twine_cmd = ['twine', 'upload']

    url, unused_hostname = pipio.get_pypi_url(input, 'out') 
    twine_cmd.extend(['--repository-url', url])

    twine_cmd.append('--username')
    twine_cmd.append(repocfg.get('username', os.getenv('TWINE_USERNAME')))
    twine_cmd.append('--password')
    twine_cmd.append(repocfg.get('password', os.getenv('TWINE_PASSWORD')))
    twine_cmd.append(pkgpath)

    subprocess.run(twine_cmd, stdout=sys.stderr.fileno(), check=True)


def out(srcdir, input):
    common.merge_defaults(input)
    common.msg('Finding package to upload')
    pkgpath = find_package(input['params']['glob'], srcdir)
    version = common.get_package_version(pkgpath)
    common.msg('Uploading {} version {}', pkgpath, version)
    upload_package(pkgpath, input)
    return {'version': {'version': str(version)}}


def main():
    print(json.dumps(out(sys.argv[1], json.load(sys.stdin))))


if __name__ == '__main__':
    main()
