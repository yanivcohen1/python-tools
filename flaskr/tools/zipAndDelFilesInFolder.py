import os
import shutil

DOWMLOAD_DIR = "C:\\Temp\\Adi\\adi\\secend_year\\proj2\\download\\"
ZIP_DIR = "C:\\Temp\\Adi\\adi\\secend_year\\proj2\\users\\"

def create_zip_file_from_folder(zipName):
    """  Creating the user pics ZIP file
    """
    path = ZIP_DIR + zipName
    archived = shutil.make_archive(path, 'zip', DOWMLOAD_DIR)

    if os.path.exists(path+".zip"):
        print(archived)
        # delete all files in folder
        for (dirpath, dirnames, filenames) in os.walk(DOWMLOAD_DIR):
            for filename in filenames:
                os.remove(dirpath + "\\" + filename)
    else:
        print("ZIP file not created")


if __name__ == '__main__':
  create_zip_file_from_folder("yaniv")
