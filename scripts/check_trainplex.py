import os

def count_trainplex_prod_loc():
    prod_extensions = {'.java', '.ts', '.tsx', '.sql', '.js', '.jsx', '.css', '.html', '.yml', '.yaml', '.py', '.json'}
    exclude_dirs = {'.git', 'node_modules', 'dist', 'target', '.idea', '.vscode', 'test', 'tests', '__pycache__', 'coverage'}
    ignored_files = {'package-lock.json', 'tsconfig.tsbuildinfo'}
    
    total_files = 0
    total_loc = 0
    lang_stats = {}

    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d.lower() not in exclude_dirs and 'test' not in d.lower()]
        for f in files:
            if f in ignored_files or f.endswith('.pyc') or f.endswith('.zip'):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in prod_extensions:
                filepath = os.path.join(root, f)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                        lines = len(file_obj.readlines())
                        total_files += 1
                        total_loc += lines
                        lang = ext[1:].upper()
                        lang_stats[lang] = lang_stats.get(lang, {'files': 0, 'lines': 0})
                        lang_stats[lang]['files'] += 1
                        lang_stats[lang]['lines'] += lines
                except Exception:
                    pass

    print(f"==================================================")
    print(f"TRAINPLEX PROD LOC AUDIT (Tests/Generated Excluded)")
    print(f"==================================================")
    for lang, stat in sorted(lang_stats.items(), key=lambda x: x[1]['lines'], reverse=True):
        print(f"Language {lang:<6} | {stat['files']:>5} files | {stat['lines']:>7} LOC")
    print(f"--------------------------------------------------")
    print(f"TOTAL PROD FILES : {total_files}")
    print(f"TOTAL PROD LOC   : {total_loc} / 50000 (Target)")
    deficit = max(0, 50000 - total_loc)
    print(f"DEFICIT TO PASS  : {deficit} LOC")
    print(f"==================================================")
    return total_loc

if __name__ == '__main__':
    count_trainplex_prod_loc()
