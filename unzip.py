import zipfile, os

def extract(file_path):
    """
    Extracts ZIP-archive to 'temp' folder and returns extracted file list.
    If file is not ZIP-archive, returns empty list.
    """
    if zipfile.is_zipfile(file_path):
        Z = zipfile.ZipFile(file_path, 'r')
        clear_temp()
        Z.extractall('temp')
        file_list = Z.namelist()
        Z.close()
        return ['temp/' + item for item in file_list]
    else:
        return []

def clear_temp():
    """
    Function clear 'temp' folder from old files OR creates 'temp' folder if it not exists.
    """
    if os.path.exists("temp"):
        fl = os.walk("temp", topdown=False)
        for item in fl:
            for f1le in item[2]:
                os.remove(item[0] + "\\" + f1le)
                #print item[0] + "\\" + f1le
            for d1r in item[1]:
                os.rmdir(item[0] + "\\" + d1r)
                #print item[0] + "\\" + d1r
    else:
        os.mkdir("temp")