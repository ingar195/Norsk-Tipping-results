import json
import requests
import os


def getData(drawID, lottoType):

    url = f"https://www.norsk-tipping.no/api-{lottoType}/getResultInfo.json?drawID={drawID}"

    response = requests.get(url)
    tmpFile = "tmp.json"
    open(tmpFile, "wb").write(response.content)
    cleanFile(tmpFile)
    with open(tmpFile) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject


def cleanFile(fileName):
    with open(fileName, "r") as f:
        newContent = tuple(f.read().split('\n'))
    with open(fileName, "w") as f:
        f.write(newContent[1])


def parse(data, value, value2):
    var = data[value]
    print(var)
    if value2 == "starTable":
        return var, data[value2]
    return var


def csvWriter(csvFileName, value, value2):
    rw = "w"
    if os.path.exists(csvFileName):
        rw = "a"
    with open(csvFileName, mode=rw) as f:
        if value != None:
            for x in value:
                print(x)
                if value[len(value) - 1] != x:
                    f.write("{},".format(x))
                else:
                    f.write("{}".format(x))
            try:
                f.write(f",{value2[0]},{value2[1]}\n")
            except:
                f.write("\n")
               

def range(min, max, csvFile, lottoType, validTypes):
    if lottoType not in validTypes:
        print(f"{lottoType} is not in {validTypes}")
        quit()

    print(f"Checking: {max - min + 1} numbers")
    if max == 0:
        max = parse(getData("", lottoType), "drawID", "")

    while min <= max:

        print(f"{min}/{max}")
        if lottoType == "lotto":
            if min < 800:
                min = 800
            csvWriter(csvFile, parse(getData(min, lottoType), "mainTable", ""), "")
        elif lottoType == "keno":
            if min < 1400:
                min = 1400
            csvWriter(csvFile, parse(getData(min, lottoType), "drawNumbers", ""), "")
        elif lottoType == "eurojackpot":
            if min == 0:
                min = 1
            data1, data2 = parse(getData(min, lottoType),"mainTable", "starTable")
            csvWriter(csvFile, data1, data2)
        min += 1


validTypes = {"lotto", "keno", "eurojackpot"}
csvFile = "LottoNumbers.csv"

range(0, 0, csvFile, "eurojackpot", validTypes)
