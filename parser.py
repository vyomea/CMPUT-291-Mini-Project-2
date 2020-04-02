
import re
def keywordsParser(query):
    copyquery = query
    a,b,c = "","",""
    a1,a2=[],[]
    ptermflag,rtermflag = False,False
    stopwords = ['pterm','rterm','price','score','date']
    if ':' in query:
        query = ' '.join(query.split(':'))
    if '>' in query:
        query = ' '.join(query.split('>'))
    if '<' in query:
        query = ' '.join(query.split('<'))
    for i in stopwords:
        if i in query:
            query = ' '.join(query.split(i))

    querywords = query.split()
    resultwords  = [word for word in querywords if word.lower() not in stopwords]
    result = ' '.join(resultwords)
    result = result.split()
    new=[]
    output=[]
    for i in result:
        try:
            if i.isdigit() or float(i):
                continue
        except:
            pass
        new.append(i)
    for i in new:
        if len(i)>1:
            output.append(i)
    keypair = {}
    for i in output:
        keypair[i]=(False,False) #0 is for pterm 1 is for rterm
        a,b,c = copyquery.partition(i)
        reverse = a[::-1]
        x = reverse.find("mretp")
        y = reverse.find("mretr")
        if x == -1 and y== -1:
            keypair[i]=(False,False)
        if x>0 and y>0:
            if x<y:
                keypair[i]=(True,False)
            else:
                keypair[i]=(False,True)
        if x<0 and y>0:
            keypair[i]=(False,True)
        if x>0 and y<0:
            keypair[i]=(True,False)

    return keypair
print(keywordsParser("pterm: abcd% rterm : guitar sound% price < 400.3score>3"))
def termParser(query):
    a,b,c,x,y,z,p,q,r,l,m,n="","","","","","","","","","","",""
    modFlag,ptermFlag,rtermFlag = False,False,False
    if re.search(r"pterm",query):
        a,b,c = query.partition("pterm")
        ptermFlag = True
        c = str(c.split(":")[1])
        if "rterm" in c:
            templist = c.split("rterm")
            if templist[0] == "rterm":
                c = templist[1]
            else:
                c = templist[0]
        if "%" in c:
            c = str(c.split("%")[0])
        p,q,r = c.strip().partition(" ")
        c=c.strip().split(" ")[0]
    if re.search(r"rterm",query):
        x,y,z = query.partition("rterm")  
        rtermFlag=True
        z = str(z.split(":")[1])
        if "pterm" in z:
            templist = z.split("pterm")
            if templist[0] == "pterm":
                z = templist[1]
            else:
                z = templist[0]
        if "%" in z:
            z = str(z.split("%")[0])
        l,m,n = z.strip().partition(" ")
        z = z.strip().split(" ")[0]

    if re.search(r"%",query):
        modFlag = True
    if ptermFlag or modFlag or rtermFlag:
        return (modFlag,ptermFlag,c.strip(),rtermFlag,z.strip(),r.strip(),n.strip())  
    else:
        return False

print(termParser("rterm: great sound pterm: guitar"))

def scoreparser(query):
    low1,high1,low2,high2 = False,False,False,False
    condition1,condition2 = "",""
    high,low = 0,0
    digit1,digit2=0,0
    if re.search(r"score",query):
        a,b,c = query.partition("score")
        if "score" in c:
            x,y,z = c.partition("score")
            condition2 = z.strip()[0]
            if condition2 == ">":
                high2 = True
            if condition2 == "<":
                low2 = True
            if low2 == False and high2 == False:
                return False  
            try:
                digit2 = int(re.search(r'{}\s*(\d+)'.format(condition2),z).group(1))
            except ValueError:
                print("Wrong digit")
                return False
        condition1= c.strip()[0]
        if condition1== ">":
            high1 = True
        if condition1 == "<":
            low1 = True
        if low1 == False and high1 == False:
            return False  
        try:
           digit1 = int(re.search(r'{}\s*(\d+)'.format(condition1),c).group(1))
        except ValueError:
            print("Wrong digit")
            return False 
        if high2 == False and low2 == False:
            if condition1 == ">":
                low = digit1
                high = None
            if condition1 == "<":
                high = digit1
                low = None
            return (low,high)
        if high2:
            low = digit2
        else:
            low = digit1
        if low2:
            high = digit2
        else:
            high = digit1
        return (low,high)  
    else:
        return False
    

def priceparser(query):
    low1,high1,low2,high2 = False,False,False,False
    low,high = 0,0
    condition1,condition2 = "",""
    digit1,digit2=0,0
    if re.search(r"price",query):
        a,b,c = query.partition("price")
        if "price" in c:
            x,y,z = c.partition("price")
            condition2 = z.strip()[0]
            if condition2 == ">":
                high2 = True
            if condition2 == "<":
                low2 = True
            if low2 == False and high2 == False:
                return False  
            try:
                digit2 = int(re.search(r'{}\s*(\d+)'.format(condition2),z).group(1))
            except ValueError:
                print("Wrong digit")
                return False
        condition1= c.strip()[0]
        if condition1== ">":
            high1 = True
        if condition1 == "<":
            low1 = True
        if low1 == False and high1 == False:
            return False  
        try:
            digit1 = int(re.search(r'{}\s*(\d+)'.format(condition1),c).group(1))
        except ValueError:
            print("Wrong digit")
            return False 
        if high2 == False and low2 == False:
            if condition1 == ">":
                low = digit1
                high = None
            if condition1 == "<":
                high = digit1
                low = None
            return (low,high)
        if high2:
            low = digit2
        else:
            low = digit1
        if low2:
            high = digit2
        else:
            high = digit1
        return (low,high) 
    else:
        return False

def dateparser(query):
    low1,low2,high1,high2=False,False,False,False
    low,high = "",""
    condition1,condition2 = "",""
    date1,date2="",""
    if re.search(r"date",query):
        a,b,c = query.partition("date")
        if "date" in c:
            x,y,z = c.partition("date")
            condition2 = z.strip()[0]
            if condition2 == ">":
                high2 = True
            if condition2 == "<":
                low2 = True
            if low2 == False and high2 == False:
                return False 
            date2 = re.search(r'(\d+/\d+/\d+)',z).group(1)
        condition1 = c.strip()[0]
        if condition1 == ">":
            high1 = True
        if condition1 == "<":
            low1 = True
        if low1 == False and high1 == False:
            return False
        date1 = re.search(r'(\d+/\d+/\d+)',c).group(1)
        if high2:
            low = date2
        else:
            low = date1
        if low2:
            high = date2
        else:
            high = date1
        return (low,high) 
    return False
            
