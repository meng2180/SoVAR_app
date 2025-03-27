def readFile(filePath):
    f = open(filePath, "r")
    fileLines = f.readlines()
    f.close()

    content = ""
    for line in fileLines:
        content += line
    return content


def writeFile(filePath, content):
    f = open(filePath, "w")
    f.write(content)
    f.close()