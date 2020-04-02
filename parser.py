
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
    low, high = False,False
    if re.search(r"score",query):
        condition = query.split("score")[1].strip()[0]
        if condition == ">":
            high = True
        if condition == "<":
            low == True
        if low == False and high == False:
            return False
        try:
            digit = int(query.split(condition)[1].strip()[0])
        except ValueError:
            print("Invalid digit")
            return False
        return (low,high,digit)
    return False

query = "rterm: guitar score > 6"
print(termParser(query))
print(scoreparser(query))
