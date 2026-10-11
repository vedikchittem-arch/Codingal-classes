import enchant
print(enchant.list_languages())
d = enchant.Dict("en_GB")
text=input('enter the code to decode\n>')
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
def caesarshift(W,k):
    alphabet=[chr(97+i) for i in range(26)]
    out=''
    for l in W:
        if not l.lower() in alphabet:
            out+=l
        else:
            n=ord(l)-97
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
def caesardecode(str):
    list=[]
    for i in range(26):
        hits=countwords(caesarshift(str,-i))
        list.append(hits)
    if len(str.split(' '))/list[max(list)]>0.5:
        return caesarshift(str,-max(list))
    else:
        return str

print(caesardecode(text))