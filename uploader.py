import sys
import os
import tarfile
import zipfile


os_name = sys.argv[1]

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
