import os


def changeFile(oldFile, newFile=None, deleteOnly=False):
    if not newFile and not deleteOnly:
        return oldFile

    if oldFile and os.path.isfile(oldFile.path):
        os.remove(oldFile.path)
    return newFile
