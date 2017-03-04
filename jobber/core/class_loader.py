# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# Thomas Quintana <quintana.thomas@gmail.com>

import sys

def safe_import(fully_qualified_name, force_load=False):
    """
    Import a module and return None if the module isn't found.

    Positional arguments:
    fully_qualified_name -- the class fully qualified name.

    Keyword arguments:
    force_load -- a flag indicating if the module should be reloaded from disk.
    """

    cache = dict()
    # If force_load is True and the module has been previously loaded from
    # disk, we have to reload the module.
    if force_load and fully_qualified_name in sys.modules:
        if fully_qualified_name not in sys.builtin_module_names:
            # Remove any submodules because they won't appear in the newly loaded
            # module's namespace if they're already in sys.modules.
            sub_modules = [m for m in sys.modules if m.startswith('{}.'.format(fully_qualified_name))]
            for key in [fully_qualified_name] + sub_modules:
                # Prevent garbage collection.
                cache[key] = sys.modules[key]
                del sys.modules[key]

    # Try to load the desired module.
    separator_offset = fully_qualified_name.rfind('.')
    fully_qualified_name_base = fully_qualified_name[:separator_offset]
    fully_qualified_name_klass = fully_qualified_name[separator_offset + 1:]
    module = __import__(fully_qualified_name_base, globals(), locals(), [fully_qualified_name_klass], -1)
    return getattr(module, fully_qualified_name_klass)
