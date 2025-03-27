import os
from common.constants import ROOT_PATH
from utils.FileUtil import readFile, writeFile

API_KEY_FILE_PATH = os.path.join(ROOT_PATH, "resource/apiKey.txt")


def getKey():
    return readFile(API_KEY_FILE_PATH)


def saveKey(key):
    writeFile(API_KEY_FILE_PATH, key)