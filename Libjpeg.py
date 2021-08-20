import clang
import clang.cindex
import os
import json
import typing
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab

clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')
index = clang.cindex.Index.create()
def extract_token(translation_unit, extent, punctuation_boolean, kind_boolean):
    res_tokens = []
    tokens = translation_unit.get_tokens(extent=extent)
    for token in tokens:
        if punctuation_boolean is False:
            if token.kind != clang.cindex.TokenKind.PUNCTUATION:
                if kind_boolean is False:
                    if token.kind != clang.cindex.TokenKind.COMMENT:
                        res_tokens.append(token.spelling)
                else:
                    res_tokens.append({"kind": str(token.kind), "spelling": str(token.spelling)})
        else:
            if kind_boolean is False:
                res_tokens.append(token.spelling)
            else:
                res_tokens.append({"kind": str(token.kind), "spelling": str(token.spelling)})
    return res_tokens
def writeToJSONFile(path,fileName,data):
    os.chdir(path)
    filePathNameWExt = str(path)+'\\'+str(fileName) + '.json'
    #os.remove(str(filePathNameWExt))
    with open(filePathNameWExt, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
def clearing_the_global_lists():
    CALL_EXPR = []           
    STRUCT_DECL = []
    FIELD_DECL= []
    ENUM_DECL= []
    FUNCTION_DECL= []
    PARM_DECL= []
    VAR_DECL= []
    TYPEDEF_DECL= []
    ENUM_CONSTANT_DECL=[]

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

def get_kids_edges(function_names_kids, map_fd_fc,callExpr_funcDecl):
    res=[]
    for kid_name in function_names_kids:
        #if kid_name is in map_fd_fc:
        tmp = callExpr_funcDecl.get(kid_name)
        if (kid_name!='None'):
            if tmp is not None:
                for kid in tmp:
                    if (kid_name,kid) not in res:
                        if kid is not None:
                            res.append((kid_name,kid))
                            list_kids_edges = get_kids_edges(tmp,map_fd_fc,callExpr_funcDecl)
                            for edge in list_kids_edges:
                                res.append(edge)
    return res
def print_function():
    print("CALL_EXPR",CALL_EXPR)
    print("FIELD_DECL",FIELD_DECL)
    print("ENUM_DECL",ENUM_DECL)
    print("ENUM_CONSTANT_DECL",ENUM_CONSTANT_DECL)
    print("FUNCTION_DECL",FUNCTION_DECL)
    print("PARM_DECL",PARM_DECL)
    print("VAR_DECL",VAR_DECL)
    print("TYPEDEF_DECL",TYPEDEF_DECL)

def dump_children(node):
    for c in node.get_children():
        print (c.kind, c.type.spelling)
        dump_children(c)
def func_call_another_file(function_name, list_of_filenames):
  
    for file in list_of_filenames:
        #print("function_name"+file)
        if "_funcDef" in file:
            with open(file) as input_file:
                data = json.load(input_file)
                for item in data:
#                     print (str(function_name) + " " +str(item['name']))
                    #TODO: compare string with string after removing the filename(path) from the name
                    initial_filename=(os.path.basename(file).split('_'))
                    find_list=(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+":"+function_name)
                    #print("function_name"+find_list)
                    if item["name"]==find_list:
                        #print("find_list"+find_list)
                        if(find_list=="jcstest.c:my_output_message"):
                            print("lol")
                        #return find_list
                        return item["filename"][item["filename"].rfind("\\") + 1:]
                        #print((item["filename"][item["filename"].rfind("\\") + 1:))
    return "externalLibrary.h"
CALL_EXPR = []
STRUCT_DECL = []
FIELD_DECL= []
ENUM_DECL= []
FUNCTION_DECL= []
PARM_DECL= []
VAR_DECL= []
TYPEDEF_DECL= []
ENUM_CONSTANT_DECL=[]
TOKENS = []
# Parse of childrens and extracting desired info
def traverse(node):
        for child in node.get_children():
            if str(child.location.file) == globalFileName:
#                 print(str(child.kind) + " "+ str(child.spelling))
                #if child.kind != clang.cindex.CursorKind.briefComment
                if child.kind != clang.cindex.TokenKind.COMMENT:
                    TOKENS.append(child.spelling)
                if child.kind == clang.cindex.CursorKind.VAR_DECL:
                    VAR_DECL.append(child)

                if child.kind == clang.cindex.CursorKind.CALL_EXPR:
                    CALL_EXPR.append(child)
                    #print(str(child.spelling) + " " + str(child.extent.start.line) + ":" + str(child.extent.start.column))
                    
                if child.kind == clang.cindex.CursorKind.STRUCT_DECL:
                    STRUCT_DECL.append(child)
                    
                if child.kind == clang.cindex.CursorKind.PARM_DECL:
                    PARM_DECL.append(child)
                        
                if child.kind == clang.cindex.CursorKind.FIELD_DECL:
                    FIELD_DECL.append(child)
                        
                if child.kind == clang.cindex.CursorKind.ENUM_DECL:
                    ENUM_DECL.append(child)
                        
                if child.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
                    ENUM_CONSTANT_DECL.append(child)

                if child.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
                    TYPEDEF_DECL.append(child)

                if child.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                    FUNCTION_DECL.append(child)
                traverse(child)
import networkx as nx
import random

    
def hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):

    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.  
    Licensed under Creative Commons Attribution-Share Alike 
    
    If the graph is a tree this will return the positions to plot this in a 
    hierarchical layout.
    
    G: the graph (must be a tree)
    
    root: the root node of current branch 
    - if the tree is directed and this is not given, 
      the root will be found and used
    - if the tree is directed and this is given, then 
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given, 
      then a random choice will be used.
    
    width: horizontal space allocated for this branch - avoids overlap with other branches
    
    vert_gap: gap between levels of hierarchy
    
    vert_loc: vertical location of root
    
    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  #allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5, pos = None, parent = None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''
    
        if pos is None:
            pos = {root:(xcenter,vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)  
        if len(children)!=0:
            dx = width/len(children) 
            nextx = xcenter - width/2 - dx/2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G,child, width = dx, vert_gap = vert_gap, 
                                    vert_loc = vert_loc-vert_gap, xcenter=nextx,
                                    pos=pos, parent = root)
        return pos

            
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
def filter_node_list_by_node_kind(nodes: typing.Iterable[clang.cindex.Cursor],kinds: list)-> typing.Iterable[clang.cindex.Cursor]:
    result = []
    for k in nodes:
        if k.kind in kinds:
            result.append(k)
    return result
            
def filter(j):
    global CALL_EXPR
    global TOKENS
    funcDef = []
    callExprMeta = []
    callExprMetaNot=[]
    callExpr_funcDecl = {}
    ls1=[]
    index = clang.cindex.Index.create()
    translation_unit = index.parse(j, ['-x', 'c++', '-std=c++17', '-D__CODE_GENERATOR__'])
    
    all_classes = filter_node_list_by_node_kind(translation_unit.cursor.get_children(), [clang.cindex.CursorKind.FUNCTION_DECL])
    for i in all_classes:
        CALL_EXPR = []
        TOKENS.clear()
        traverse(i)
#       Generation of the FuncDef List
        if(i.location.file.name == j):    
            tmp = {'name': str(os.path.basename(i.location.file.name))+ ":"+ str(i.spelling),
                            'filename' : str(i.location.file.name),
                            'loc_start_line': str(i.extent.start.line), 
                            'loc_start_col' : str(i.extent.start.column),
                            'loc_end_line'  : str(i.extent.end.line), 
                            'loc_end_col'   : str(i.extent.end.column),
                            'function_calls': [],
                            'tokens': extract_token(translation_unit, i.extent, False, False)}
            if len(tmp["tokens"])<1:
                for token in TOKENS:
                    tmp['tokens'].append(str(token))
            funcDef.append(tmp)


#         Generation of the callExprMeta List
        #print(CALL_EXPR)
        for child in CALL_EXPR:
            if(child.location.file.name == j):
                #funcDefForChild = child.get_funcDef()
                try:
                    funcDefForChild = child.get_definition() 

                    
                    val = {"name": str(os.path.basename(funcDefForChild.location.file.name))+ ":"+ str(child.spelling),
                                "filename" : str(child.location.file.name),
                                "loc_start_line": str(child.extent.start.line),
                                "loc_start_col" : str(child.extent.start.column),
                                "loc_end_line"  : str(child.extent.end.line),
                                "loc_end_col"   : str(child.extent.end.column)}


                    callExprMeta.append(val)
                except:
                    #funcDefForChild = child.get_definition() 

                    
                    val = {"name":"externalLibrary.h:"+str(child.spelling),
                                "filename" : str(child.location.file.name),
                                "loc_start_line": str(child.extent.start.line),
                                "loc_start_col" : str(child.extent.start.column),
                                "loc_end_line"  : str(child.extent.end.line),
                                "loc_end_col"   : str(child.extent.end.column)}


                    callExprMeta.append(val)

#         Generation of the callExpr_funcDecl List                
        for func in funcDef:
            callExpr_funcDecl[func['name']] = []
            for callExpr in callExprMeta:
                if (int(callExpr['loc_start_line']) < int(func['loc_end_line']) and 
                     int(callExpr['loc_start_line']) > int(func['loc_start_line'])):
                     callExpr_funcDecl[func['name']].append(callExpr['name'])
                elif (int(callExpr['loc_end_line']) == int(func['loc_end_line']) and 
                     int(callExpr['loc_start_col']) > int(func['loc_start_line'])and int(callExpr['loc_start_col']) < int(func['loc_end_col'])):
                     callExpr_funcDecl[func['name']].append(callExpr['name'])#end_line == compare column no
                elif (int(callExpr['loc_start_line']) == int(func['loc_start_line']) and 
                     int(callExpr['loc_start_col']) > int(func['loc_start_line'])and int(callExpr['loc_start_col']) < int(func['loc_end_col'])):
                     callExpr_funcDecl[func['name']].append(callExpr['name'])#start_line == compare column no
        




    #writeToJSONFile(directory,'funcDef', funcDef)
    location1=(os.path.basename(j))
    location=location1.split(".")
    location=location[0]+location[1]
    filename = "./Temp/"+str(location)+"_funcDef.json"
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(funcDef, fp, ensure_ascii=False, indent=4)
    filename1 = "./Temp/"+str(location)+"_callExprMeta.json"
    with open(filename1, 'w', encoding='utf-8') as fp:
        json.dump(callExprMeta, fp, ensure_ascii=False, indent=4)
    filename2 = "./Temp/"+str(location)+"_callExpr_funcDecl.json"
    with open(filename2, 'w', encoding='utf-8') as fp:
        json.dump(callExpr_funcDecl, fp, ensure_ascii=False, indent=4)
files_executed = 0

file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\libjpeg-turbo-master\\libjpeg-turbo-master")
#file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\test_case_msc")
directory='Temp'
if not os.path.exists(directory):
    os.makedirs(directory)
c_files=[]
for s in file_list:
    #print(i)
    if s[-2:]==".c" or s[-2:]==".h":
       c_files.append(s)
       
for j in c_files:
    #clearing_the_global_lists()
    #globalFileName=str(j)
    #print("the results for the file"+j)
    #filter(j)
    #print(j)
    try:
            clearing_the_global_lists()
            globalFileName=str(j)
            print("There are " + str(j) + " files which executed.")
            filter(j)
            files_executed=files_executed+1
    except Exception as e:
            print("There are " + str(j) + " files which failed:" )
print("Total files executed:"+str(files_executed))
def filter_node_list_by_node_kind(nodes: typing.Iterable[clang.cindex.Cursor],kinds: list)-> typing.Iterable[clang.cindex.Cursor]:
    result = []
    for k in nodes:
        if k.kind in kinds:
            result.append(k)
    return result
            
def filter(j):
    global CALL_EXPR
    global TOKENS
    funcDef = []
    callExprMeta = []
    callExprMetaNot=[]
    callExpr_funcDecl = {}
    ls1=[]
    index = clang.cindex.Index.create()
    translation_unit = index.parse(j, ['-x', 'c++', '-std=c++17', '-D__CODE_GENERATOR__'])
    
    all_classes = filter_node_list_by_node_kind(translation_unit.cursor.get_children(), [clang.cindex.CursorKind.FUNCTION_DECL])
    for i in all_classes:
        CALL_EXPR = []
        TOKENS.clear()
        traverse(i)
#       Generation of the FuncDef List
        if(i.location.file.name == j):    
            tmp = {'name': str(os.path.basename(i.location.file.name))+ ":"+ str(i.spelling),
                            'filename' : str(i.location.file.name),
                            'loc_start_line': str(i.extent.start.line), 
                            'loc_start_col' : str(i.extent.start.column),
                            'loc_end_line'  : str(i.extent.end.line), 
                            'loc_end_col'   : str(i.extent.end.column),
                            'function_calls': [],
                            'tokens': extract_token(translation_unit, i.extent, False, False)}
            if len(tmp["tokens"])<1:
                for token in TOKENS:
                    tmp['tokens'].append(str(token))
            funcDef.append(tmp)


#         Generation of the callExprMeta List
        #print(CALL_EXPR)
        for child in CALL_EXPR:
            if(child.location.file.name == j):
                #funcDefForChild = child.get_funcDef()
                try:
                    funcDefForChild = child.get_definition() 

                    
                    val = {"name": str(os.path.basename(funcDefForChild.location.file.name))+ ":"+ str(child.spelling),
                                "filename" : str(child.location.file.name),
                                "loc_start_line": str(child.extent.start.line),
                                "loc_start_col" : str(child.extent.start.column),
                                "loc_end_line"  : str(child.extent.end.line),
                                "loc_end_col"   : str(child.extent.end.column)}


                    callExprMeta.append(val)
                except:
                    #funcDefForChild = child.get_definition() 
                    try:
                        func_filename= func_call_another_file(child.spelling, get_list_of_files('C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Temp'))
                        val = {"name": func_filename + ":" +str(child.spelling),
                                "filename" : str(child.location.file.name),
                                "loc_start_line": str(child.extent.start.line),
                                "loc_start_col" : str(child.extent.start.column),
                                "loc_end_line"  : str(child.extent.end.line),
                                "loc_end_col"   : str(child.extent.end.column)}
                    except:
                        val = {"name":"externalLibrary.h:"+str(child.spelling),
                                "filename" : str(child.location.file.name),
                                "loc_start_line": str(child.extent.start.line),
                                "loc_start_col" : str(child.extent.start.column),
                                "loc_end_line"  : str(child.extent.end.line),
                                "loc_end_col"   : str(child.extent.end.column)}

                    callExprMeta.append(val)

#         Generation of the callExpr_funcDecl List                
        for func in funcDef:
            callExpr_funcDecl[func['name']] = []
            for callExpr in callExprMeta:
                if (int(callExpr['loc_start_line']) < int(func['loc_end_line']) and 
                     int(callExpr['loc_start_line']) > int(func['loc_start_line'])):
                     callExpr_funcDecl[func['name']].append(callExpr['name'])
                elif (int(callExpr['loc_end_line']) == int(func['loc_end_line']) and 
                     int(callExpr['loc_start_col']) > int(func['loc_start_line'])and int(callExpr['loc_start_col']) < int(func['loc_end_col'])):
                     callExpr_funcDecl[func['name']].append(callExpr['name'])#end_line == compare column no
                elif (int(callExpr['loc_start_line']) == int(func['loc_start_line']) and 
                     int(callExpr['loc_start_col']) > int(func['loc_start_line'])and int(callExpr['loc_start_col']) < int(func['loc_end_col'])):
                     callExpr_funcDecl[func['name']].append(callExpr['name'])#start_line == compare column no
        




    #writeToJSONFile(directory,'funcDef', funcDef)
    location1=(os.path.basename(j))
    location=location1.split(".")
    location=location[0]+location[1]
    filename = "./Temp/"+str(location)+"_funcDef.json"
    with open(filename, 'w', encoding='utf-8') as fp:
        json.dump(funcDef, fp, ensure_ascii=False, indent=4)
    filename1 = "./Temp/"+str(location)+"_callExprMeta.json"
    with open(filename1, 'w', encoding='utf-8') as fp:
        json.dump(callExprMeta, fp, ensure_ascii=False, indent=4)
    filename2 = "./Temp/"+str(location)+"_callExpr_funcDecl.json"
    with open(filename2, 'w', encoding='utf-8') as fp:
        json.dump(callExpr_funcDecl, fp, ensure_ascii=False, indent=4)
file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\libjpeg-turbo-master\\libjpeg-turbo-master")
#file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\test_case_msc")
directory='Temp'
if not os.path.exists(directory):
    os.makedirs(directory)
c_files=[]
for s in file_list:
    #print(i)
    if s[-2:]==".c" or s[-2:]==".h":
       c_files.append(s)
       
for j in c_files:
    try:
            clearing_the_global_lists()
            globalFileName=str(j)
            filter(j)
            files_executed=files_executed+1
    except Exception as e:
            files_executed=files_executed+1
# Call_graph
import json
#file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Msc Dissertation\\libjpeg-turbo-master\\libjpeg-turbo-master")
file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp")
#file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\test_case_msc\\lol")

# function_1 check_is_from_same_file: add the kids into kid_list; remove current kid; add res_list(kid;kids_kid)
# function_2 check_is_from_another_file: add the kids into kid_list; remove current kid; add res_list(kid;kids_kid)
def check_is_from_same_file(function_call, filename,map_fd_fc):
    tmp_filename = function_call[:function_call.index(".")]
    if tmp_filename == filename:
        function_call_kids=map_fd_fc.get(function_call)
        if function_call_kids is not None:
            return function_call_kids
    return []
    
def check_is_from_another_file(function_call, list_of_filenames):
    
#     print(list_of_filenames)
    tmp_filename = function_call[:function_call.index(".")]
    for file in list_of_filenames:
        tmp_file=(os.path.basename(file).split('_'))
#         print("1 " +str(tmp_filename) + " 2 "+str(tmp_file[0]))
        if tmp_filename == str(tmp_file[0][-1:]):
#             print("got here")
            with open(file) as input_file:
                map_fd_fc = json.load(input_file)
                function_call_kids=map_fd_fc.get(function_call)
                if function_call_kids is not None:
                #print("extracted:"+str(function_call_kids))
                    return function_call_kids
    return []
#getting the files
c_files=[]
get_files=[]
for s in file_list:
    #print(i)
    if s[-14:]=="_funcDecl.json":
       c_files.append(s)
for file in c_files:
    get=(os.path.basename(file).split('_'))
    get_files.append(get)

for j in c_files:
    initial_filename=(os.path.basename(j).split('_'))
    #getting the filename
    kid_list=[]
    with open(j) as f:
        res_edge = []
        data = json.load(f)
        
        #print(data)
    #getting the main function
        #print(j)
        kid_list=data.get(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')
        if (kid_list!='None'):
            if kid_list is not None:
                #print(kid_list)
                for tmp_kid in kid_list:
                    kid3=tmp_kid.split(":")
                    if(kid3[0]!="externalLibrary.h" and kid3[0]!="stdio.h"):
                        res_edge.append((initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main',tmp_kid))
#                     kid_list.remove(tmp_kid)
                while len(kid_list) > 0:
    #                     print(kid_list)
                        kid = kid_list[0]
                       # print(kid)
                        
                        
                        tmp_kid_list = check_is_from_same_file(kid,initial_filename[0][:-1],data)
                        kid_list.extend(tmp_kid_list)
                        for tmp_kid in tmp_kid_list:
                            kid1=tmp_kid.split(":")
                            
                            if(kid1[0]!="externalLibrary.h" and kid1[0]!="stdio.h"):
                               # print(kid1)
                                res_edge.append((kid,tmp_kid))
                        if len(tmp_kid_list)==0:
                            
                            tmp_kid_list = check_is_from_another_file(kid,c_files)
                            kid_list.extend(tmp_kid_list)
                            for tmp_kid in tmp_kid_list:
                                kid2=tmp_kid.split(":")
                                if(kid2[0]!="externalLibrary.h" and kid2[0]!="stdio.h" ):
                                    res_edge.append((kid,tmp_kid))
                        kid_list.remove(kid_list[0])
       
        location1=(os.path.basename(j))
        location=location1.split(".")
        location=location[0]
        filename = "./Temp/"+str(location)+"_call_graph.json"
        if (data.get(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')!=None):
            with open(filename, 'w') as fp:
                json.dump(res_edge, fp, ensure_ascii=False, indent=4)
        #print("final " + str(res_edge))

        if (data.get(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')!=None):
            test=(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')
            print(j)
            print(test)
            G = nx.DiGraph()
            #output = ("main", "function")
            # Edges
            G.add_edges_from(res_edge)

            pos = nx.spring_layout(G)
            # plot the nodes
            nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                                   node_color = 'y', node_size = 30)
            nx.draw_networkx_labels(G, pos)
            # plot the edges
            nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='b', arrows=True)
            # plt.show()
            plt.savefig(filename+".pdf")
            plt.clf()
            leafs = [node for node in G.nodes() if G.out_degree(node)==0 ]
            nodesin = [node for node in G.nodes()]
            a1=[]
            #for i in nodesin:
            a1=[]
            for i in nodesin:
                for path in nx.all_simple_paths(G, source=(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main'), target=i):
                    a1.append(path)
            #nodes_reverse=nodesin.reverse()
            #print(nodesin)
            #print(leafs)
            #print(a1)
            filename = "./Temp/"+str(location)+"_peel.json"
            #if (data.get(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')!=None):
            with open(filename, 'w') as fp:
                json.dump(leafs, fp, ensure_ascii=False, indent=4)
            filename1 = "./Temp/"+str(location)+"_nodes.json"
            #if (data.get(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')!=None):
            with open(filename1, 'w') as fp:
                json.dump(nodesin, fp, ensure_ascii=False, indent=4)
            filename1 = "./Temp/"+str(location)+"_paths.json"
            #if (data.get(initial_filename[0][:-1]+"."+initial_filename[0][-1:]+':main')!=None):
            with open(filename1, 'w') as fp:
                json.dump(a1, fp, ensure_ascii=False, indent=4)
# Entropy
import dit
import re
import hashlib
from collections import Counter
from decimal import *


def utf_encode(string):
    if isinstance(string, str):
        string = string.encode('utf-8')
    return str(string)


def is_list_empty(input_list):
    if isinstance(input_list, list):  # Is a list
        return all(map(is_list_empty, input_list))
    return False


# Splits elements of list for uppercase
def prepare_to_process(input_list, further_tokenizing):
    final_list = []
    input_list = [item for item in input_list if item]
    if (any(isinstance(i, list) for i in input_list)) is True:
        input_list = [a for b in input_list for a in b]
    input_list = [item for item in input_list if item != 'None']
    input_list = [item for item in input_list if item != '']

    if further_tokenizing is True:
        for item in input_list:
            words_list = re.findall('([A-Z](?=[a-z]+[0-9]*)[a-z]*[0-9]*|[A-Z]+(?=[A-Z]{2,})[A-Z])', item)
            if len(words_list) > 0:
                for word in words_list:
                    final_list.append(word)
            else:
                final_list.append(item)
    else:
        final_list = input_list
        return final_list

    final_list = [e for e in final_list if e]
    #count=len(final_list)
    #print(count)
    return final_list


# probabilities for a list
def pmf(input_list, size_of_hash):
    v = []
    for item in input_list:
        h = hashlib.blake2b(digest_size=size_of_hash)
        h.update(item.encode('utf-8'))
        v.append(h.hexdigest())

    C = Counter(v)
    total = float(sum(C.values()))
    for key in C:
        C[key] = Decimal(C[key] / total)
    return [k for k, v in C.items()], [v for k, v in C.items()]


# Entropy calculation for a list; returns value or None if list is empty
def calculate_entropy(input_list, further_tokenizing):
    done = False
    size_of_hash = 60

    if is_list_empty(input_list) is True:
        return None

    while not done:
        try:
            # Process the list, Calculate the probabilities, distribution and entropy
            input_list = prepare_to_process(input_list, further_tokenizing)
            count=(len(input_list)) #<- here should be final form of the list
            p_list = pmf(input_list, size_of_hash)
            d_list = dit.Distribution(p_list[0], p_list[1])
            entropy_list = dit.shannon.entropy(d_list)
            done = True
        except Exception as e:
            if str(e) != "Python int too large to convert to C long":
                # traceback.print_exc(file=sys.stdout)
                if str(e) == "`outcomes` must be nonempty if no sample space is given":
                    print("ERROR: " + str(e) + '\n\n')
                else:
                    print("ERROR: " + str(e) + '\n\n')
            # hashing on different sizes cuz of error.
            elif str(e) == "Python int too large to convert to C long":
                if size_of_hash is 60:
                    size_of_hash = 40
                    continue
                if size_of_hash is 40:
                    size_of_hash = 20
                    continue
                if size_of_hash is 20:
                    size_of_hash = 15
                    continue
                if size_of_hash is 15:
                    size_of_hash = 10
                    continue
                done = True
            None
    return entropy_list
directory='Entropy_Calculation'
MYDIR="C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\"

if not os.path.exists(MYDIR+directory):
    os.makedirs(MYDIR+directory)
def extract_all_tokens(function_call, list_of_filenames):
    #print(function_call)
    pathname="C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\"
    get_completefile=pathname+list_of_filenames+"_funcDef.json"
    if(os.path.isfile(get_completefile)):
        with open(get_completefile) as s:
            data1 = json.load(s)
            for search in data1:
                #print(get_completefile)
                if search["name"] ==function_call:
                    #print("function_call"+function_call)
                    #print("lol"+function_call)
                    #print("lol2"+function_call)
                    return (search["tokens"])
file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp")
#file_list=get_list_of_files("C:\\Users\\RITIN JAISWAL\\Desktop\\test_case_msc\\lol")
get_files=[]
c_files=[]
for s in file_list:
    #print(i)
    if s[-10:]=="paths.json":
       c_files.append(s)
for file in c_files:
    get=(os.path.basename(file).split('_'))
    get_files.append(get)

for file in c_files:
    initial_filename=(os.path.basename(file).split('_'))
    leaf_pathname="C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\"
    leaf_file=leaf_pathname+initial_filename[0]+"_"+initial_filename[1]+"_"+initial_filename[2]+"_nodes.json"
    path1 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"
    directory = (initial_filename[0])
    path = os.path.join(path1, directory)
    if not os.path.isdir(path):
        os.mkdir(path)
    
    with open(file) as path_list_file:
        path_list = json.load(path_list_file)
        joint_entropy_list=[]
        knowing_entropy_list=[]
        total=[]
        cond_entropy=[]
        print(file)
        final_solution=[]
        imp_path=[]
        not_imp=[]
        not_considered=[]
        imp_path1=[]
        not_imp1=[]
        not_considered1=[]
        for path in path_list:
            #print(path)
            
            for node in reversed(path[1:]):
#                 print(node)
# #                 print(path[:path.index(node)])
                
                joint_list = path[:path.index(node)+1]
                knowing_list = path[:path.index(node)]
            
                #print("joint" + str(joint_list))
                #print("knowing" +str(knowing_list))
                tokens_joint=[]
                for iterator in joint_list:
                    search_function=iterator.split(":")
                    #print(iterator)
                    #print(iterator.split(":")[1])
                    #search_function[0][:-2]+search_function[0][-1:]
                    tokens_joint1 = extract_all_tokens(iterator,(search_function[0][:-2]+search_function[0][-1:]))
                    tokens_joint.append(tokens_joint1)
                joint_entropy= calculate_entropy(tokens_joint, False)
                joint_entropy_list.append(joint_entropy)
                #print(joint_list)
                #print(joint_entropy)
                knowing_tokens=[]
                for iterator1 in knowing_list:
                    search_function1=iterator1.split(":")
                    #print(iterator1)
                    #print(iterator.split(":")[1])
                    #search_function[0][:-2]+search_function[0][-1:]
                    knowing_tokens1 = extract_all_tokens(iterator1,(search_function1[0][:-2]+search_function1[0][-1:]))
                    knowing_tokens.append(knowing_tokens1)
                knowing_entropy= calculate_entropy(knowing_tokens, False)
                knowing_entropy_list.append(knowing_entropy)
                total.append((joint_entropy_list,knowing_entropy_list))
                #to be deleted later for checking entropy difference:
                for i in range(len(joint_entropy_list)):
                    cond_entropy=joint_entropy_list[i]-knowing_entropy_list[i]
                final_solution.append((joint_list,cond_entropy))
                res = []
                [res.append(x) for x in final_solution if x not in res]
        for i in range(len(res)):
            if(res[i][1]>0):
                imp_path.append(res[i])
            elif(res[i][1]<0):
                not_imp.append(res[i])
            else:
                not_considered.append(res[i])
        for i in range(len(final_solution)):
            if(final_solution[i][1]>0):
                imp_path1.append(final_solution[i])
            elif(final_solution[i][1]<0):
                not_imp1.append(final_solution[i])
            else:
                not_considered1.append(final_solution[i])
                #to be deleted later
                #print(filename)
    filename1 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\entropy.json"
    filename2 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\conditional_entropy.json"
    filename3 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\conditional_entropy1.json"


    with open(filename1, 'w') as fp:
            json.dump(total, fp, ensure_ascii=False, indent=4)
    with open(filename2, 'w') as fp:
            json.dump(final_solution, fp, ensure_ascii=False, indent=4)
    with open(filename3, 'w') as fp:
            json.dump(res, fp, ensure_ascii=False, indent=4)
    filename4 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\imp_path1.json"
    filename5 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\not_imp1.json"
    filename6 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\not_considered1.json"

    with open(filename4, 'w') as fp:
            json.dump(imp_path, fp, ensure_ascii=False, indent=4)
    with open(filename5, 'w') as fp:
            json.dump(not_imp, fp, ensure_ascii=False, indent=4)
    with open(filename6, 'w') as fp:
            json.dump(not_considered, fp, ensure_ascii=False, indent=4)
    filename7 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\imp_path.json"
    filename8 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\not_imp.json"
    filename9 = "C:\\Users\\RITIN JAISWAL\\Desktop\\Finer-Softwares-master (1)\\Finer-Softwares-master\\Libjpeg\\Temp\\Entropy_Calculation\\"+str((((file.split("\\"))[8]).split("_"))[0])+"\\not_considered.json"

    with open(filename7, 'w') as fp:
            json.dump(imp_path1, fp, ensure_ascii=False, indent=4)
    with open(filename8, 'w') as fp:
            json.dump(not_imp1, fp, ensure_ascii=False, indent=4)
    with open(filename9, 'w') as fp:
            json.dump(not_considered1, fp, ensure_ascii=False, indent=4)
