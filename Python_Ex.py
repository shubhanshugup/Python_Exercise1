import xml.etree.ElementTree as ET
import os
import pathlib
import shutil
import sys


def removeFailTestCases(dirList, path):
    try:
        for dirs in dirList:
            dirname = path + "/" + dirs + "/tc_log.xml"
            tree = ET.parse(dirname)

            # get the parent tag
            root = tree.getroot()
            # print the root (parent) tag along with its memory location
            for i in root.findall("TCASE"):
                if i.findtext("VERDICT") != "PASS":
                    brr = i.findtext("LOG")
                    brr = brr.replace("\\", "/")
                    drr = brr.split("/")

                    dir_del = path + dirs + "/" + drr[0] + "/"
                    root.remove(i)
                    shutil.rmtree(dir_del)

            tree.write(dirname)
    except Exception as ez:
        print(ez)


def list_dir(dir):
    path = pathlib.Path(dir)
    dir = []
    try:
        for item in path.iterdir():
            itemdataList = False
            for itemdata in item.iterdir():
                if itemdata.name.split("/")[-1] == "tc_log.xml":
                    itemdataList = True
            if itemdataList:
                if item.name.split("/")[-1] in ['A2DP', 'BAS', 'DID', 'DIS', 'HFP']:
                    dir.append(item.name.split("/")[-1])
        return dir
    except FileNotFoundError:
        print('Invalid directory')


def main():
    path = sys.argv
    path = path[1]
    path = path.replace("\\", "/")
    print(path)
    dirList = list_dir(path)
    removeFailTestCases(dirList, path)


main()