import os

categories = {
    'Backend Core & Modules (Java)': ['.java'],
    'Frontend SPA (TS / TSX / CSS / HTML)': ['.ts', '.tsx', '.css', '.html'],
    'Database Schemas & Migrations (SQL)': ['.sql'],
    'Infrastructure, Docker & K8s (YAML / Nginx)': ['.yml', '.yaml', '.conf'],
    'Technical Architecture & Docs (Markdown)': ['.md'],
    'AI Prompts & Benchmark Datasets (JSON)': ['.json'],
    'Automation Scripts & Setup (Python)': ['.py'],
}

stats = {cat: {'files': 0, 'lines': 0, 'code': 0} for cat in categories}
stats['Other Configs'] = {'files': 0, 'lines': 0, 'code': 0}

exclude_dirs = {'.git', 'node_modules', 'dist', 'target', '.idea', '.vscode'}
ignored_files = {'package-lock.json', 'tsconfig.tsbuildinfo'}

total_files = 0
total_lines = 0

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for f in files:
        if f in ignored_files:
            continue
        ext = os.path.splitext(f)[1]
        filepath = os.path.join(root, f)
        
        matched_cat = 'Other Configs'
        for cat, matchers in categories.items():
            if ext in matchers or f in matchers:
                matched_cat = cat
                break
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file_obj:
                lines = file_obj.readlines()
                line_count = len(lines)
                code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('//') and not l.strip().startswith('#') and not l.strip().startswith('--')])
                stats[matched_cat]['files'] += 1
                stats[matched_cat]['lines'] += line_count
                stats[matched_cat]['code'] += code_lines
                total_files += 1
                total_lines += line_count
        except Exception:
            pass

print(f"{'Subsystem / Category':<45} | {'Files':>6} | {'Total Lines':>12} | {'Code Lines':>12}")
print("-" * 85)
for cat, data in stats.items():
    if data['files'] > 0:
        print(f"{cat:<45} | {data['files']:>6} | {data['lines']:>12} | {data['code']:>12}")
print("-" * 85)
total_code = sum(d['code'] for d in stats.values())
print(f"{'TOTAL CODEBASE':<45} | {total_files:>6} | {total_lines:>12} | {total_code:>12}")
