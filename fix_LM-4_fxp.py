# -*- coding: UTF-8 -*-
import re
import os
import sys

unknownBlock1 = b'\x00\x00\x05\x91\x00\x00\x10\x0C\x00\x00\x00\x00'  #0x91 or 0x93 ?
unknownBlock2 = bytes.fromhex(
    "000000003F80000000000001000000003F80000000000002000000003F8000000000000B0000000100000000000000000000000000000000"
)


def convertFxp(path):
    newFxpContent = b""
    fName = os.path.split(f)[1]
    with open(path, 'rb') as fr:
        fxpContent = fr.read()
        pattern = re.compile(br'HaSm(.|\n)*?(\\[\w ]*\\[\w ]*\.aif)')
        pos = 0
        count = 0
        while 1:
            m = pattern.search(fxpContent[pos:])
            if m is None:
                newFxpContent += insertUnknownBlock2(fxpContent[pos:], b'Harp')
                break
            fNameWithParentDir = m.group(2).replace(b"\\", b"\\\\")
            repl = b'HaSm' + unknownBlock1 + bytes(
                doubleBackslash(installPath), 'utf-8') + fNameWithParentDir
            block = re.sub(pattern,
                           repl,
                           fxpContent[pos:pos + m.end()],
                           count=1)
            if count > 0:
                if "Reso" in fName:  #Reso Kit preset has multiple samples in one pad
                    """ if findHaPa(block) is True:
                        block = insertUnknownBlock2(block, b'HaPa')
                    else:
                        block = insertUnknownBlock2(block, b'HaSm') """  #old function ,deprecated
                    pass
                else:
                    block = insertUnknownBlock2(block, b'HaPa')
            newFxpContent += block
            pos += m.end()
            count += 1
    with open(fName, 'wb') as fw:
        fw.write(newFxpContent)
        print("success!")


def insertUnknownBlock2(chunk, reg):
    pattern = re.compile(reg)
    m = pattern.search(chunk)
    if m is None:
        print("can't find insert position")
        return chunk
    else:
        return (chunk[:m.start()] + unknownBlock2 + chunk[m.start():])


def findHaPa(chunk):
    pattern = re.compile(b'HaPa')
    m = pattern.search(chunk)
    if m is None:
        return False
    else:
        return True


def doubleBackslash(str):
    str = str.replace("\\", "\\\\")
    str = str.replace("/", "\\\\")
    return str


if __name__ == "__main__":
    installPath = input(
        "Input your \"Processed Studio Kits\" folder path (ends with \"Processed Studio Kits\"):\n"
    )
    if installPath.endswith("\\") or installPath.endswith("/"):
        installPath = installPath[:-1]
    if len(sys.argv)>=2:
        fxpPath=sys.argv[2]
        
    else:
        try:
            fileList = os.listdir(installPath)
        except FileNotFoundError:
            print("file not found")
            sys.exit(0)
        fxpList = []
        for f in fileList:
            if f.lower().endswith(".fxp"):
                fxpList.append(f)
        if len(fxpList) == 0:
            print("can't find fxp files, please check directory")
            sys.exit(0)
        print(f"found {len(fxpList)} fxp files, processing...")
        for f in fxpList:
            print(f"converting {f} ...")
            convertFxp(installPath + "\\" + f)
            if f == fxpList[-1]:
                print("all finished, converted preset files are in current folder")
