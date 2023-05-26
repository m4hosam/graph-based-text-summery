


fname = "C:\\Users\\Marah\\Desktop\\ornek.txt"

file = open(fname,'r', encoding='utf-8')
fileContent = file.read()
fileContent = fileContent.split('Main:')
fileContent = fileContent[1].split('Summary:')
newLineSep = fileContent[0].split('\n')
fileContent = [para.replace('\n','') for para in fileContent]

mainTextSentences = fileContent[0].split('.')
# title = fileContent[0].split('\n')[0]
summaryTextSentences = fileContent[1].split('.')
# for para in fileContent: 
#     para.replace('\n','')
title = [i for i in newLineSep if i][0]
mainTextSentences = [i for i in mainTextSentences if i]
summaryTextSentences = [i for i in summaryTextSentences if i]
print(title)
mainTextSentences[0] = mainTextSentences[0].replace(title,'') 
print(mainTextSentences)
print(summaryTextSentences)