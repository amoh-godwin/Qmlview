import sys
import os
import tarfile
import zipfile


_, os_name, token = sys.argv
print('token length: ', len(token))

folder_name = os.path.realpath('./dist/qmlview/')

# Build archives
if os_name == 'windows-latest':
    # zip file
    filename = 'qmlview.zip'
    with zipfile.ZipFile(filename, 'w') as my_zip:
        my_zip.write(folder_name)

else:
    filename = 'qmlview.tar.gz'
    with tarfile.open(filename, 'w:gz') as my_tar:
        my_tar.add(folder_name)

print(f'filename: {filename}')

with open('token.txt', 'w') as tok:
    tok.write(token)
    print('Finished writing token file')
