import enchant,os,random

d=enchant.Dict("en_UK")
#the thing you want to decode
#pygame part
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
#constants
mod26_inverses = {
    1: 1,
    3: 9,
    5: 21,
    7: 15,
    9: 3,
    11: 19,
    15: 7,
    17: 23,
    19: 11,
    21: 5,
    23: 17,
    25: 25
}
#functions
def bubblesortint(list):
    adr=0
    while adr<len(list)-1:
        if list[adr]>list[adr+1]:
            list[adr],list[adr+1]=list[adr+1],list[adr]
            adr-=1
        else: adr+=1
        if adr<0: adr+=1      
    return list
def bubblesort(list):
    adr=0
    while adr<len(list)-1:
        if list[adr][1]>list[adr+1][1]:
            list[adr],list[adr+1]=list[adr+1],list[adr]
            adr-=1
        else: adr+=1
        if adr<0: adr+=1      
    return list
def isWord(str):
    return d.check(str)
def countwords(str):
    list=str.split(' ')
    hits=0
    for i in list:
        if len(i)>0:
            if isWord(i):
                hits+=1
    return(hits)
def linearsearch(i,l):
    for j in range(len(l)):
        if l[j]==i: return j
    else:
        return -1
"""def render(list,colour):
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    width=SCREEN_WIDTH/len(list)
    heightratio=SCREEN_HEIGHT/max(list)
    for i in range(len(list)):
        pygame.draw.rect(screen,colour,pygame.Rect(width*i,SCREEN_HEIGHT-heightratio*list[i], width ,heightratio*list[i]))"""
def caesarshift(W,k):
    alphabet=[chr(97+i) for i in range(26)]
    out=''
    for l in W:
        if not l.lower() in alphabet:
            out+=l
        else:
            n=linearsearch(l.lower(),alphabet)
            n+=k
            n=n%26
            out=out+alphabet[n]
    return(out)
def max(list):
    maxval=0
    index=0
    for i in range(len(list)):
        if list[i]>maxval:
            maxval=list[i]
            index=i
    return index
def affineshift(str,a,b):
    alphabet=[chr(97+i) for i in range(26)]
    out=''
    for l in str:
        if not l.lower() in alphabet:
            out+=l
        else:
            n=linearsearch(l.lower(),alphabet)
            n=n*a
            n+=b
            n=n%26
            out=out+alphabet[n]
    return(out)    
#the main body
def caesardecode(str):
    list=[]
    for i in range(26):
        hits=countwords(caesarshift(str,-i))
        list.append(hits)
    if len(str.split(' '))/list[max(list)]>0.5:
        return caesarshift(str,-max(list))
    else:
        return str
def affinedecode(str):
    list=[]
    for i in range(26):
        for j in range(26):
            hits=countwords(affineshift(str,i,j))
            list.append(hits)
        print(f'{i} complete')
    maxi=max(list)
    if len(str.split(' '))/list[maxi]>0.5:
        a=maxi//26
        b=maxi%26  
        print(mod26_inverses[a],(mod26_inverses[a]*-b)%26)
        return affineshift(str,a,b)
    else:
        return str
def friendlydecode(str):
    list=[]
    for i in range(26):
        hits=countwords(caesarshift(str,-i))
        list.append(hits)
    print(f'message decoded is \n{caesarshift(str,-max(list))}')
    print(f'{list[max(list)]} hits')
    print(f'key is {max(list)}')
    
def caesardecodefile(file):
    with open(file,'r') as txt:
        txt=txt.read()
        l=caesardecode(txt)
    with open(file,'w') as f:
        f.write(l)

def caesarshiftfile(file,key):
    with open(file,'r') as f:
        text=caesarshift(f.read(),key)
    with open(file,'w') as f:
        f.write(text)

def frequencyanalysis(txt):
    alphabet=[chr(97+i) for i in range(26)]
    freq=[0 for i in range(26)]
    for i in txt:
        ind=linearsearch(i.lower(),alphabet)
        if ind>=0:
            freq[ind]=freq[ind]+1
    for i in range(26):
        freq[i]=(alphabet[i],freq[i])
    freq=bubblesort(freq)
    return freq
def randomalphabet():
    Lone=[chr(122-i) for i in range(26)]
    Ltwo=[chr(122-i) for i in range(26)]
    random.shuffle(Ltwo)
    return [(Lone[i],Ltwo[i]) for i in range(26)]
def substitute(text,alphabet,reverse=False):
    outtext=''
    ab=[chr(i+97) for i in range(26)]
    if reverse:
        for i in text:
            if i.lower()  in ab:
                for j in range(26):
                    if alphabet[j][1]==i:
                        outtext+=alphabet[j][0]
                        break
            else:outtext+=i          
    else:
        for i in text:
            if i.lower in ab:
                for j in range(26):
                    if alphabet[j][0]==i:
                        outtext+=alphabet[j][1]
            else:outtext+=i
    return(outtext)
def freqaffinesolve(txt):
    freqs=frequencyanalysis(txt)
    first=freqs[25][0]
    first=ord(first)-97
    second=freqs[24][0]
    second=ord(second)-97
    for i in [['e','t'],['e','a']]:
        options=[]
        for a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            for b in range(26):
                if (((ord(i[0])-1)*a)+b)%26==first:
                    options.append((a,b))
        print(options)
        for n in range(len(options)):
            if (((ord(i[1])-1)*options[n][0])+options[n][1])%26!=second:
                options.pop(n)
        print(options)

    

text = ""
print(frequencyanalysis(text))
