import sys
import os
import tarfile
import zipfile

print(sys.argv)

_, os_name, token = sys.argv
print('token length: ', len(token))
osn = os_name[0]

folder_name = os.path.realpath('./dist/qmlview/')

# Build archives
if os_name == 'windows-latest':
    # zip file
    filename = 'qmlview.zip'
    with zipfile.ZipFile(filename, 'w') as my_zip:
        my_zip.write('dist/qmlview/')

else:
    filename = 'qmlview.tar.gz'
    with tarfile.open(filename, 'w:gz') as my_tar:
        my_tar.add('./dist/qmlview/')

print(f'filename: {filename}')

with open('token.txt', 'w') as tok:
    tok.write(token)
    print('Finished writing token file')

# Login to GH
cmd = 'gh auth login --with-token < token.txt'
os.system(cmd)
print('Authenticated')
cmd1 = f'gh release create v3.1{osn} {filename}'
os.system(cmd1)
