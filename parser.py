
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
        if " " in c.strip():
            f = c.split(" ")
            b = c.split(" ")[2]
            c = c.split(" ")[1]
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
        if " " in z.strip():
            y = z.split(" ")[2]
            z = z.split(" ")[1]

    if re.search(r"%",query):
        modFlag = True
    if ptermFlag or modFlag or rtermFlag:
        return (modFlag,ptermFlag,c.strip(),rtermFlag,z.strip(),b.strip(),y.strip())  #b.strip is pterm second word, y.strip is rterm second word
    else:
        return False

print(termParser("rterm: great sound%"))

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
    
print(scoreparser("score < 40"))
"""query = "rterm: guitar score > 6"
print(termParser(query))
print(scoreparser(query))"""

def priceparser(query):
    low1,high1,low2,high2 = False,False,False,False
    low,high = 0,0
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

print(priceparser("price>40 price <30"))
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
            
print(dateparser("date>4000/31/31date<9000/31/12"))
