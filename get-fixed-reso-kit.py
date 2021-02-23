# -*- coding: UTF-8 -*-
import re
import os
import sys
from urllib import request

fxpUrl = "https://gitee.com/millionlive/stepPic/raw/master/04_Reso_Kit_fix.fxp"
#fxpUrl= "https://cdn.jsdelivr.net/gh/nulla2011/fix-LM-4-MarkII/04_Reso_Kit_fix.fxp"
#fxpUrl= "https://raw.githubusercontent.com/nulla2011/fix-LM-4-MarkII/master/04_Reso_Kit_fix.fxp"

unknownBlock1 = b'\x00\x00\x05\x90\x00\x00\x10\x0C\x00\x00\x00\x00'  #0x91 or 0x93 or 0x90?


def getFxpFile(url):
    print("downloading file...")
    try:
        f = request.urlopen(url)
    except Exception:
        print('Network Error, you can try another fxpUrl')
        sys.exit(0)
    return f.read()


def replacePath(data, path):
    newContent = b""
    pattern = re.compile(
        br'HaSm(.|\n)*?E:\\Steinberg\\Vstplugins\\LM-4 MarkII\\Processed Studio Kits\\04 Reso Kit\\([\w ]*\.aif)'
    )
    pos = 0
    while 1:
        m = pattern.search(data[pos:])
        if m is None:
            newContent += data[pos:]
            break
        fName = m.group(2)
        repl = b'HaSm' + unknownBlock1 + bytes(path.replace(
            "\\", "\\\\"), 'utf-8') + b'\\\\04 Reso Kit\\\\' + fName
        newContent += re.sub(pattern, repl, data[pos:pos + m.end()], count=1)
        pos += m.end()
    return newContent


if __name__ == "__main__":
    installPath = input(
        "Input your \"Processed Studio Kits\" folder path (ends with \"Processed Studio Kits\"):\nexample: C:\Program Files (x86)\Steinberg\Vstplugins\LM-4 MarkII\Processed Studio Kits\n"
    )
    assert os.path.isdir(installPath), "illegal path"
    if installPath.endswith("\\") or installPath.endswith("/"):
        installPath = installPath[:-1]
    fxpData = getFxpFile(fxpUrl)
    print(f"converting to new fxp...")
    newFxpContent = replacePath(fxpData, installPath)
    with open(installPath + "\\04 Reso Kit_fix.fxp", 'wb') as fw:
        fw.write(newFxpContent)
    print(f"Success, fixed preset file is in \"{installPath}\"")
