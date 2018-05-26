import subprocess
import sys
import os
import os.path
import mpmath
import sys
import pickle
sys.modules['sympy.mpmath'] = mpmath
from sympy.combinatorics.prufer import Prufer
from PIL import Image

prefixCode = {}
listOfEdges = []
i = 0
listValue = []
listOfLetters = {}

def draw_tree(tree, val, prefix = ''):
    global i
    global listValue
    i += 1
    
    if isinstance(tree, str):    
        descr = '%s [label="%s\n%s", fontcolor=black, fontsize=14];\n'%(i-1, i-1, tree)
        listOfLetters[i-1] = tree
        prefixCode[prefix] = i-1
        listValue.append(tree)	
    else:
        descr = '%s [label="%s"];\n'%(i-1, i-1)
        prefixCode[prefix] = i-1
        for child in tree.keys(): 
            descr += draw_tree(tree[child], i-1, prefix = prefix+child)
            descr += '%s -> %s;\n'%(prefixCode[prefix],prefixCode[prefix+child])
            listOfEdges.append([prefixCode[prefix],prefixCode[prefix+child]])
    
    
    return descr
  
def assign_code(nodes, label, result, prefix = ''):    
    childs = nodes[label]     
    tree = {}
    if len(childs) == 2:
        tree['0'] = assign_code(nodes, childs[0], result, prefix)
        tree['1'] = assign_code(nodes, childs[1], result, prefix)     
        return tree
    else:
        result[label] = prefix
        return label

def Huffman_code(_vals):    
    vals = _vals.copy()
    nodes = {}
    for n in vals.keys():
        nodes[n] = []

    while len(vals) > 1:
        s_vals = sorted(vals.items(), key=lambda x:x[1]) 
        a1 = s_vals[0][0]
        a2 = s_vals[1][0]
        vals[a1+a2] = vals.pop(a1) + vals.pop(a2)
        nodes[a1+a2] = [a1, a2]        
    code = {}
    root = a1+a2
    tree = {}
    tree = assign_code(nodes, root, code) 
    return code, tree

def menu(modeOption):
    if modeOption == "1":
        while True:
            fileWithInputDataForMode1 = input("Podaj scieżkę do pliku z tekstem wejsciowym: ") 
            if os.path.exists(fileWithInputDataForMode1):   
                file_object  = open(fileWithInputDataForMode1, "r")
                print("\n# =====================================================")
                print("#            Wybrałeś plik: " +os.path.basename(fileWithInputDataForMode1))
                print("# =====================================================\n")
                break
            else:
                print ("Plik "+ os.path.basename(fileWithInputDataForMode1)+" nie istnieje, podaj inną scieżkę!")
                continue
        readFromFile = file_object.read()
        codes = {}
        for z in readFromFile:
            if z == "\n":
                z = " "
            if( z in codes):
                codes[z] += 1
            else:
                codes[z] = 1

        code, tree = Huffman_code(codes)

        nameOfGraphFileForMode1 = input("Podaj sciezke w której ma powstać graf(no extension): ")
        print("\n# =====================================================")
        print("#        Graf powstał w pliku: " +os.path.basename(nameOfGraphFileForMode1) + ".jpeg")
        print("# =====================================================\n")        
        with open(nameOfGraphFileForMode1 + ".dot",'w') as f:
            f.write('digraph G {\n')
            f.write(draw_tree(tree, 0))
            f.write('}')   
        subprocess.call('dot -Tjpeg '+nameOfGraphFileForMode1+'.dot -o '+nameOfGraphFileForMode1+'.jpeg', shell=True)

        a = Prufer.to_prufer(listOfEdges,len(listOfEdges)+1)

        fileWithOutputDataForMode1 = input("Podaj sciezke do pliku wyjściowego: ")
        print("\n# =====================================================")
        print("#        Powstały plik wyjściowy to: " +os.path.basename(fileWithOutputDataForMode1))
        print("# =====================================================\n") 
        outputFileForMode1 = open(fileWithOutputDataForMode1, "w")
        firstLine = "0"
        secondLine = ""
        thirdLine = ""
        for x in a:
            secondLine = secondLine + str(x) + " "
        for c in listValue:  
            thirdLine = thirdLine + str(c) + " "
        lines = [firstLine,"\n",secondLine,"\n",thirdLine]    
        outputFileForMode1.writelines(lines)
        outputFileForMode1.close()
        
        with open("tempFile.txt",'wb') as tF:
            pickle.dump(listOfLetters, tF)
        
        f = Image.open(nameOfGraphFileForMode1+".jpeg").show()
        os.system(fileWithOutputDataForMode1) 
        
    elif modeOption == "2":

        while True:
            fileWithInputDataMode2 = input("Podaj ścieżkę do pliku zawierającego kod Prufera: ") 
            if os.path.exists(fileWithInputDataMode2):   
                file_object  = open(fileWithInputDataMode2, "r")
                print("\n# =====================================================")
                print("#            Wybrałeś plik: " +os.path.basename(fileWithInputDataMode2))
                print("# =====================================================\n")
                break
            else:
                print ("Plik "+ os.path.basename(fileWithInputDataMode2)+" nie istnieje, podaj inną scieżkę!")
                continue
                
        pruferVert = []
        
        for a, b in enumerate(file_object):
            if a == 1:
                c = b.split(" ")
                for d in c:
                    pruferVert.append(d)
            elif a > 1:
                break
                
        for x in pruferVert:
            if x == " " or x == '\n':
                pruferVert.remove(x)
                
        while True:
            try:
                Prufer_list = [int(i) for i in pruferVert]
                break
            except ValueError:
                print ("Oops! Zły format pliku wejściowego "+ os.path.basename(fileWithInputDataMode2)+". Zamykanie programu...")
                sys.exit()
                
        pruferTree = Prufer.to_tree(Prufer_list)

        if os.path.exists('tempFile.txt'):   
            with open ('tempFile.txt', 'rb') as fp:
                itemlist = pickle.load(fp)
        else:
            itemlist={}
        
        newStr = "digraph G {\n"
        for x in pruferTree:
            if itemlist.get(x[0]):
                newStr +='%s [label="%s\n%s", fontcolor=black, fontsize=14];\n'%(str(x[0]), str(x[0]), itemlist.get(x[0]))
            elif itemlist.get(x[1]):
                newStr +='%s [label="%s\n%s", fontcolor=black, fontsize=14];\n'%(str(x[1]), str(x[1]), itemlist.get(x[1]))
            newStr += str(x[0]) + " -> "
            newStr += str(x[1]) + "\n"
        newStr+="}"
        
        nameOfGraphFileMode2= input("Podaj sciezke gdzie ma powstac graf(no extension): ") 
        print("\n# =====================================================")
        print("#        Graf powstał w pliku: " +os.path.basename(nameOfGraphFileMode2) + ".jpeg")
        print("# =====================================================\n")          
        with open(nameOfGraphFileMode2 + ".dot",'w') as f:
            f.write(newStr)   
            
        subprocess.call('dot -Tjpeg '+nameOfGraphFileMode2+'.dot -o '+nameOfGraphFileMode2+'.jpeg', shell=True)
        f = Image.open(nameOfGraphFileMode2+".jpeg").show()

    elif modeOption == '3':
        os.system('cls')
        sys.exit()
        
    else:
        print("\n# =====================================================")
        print("#                        BŁĄD")
        print("#            PODAJ POPRAWNĄ WARTOŚĆ Z MENU")
        print("# =====================================================\n")
        print("1. Kodowanie na podstawie gotowego pliku tekstowego ")
        print("2. Dekodowanie na podstawie pliku z kodem Prufera")
        print("3. Zamknij program\n")
        print("# =====================================================\n")
        newVal = input(">> ")
        menu(newVal)
    
os.system('cls')    
print("\n# =====================================================")
print("#           WITAJ W PROGRAMIE DO KODOWANIA")
print("# =====================================================\n")

print("1. Kodowanie na podstawie gotowego pliku tekstowego ")
print("2. Dekodowanie na podstawie pliku z kodem Prufera")
print("3. Zamknij program\n")
print("# =====================================================\n")

modeOption = input(">> ")
    
menu(modeOption)