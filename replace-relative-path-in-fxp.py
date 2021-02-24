# -*- coding: UTF-8 -*-
import re

unknownBlock1 = b'\x00\x00\x05\x91\x00\x00\x10\x0C\x00\x00\x00\x00'
path = r"E:\Steinberg\Vstplugins\LM-4 MarkII\Processed Studio Kits"
fxpPath = r"C:\Users\n\Desktop\04 Reso Kit_fix.fxp"

if __name__ == "__main__":
    newFxpContent = b""
    with open(fxpPath, 'rb') as fr:
        fxpContent = fr.read()
        pattern = re.compile(br"HaSm(.|\n)*?" +
                             bytes(path.replace("\\", "\\\\"), 'utf-8') +
                             br"(\\[\w ]*\\[\w ]*\.aif)")
        pos = 0
        while 1:
            m = pattern.search(fxpContent[pos:])
            if m is None:
                newFxpContent += fxpContent[pos:]
                break
            fNameWithParentDir = m.group(2).replace(b"\\", b"\\\\")
            repl = b'HaSm' + unknownBlock1 + fNameWithParentDir
            newFxpContent += re.sub(pattern,
                                    repl,
                                    fxpContent[pos:pos + m.end()],
                                    count=1)
            pos += m.end()
    with open(path + "\\04 Reso Kit_fix_test.fxp", 'wb') as fw:
        fw.write(newFxpContent)
