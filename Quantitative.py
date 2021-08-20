import json
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os


def get_list_of_files(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles
# Lib JPEG
file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp")
#file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\test_case_msc")

c_files=[]
for s in file_list:
    #print(i)
     if s[-13:]=="_funcDef.json":
       c_files.append(s)
functiondef_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["name"]):
                functiondef_count=functiondef_count+1
c_files=[]
for s in file_list:
    #print(i)
     if s[-18:]=="_callExprMeta.json":
       c_files.append(s)
callexpr_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["name"]):
                callexpr_count=callexpr_count+1
c_files=[]
for s in file_list:
    #print(i)
     if s[-20:]=="_funcDecl_paths.json":
       c_files.append(s)
paths_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        paths_count=paths_count+len(data)
c_files=[]
for s in file_list:
    #print(i)
     if s[-13:]=="_funcDef.json":
       c_files.append(s)
tokens_count=0
tokens=[]
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["tokens"]):
                tokens_count=tokens_count+len(data[i]["tokens"])
                tokens.append(data[i]["tokens"])
print("functiondef_count",functiondef_count)
print("callexpr_count",callexpr_count)
print("paths_count",paths_count)
print("tokens_count",tokens_count)
flat_list = [item for sublist in tokens for item in sublist]

frequency_dist = nltk.FreqDist(flat_list)
sorted(frequency_dist,key=frequency_dist.__getitem__,reverse=True)[0:30]

large_words = dict([(k,v) for k,v in frequency_dist.items() if
len(k)>3])
frequency_dist = nltk.FreqDist(large_words)
wcloud = WordCloud().generate_from_frequencies(frequency_dist)
plt.imshow(wcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
# Lib Mpeg
file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libmpeg\\Temp")

c_files=[]
for s in file_list:
    #print(i)
     if s[-13:]=="_funcDef.json":
       c_files.append(s)
functiondef_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["name"]):
                functiondef_count=functiondef_count+1
c_files=[]
for s in file_list:
    #print(i)
     if s[-18:]=="_callExprMeta.json":
       c_files.append(s)
callexpr_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["name"]):
                callexpr_count=callexpr_count+1
c_files=[]
for s in file_list:
    #print(i)
     if s[-20:]=="_funcDecl_paths.json":
       c_files.append(s)
paths_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        paths_count=paths_count+len(data)
c_files=[]
for s in file_list:
    #print(i)
     if s[-13:]=="_funcDef.json":
       c_files.append(s)
tokens_count=0
tokens=[]
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["tokens"]):
                tokens_count=tokens_count+len(data[i]["tokens"])
                tokens.append(data[i]["tokens"])
print("functiondef_count",functiondef_count)
print("callexpr_count",callexpr_count)
print("paths_count",paths_count)
print("tokens_count",tokens_count)
flat_list = [item for sublist in tokens for item in sublist]

frequency_dist = nltk.FreqDist(flat_list)
sorted(frequency_dist,key=frequency_dist.__getitem__,reverse=True)[0:30]

large_words = dict([(k,v) for k,v in frequency_dist.items() if
len(k)>3])
frequency_dist = nltk.FreqDist(large_words)
wcloud = WordCloud().generate_from_frequencies(frequency_dist)
plt.imshow(wcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
# Lib Png
file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libpng\\Temp")


c_files=[]
for s in file_list:
    #print(i)
     if s[-13:]=="_funcDef.json":
       c_files.append(s)
functiondef_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["name"]):
                functiondef_count=functiondef_count+1
c_files=[]
for s in file_list:
    #print(i)
     if s[-18:]=="_callExprMeta.json":
       c_files.append(s)
callexpr_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["name"]):
                callexpr_count=callexpr_count+1
c_files=[]
for s in file_list:
    #print(i)
     if s[-20:]=="_funcDecl_paths.json":
       c_files.append(s)
paths_count=0
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        paths_count=paths_count+len(data)
c_files=[]
for s in file_list:
    #print(i)
     if s[-13:]=="_funcDef.json":
       c_files.append(s)
tokens_count=0
tokens=[]
for j in c_files:
    #getting the filename
    
    with open(str(j)) as f:
        data = json.load(f)
        for i in range(len(data)):
            if (data[i]["tokens"]):
                tokens_count=tokens_count+len(data[i]["tokens"])
                tokens.append(data[i]["tokens"])
print("functiondef_count",functiondef_count)
print("callexpr_count",callexpr_count)
print("paths_count",paths_count)
print("tokens_count",tokens_count)
flat_list = [item for sublist in tokens for item in sublist]

frequency_dist = nltk.FreqDist(flat_list)
sorted(frequency_dist,key=frequency_dist.__getitem__,reverse=True)[0:30]

large_words = dict([(k,v) for k,v in frequency_dist.items() if
len(k)>3])
frequency_dist = nltk.FreqDist(large_words)
wcloud = WordCloud().generate_from_frequencies(frequency_dist)
plt.imshow(wcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
