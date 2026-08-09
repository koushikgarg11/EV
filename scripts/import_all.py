import os, sys, importlib, traceback
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
py_files = []
for root, dirs, files in os.walk(os.path.join(repo_root, 'src')):
    for f in files:
        if f.endswith('.py'):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, repo_root)
            mod = rel[:-3].replace(os.path.sep, '.')
            if mod.endswith('.__init__'):
                mod = mod[:-9]
            py_files.append(mod)

print('Found', len(py_files), 'modules')
failed = []
for m in sorted(set(py_files)):
    try:
        print('Importing', m)
        importlib.import_module(m)
    except Exception:
        print('FAILED', m)
        traceback.print_exc()
        failed.append(m)

print('\nSUMMARY:')
print('Total:', len(py_files))
print('Failed:', len(failed))
if failed:
    print('\n'.join(failed))
