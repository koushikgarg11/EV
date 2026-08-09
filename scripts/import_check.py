import os, sys, importlib, traceback
# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
modules = ['src.config','src.components','src.components.key_insights','src.database.db_manager']
try:
    for m in modules:
        print('Importing', m)
        importlib.import_module(m)
    print('IMPORTS_OK')
except Exception:
    traceback.print_exc()
    raise
