
import re
def termParser(query):
    a,b,c,x,y,z="","","","","",""
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
    if re.search(r"%",query):
        modFlag = True
    if ptermFlag or modFlag or rtermFlag:
        return (modFlag,ptermFlag,c.strip(),rtermFlag,z.strip())
    else:
        return False

def scoreparser(query):
    low1,high1,low2,high2 = False,False,False,False
    condition1,condition2 = "",""
    digit1,digit2=0,0
    if re.search(r"score",query):
        a,b,c = query.partition("score")
        if "score" in c:
            print(c)
            x,y,z = c.partition("score")
            condition2 = z.strip()[0]
            if condition2 == ">":
                high2 = True
            if condition2 == "<":
                low2 = True
            if low2 == False and high2 == False:
                return False  
            try:
                print(z.split(condition2)[1].strip())
                digit2 = int(z.split(condition2)[1].strip())
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
            digit1 = int(c.split(condition1)[1].strip().split("score")[0].strip())
        except ValueError:
            print("Wrong digit")
            return False 
        return (low1,high1,digit1,low2,high2,digit2) 
    else:
        return False
    

"""query = "rterm: guitar score > 6"
print(termParser(query))
print(scoreparser(query))"""

def priceparser(query):
    low1,high1,low2,high2 = False,False,False,False
    condition1,condition2 = "",""
    digit1,digit2=0,0
    if re.search(r"price",query):
        a,b,c = query.partition("price")
        if "price" in c:
            print(c)
            x,y,z = c.partition("price")
            condition2 = z.strip()[0]
            if condition2 == ">":
                high2 = True
            if condition2 == "<":
                low2 = True
            if low2 == False and high2 == False:
                return False  
            try:
                print(z.split(condition2)[1].strip())
                digit2 = int(z.split(condition2)[1].strip())
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
            digit1 = int(c.split(condition1)[1].strip().split("price")[0].strip())
        except ValueError:
            print("Wrong digit")
            return False 
        return (low1,high1,digit1,low2,high2,digit2) 
    else:
        return False
    
print(priceparser("price>400 price<500"))
print(scoreparser("score>400 score>4054"))
