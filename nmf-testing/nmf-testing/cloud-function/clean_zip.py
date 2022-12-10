# This file cleans the __MACOSX and __pycache__ folders from the zip file
# These two folders were causing errors with the deployment of the cloud function

from zipfile import ZipFile
import os


def check_archive_for_bad_filename(file):
  zip_file = ZipFile(file, 'r')
  for filename in zip_file.namelist():
    print(filename)
    if filename.startswith('__MACOSX/') or filename.startswith('__pycache__'):
      return True


def remove_bad_filename_from_archive(original_file, temporary_file):
  zip_file = ZipFile(original_file, 'r')
  for item in zip_file.namelist():
    buffer = zip_file.read(item)
    if not item.startswith('__MACOSX/') and not item.startswith('__pycache__'):
      if not os.path.exists(temporary_file):
        new_zip = ZipFile(temporary_file, 'w')
        new_zip.writestr(item, buffer)
        new_zip.close()
      else:
        append_zip = ZipFile(temporary_file, 'a')
        append_zip.writestr(item, buffer)
        append_zip.close()

  zip_file.close()


archive_filename = './Archive.zip'
temp_filename = './NewArchive.zip'

results = check_archive_for_bad_filename(archive_filename)
if results:
  print('Removing MACOSX and __pycache__ file from archive.')
  remove_bad_filename_from_archive(archive_filename, temp_filename)
else:
  print('No MACOSX file in archive.')
