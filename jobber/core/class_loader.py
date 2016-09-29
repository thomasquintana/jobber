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

def safe_import(fqn, force_load=False):
  '''
  Import a module and return None if the module isn't found.

  Positional arguments:
  fqn -- the class fully qualified name.

  Keyword arguments:
  force_load -- a flag indicating if a module should be reloaded from disk.
  '''

  cache = dict()
  try:
    # If force_load is True and the module has been previously loaded from
    # disk, we have to reload the module.
    if force_load and fqn in sys.modules:
      if fqn not in sys.builtin_module_names:
        # Remove any submodules because they won't appear in the newly loaded
        # module's namespace if they're already in sys.modules.
        sub_modules = [m for m in sys.modules if m.startswith(fqn + '.')]
        for key in [fqn] + sub_modules:
          # Prevent garbage collection.
          cache[key] = sys.modules[key]
          del sys.modules[key]
    module = __import__(fqn)
  except ImportError:
    return None
  for token in fqn.split('.')[1:]:
    try:
      module = getattr(module, token)
    except AttributeError:
      return None
  return module
