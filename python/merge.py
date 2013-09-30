import os, re

srcPath = '../010-TSV/'
mergeFile = open('merged.txt', 'wt')
whiteSpace = re.compile(r'^(\s)*$')

srcFileNames = os.listdir(srcPath)
for srcFileName in srcFileNames:
    print('Merging file: ' + srcFileName)
    srcFile = open(srcPath + srcFileName, 'rt')
    for textLine in srcFile:
        if (whiteSpace.match(textLine) or textLine.startswith('LOT\tSUBLOT')):
            continue
        mergeFile.write(textLine)
    srcFile.close()

mergeFile.close()
