import json
import os
from common.constants import ROOT_PATH
from utils.FileUtil import readFile, writeFile

MODEL_FILE_PATH = os.path.join(ROOT_PATH, "resource/model.txt")

MODEL_LIST_FILE_PATH = os.path.join(ROOT_PATH, "resource/modelList.txt")


def getModel():
    return readFile(MODEL_FILE_PATH)


def saveModel(model):
    writeFile(MODEL_FILE_PATH, model)


def getModelList():
    return json.loads(readFile(MODEL_LIST_FILE_PATH))


def saveModelList(modelList):
    writeFile(MODEL_LIST_FILE_PATH, str(modelList).replace("'", "\""))