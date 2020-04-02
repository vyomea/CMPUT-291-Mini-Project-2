#!/usr/bin/python
# -*- coding: utf-8 -*-

import re


def keywordsParser(query):
    """
    Parser to separate the terms from the query.
    Method: Works using distance between words to classify
    words as terms and keywords. 
    Further classfies each term into an rterm or pterm boolean.
    Output: A dictionary of terms with their respective flags.
    """

    copyquery = query
    (a, b, c) = ('', '', '')
    stopwords = ['pterm', 'rterm', r"price", r"score", r"date"]
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
    resultwords = [word for word in querywords if word.lower()
                   not in stopwords]
    result = ' '.join(resultwords)
    result = result.split()
    new = []
    output = []

    for i in result:
        try:
            if i.isdigit() or float(i):
                continue
        except:
            pass
        new.append(i)
    for i in new:
        if len(i) > 1:
            output.append(i)
    keypair = {}
    for i in output:
        keypair[i] = (False, False)  # 0th index is for pterm 1st index is for rterm
        (a, b, c) = copyquery.partition(i)
        reverse = a[::-1]
        x = reverse.find('mretp')
        y = reverse.find('mretr')
        z = -1
        minz = float('inf')
        a = []
        for j in keypair.keys():
            a.append(reverse.find(j[::-1]))
        for k in a:
            if k > 0 and k < minz:
                minz = k
        if x != -1 and x < minz:
            keypair[i] = (True, False)
        if y != -1 and y < minz:
            keypair[i] = (False, True)
        else:
            keypair[i] == (False, False)
        if z == -1:
            continue
        if x == -1 and y == -1:
            keypair[i] = (False, False)
        if x > 0 and y > 0:
            if x < y:
                keypair[i] = (True, False)
            else:
                keypair[i] = (False, True)
        if x < 0 and y > 0:
            keypair[i] = (False, True)
        if x > 0 and y < 0:
            keypair[i] = (True, False)
    return keypair

def scoreparser(query):
    """
    Parser to separate the scores from the query.
    Method: Uses re to find patterns and partitions
    to ensure the handling of multiple score words.
    Output: A tuple (low,high) denoting the interval.
    """

    (low1, high1, low2, high2) = (False, False, False, False)
    (condition1, condition2) = ('', '')
    (high, low) = (0, 0)
    (digit1, digit2) = (0, 0)
    if re.search(r"score", query):
        (a, b, c) = query.partition(r"score")
        if r"score" in c:
            (x, y, z) = c.partition(r"score")
            condition2 = z.strip()[0]
            if condition2 == '>':
                high2 = True
            if condition2 == '<':
                low2 = True
            if low2 == False and high2 == False:
                return False
            try:
                if '.' in z:
                    digit2 = \
                        float(re.search(r'{}\s*(\d+.\d+)'.format(condition2),
                              z).group(1))
                else:
                    digit2 = \
                        int(re.search(r'{}\s*(\d+)'.format(condition2),
                            z).group(1))
            except ValueError:
                print ('Wrong digit')
                return False
        condition1 = c.strip()[0]
        if condition1 == '>':
            high1 = True
        if condition1 == '<':
            low1 = True
        if low1 == False and high1 == False:
            return False
        try:
            if '.' in c:
                digit1 = \
                    float(re.search(r'{}\s*(\d+.\d+)'.format(condition1),
                          c).group(1))
            else:
                digit1 = \
                    int(re.search(r'{}\s*(\d+)'.format(condition1),
                        c).group(1))
        except ValueError:
            print ('Wrong digit')
            return False
        if high2 == False and low2 == False:
            if condition1 == '>':
                low = digit1
                high = None
            if condition1 == '<':
                high = digit1
                low = None
            return (low, high)
        if high2:
            low = digit2
        else:
            low = digit1
        if low2:
            high = digit2
        else:
            high = digit1
        return (low, high)
    else:
        return False

def priceparser(query):
    """
    Parser to separate the price from the query.
    Method: Uses re to find patterns and partitions
    to ensure the handling of multiple score words.
    Output: A tuple (low,high) denoting the interval.
    """

    (low1, high1, low2, high2) = (False, False, False, False)
    (low, high) = (0, 0)
    (condition1, condition2) = ('', '')
    (digit1, digit2) = (0, 0)
    if re.search(r"price", query):
        (a, b, c) = query.partition(r"price")
        if r"price" in c:
            (x, y, z) = c.partition(r"price")
            condition2 = z.strip()[0]
            if condition2 == '>':
                high2 = True
            if condition2 == '<':
                low2 = True
            if low2 == False and high2 == False:
                return False
            try:
                if '.' in z:
                    digit2 = \
                        float(re.search(r'{}\s*(\d+.\d+)'.format(condition2),
                              z).group(1))
                else:
                    digit2 = \
                        int(re.search(r'{}\s*(\d+)'.format(condition2),
                            z).group(1))
            except ValueError:
                print ('Wrong digit')
                return False
        condition1 = c.strip()[0]
        if condition1 == '>':
            high1 = True
        if condition1 == '<':
            low1 = True
        if low1 == False and high1 == False:
            return False
        try:
            if '.' in c:
                digit1 = \
                    float(re.search(r'{}\s*(\d+.\d+)'.format(condition1),
                          c).group(1))
            else:
                digit1 = \
                    int(re.search(r'{}\s*(\d+)'.format(condition1),
                        c).group(1))
        except ValueError:
            print ('Wrong digit')
            return False
        if high2 == False and low2 == False:
            if condition1 == '>':
                low = digit1
                high = None
            if condition1 == '<':
                high = digit1
                low = None
            return (low, high)
        if high2:
            low = digit2
        else:
            low = digit1
        if low2:
            high = digit2
        else:
            high = digit1
        return (low, high)
    else:
        return False

def dateparser(query):
    """
    Parser to separate the date from the query.
    Method: Uses partition to separate the date, and
    searches for a pattern of inequality signs.
    Output: A tuple bound (low,high) for the range 
    of dates. 
    """

    (low1, low2, high1, high2) = (False, False, False, False)
    (low, high) = ('', '')
    (condition1, condition2) = ('', '')
    (date1, date2) = ('', '')
    if re.search(r"date", query):
        (a, b, c) = query.partition(r"date")
        if r"date" in c:
            (x, y, z) = c.partition(r"date")
            condition2 = z.strip()[0]
            if condition2 == '>':
                high2 = True
            if condition2 == '<':
                low2 = True
            if low2 == False and high2 == False:
                return False
            date2 = re.search(r'(\d+/\d+/\d+)', z).group(1)
        condition1 = c.strip()[0]
        if condition1 == '>':
            high1 = True
        if condition1 == '<':
            low1 = True
        if low1 == False and high1 == False:
            return False
        date1 = re.search(r'(\d+/\d+/\d+)', c).group(1)
        if high2:
            low = date2
        else:
            low = date1
        if low2:
            high = date2
        else:
            high = date1
        return (low, high)
    return False
