import json

import requests
import os

from common.constants import ROOT_PATH
from logicProcess.infoExtract.ModelService import getModel
from src.entity.CrashInfo import CrashInfo
from logicProcess.infoExtract.KeyService import getKey
from utils.FileUtil import readFile, writeFile

GPT_URL = "https://cfcus02.opapi.win/v1/chat/completions"

PREPROCESS_PROMPT = "You should help me process a car accident description. You should analyse each sentence in the description. Once you found a sentence that contains impact actions, then drop all the sentences after." + \
             "Output the processed description." + \
             "The accident description is : "

PROMPT_FILE_NAME = os.path.join(ROOT_PATH, "resource/prompt.txt")

EXTRACT_PROMPT = readFile(PROMPT_FILE_NAME)

RECORD_FILE_NAME = os.path.join(ROOT_PATH, "resource/infoExtractLog.txt")


def extractInfo(filePath):
    report = readFile(filePath)
    err, result = postLLM(PREPROCESS_PROMPT + report)
    if err:
        return True, result
    err, result = postLLM(EXTRACT_PROMPT + result)
    if err:
        return True, result
    finalResult = processResult(result)
    return False, CrashInfo(finalResult)


def postLLM(prompt):
    headers = {
        "Authorization": 'Bearer ' + getKey(),
    }

    params = {
        "messages": [{"role": 'user', "content": prompt}],
        "model": getModel()
    }

    response = requests.post(GPT_URL, headers=headers, json=params, stream=False).json()
    if 'choices' not in response:
        return True, response['message']
    return False, response['choices'][0]['message']['content']


def processResult(result):
    start = result.index("{")
    end = result.rindex("}")
    return result[start:end + 1]


def getInfoExtractRecord():
    recordFileContent = readFile(RECORD_FILE_NAME)
    return json.loads(recordFileContent)


def saveInfoExtractRecord(recordString):
    writeFile(RECORD_FILE_NAME, recordString)
