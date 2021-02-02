import sys
import os
import tarfile
import shutil

version = os.environ['GITHUB_REF'].split('/')[-1]
print(f'version: {version}')

_, os_name, token = sys.argv
print('token length: ', len(token))
osn = os_name[0]

folder_name = os.path.realpath('./dist/qmlview/')

# Build archives
if os_name == 'windows-latest':
    # zip file
    filename = shutil.make_archive('qmlview', 'zip', folder_name)

else:
    # tar.gz file
    filename = shutil.make_archive('qmlview', 'gztar', folder_name)

print(f'filename: {filename}')

with open('token.txt', 'w') as tok:
    tok.write(token)
    print('Finished writing token file')

# Login to GH
cmd = 'gh auth login --with-token < token.txt'
os.system(cmd)
print('Authenticated')
cmd1 = f'gh release create {version}{osn} {filename}'
os.system(cmd1)
print('All Done')
