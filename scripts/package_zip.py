import os, zipfile

zip_filename = 'AI-POWERED-LEARNING-MANAGEMENT-SYSTEM.zip'
exclude_dirs = {'node_modules', 'dist', 'target', '.idea', '.vscode', '__pycache__', 'coverage'}
exclude_files = {zip_filename, 'package-lock.json', 'tsconfig.tsbuildinfo'}

total_files = 0
total_uncompressed_bytes = 0
git_files = 0

print(f"Creating {zip_filename} including .git history...")

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        # Allow .git but exclude node_modules, dist, etc.
        dirs[:] = [d for d in dirs if d.lower() not in exclude_dirs]
        for file in files:
            if file in exclude_files or file.endswith('.pyc'):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '.')
            zipf.write(full_path, rel_path)
            total_files += 1
            total_uncompressed_bytes += os.path.getsize(full_path)
            if '.git' in rel_path:
                git_files += 1

zip_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
print(f"==================================================")
print(f"ZIP ARCHIVE SUCCESSFULLY CREATED WITH GIT HISTORY")
print(f"==================================================")
print(f"Archive Path           : {os.path.abspath(zip_filename)}")
print(f"Total Packaged Files   : {total_files} (including {git_files} git metadata objects)")
print(f"Uncompressed Payload   : {total_uncompressed_bytes / (1024 * 1024):.2f} MB")
print(f"Compressed Archive Size: {zip_size_mb:.2f} MB ({os.path.getsize(zip_filename)} bytes)")
print(f"==================================================")
