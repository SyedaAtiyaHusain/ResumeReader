"""
Title:Resume Reader
Developed  by : Syeda Atiya Husain and Ashish Kore
Language: Python
Requirement:
            Python version: Python 3 or later
            Libraries:1) Pandas
                      2) re
            Additional files: Resume Headings & Subheadings.xlsx
"""

import pandas as pd                                   #importing necessary libraries                                                    
import re

def reader(x):
    """This function is defined so as to convert a parsed resume into a key value pair format (dictionary).
    The headings in the resume becomes keys in dicionary and their content becomes value in the same.
    It takes parsed resume as an argument."""
    
    df = pd.read_excel('Resume Headings & Subheadings.xlsx')        #load the heading dataset
    headings=df['headings']
    headings=headings.dropna()
                                                                   #this part of code fetches all the headings from the resume which 
                                                                   #have new line (\n) after them.
    resume=x.split("\n")
    resume_len=len(resume)
    for i in range(resume_len):
        resume[i]=resume[i]+"\n"
    copy_headings=[]
    for i in headings:
        copy_headings.append(i)
    keys=[]
    dic={}
    value=""                                 
    for i in range(resume_len):
        for j in headings:
            to=re.findall(r'[A-Za-z0-9-:()&.@/, \t |]+[A-Za-z0-9-:()&.@/,\t |]',resume[i])
            if len(to)!=0:
                if j == to[0].lower():
                    keys.append([to[0],i,"a"])
    key_len=len(keys)
                    
    def func1():
        
        """This part of code fetches all the headings from the resume which 
            have tab space (\t) after them """
 
        count=-1
        head,list=[],[]
        for i in resume:
            count+=1
            if "\t" in i:
                r=re.findall(r'[\w\s]*?[\w]+\t',i)
                if len(r)!=0:
                    r[0]=r[0].replace('\t','')
                    if r[0].lower() in copy_headings:
                        if ([r[0],count,'a'] not in keys) or ([r[0],count,'m'] not in keys):
                            keys.append([r[0],count,"m"])
                            
    func1()                                                                 
    
    def func2():
        
            """This part of code fetches all the headings from the resume which 
            have colon (:) or hyphen(-) after them """
            
        list,head=[],[]
        count=-1
        for i in resume:
            count+=1
            if ":" in i or "\t" in i or "-" in i:
                r=re.findall(r'[\w\s\t\n]?[\w\s]+[:\t-\n\s]+?',i)
                if len(r)!=0:
                    for j in range(len(r)):
                        r[j]=r[j].replace(':','')
                        r[j]=r[j].replace('\t','')
                        r[j]=r[j].replace('-','')
                        if r[j].lower() in copy_headings:
                            if ([r[0],count,'a'] not in keys) and ([r[0],count,'m'] not in keys):
                                keys.append([r[0],count,"m"])

    func2()
    
                                                  #This part of code merges all the headings obtained from the above three sections.  
    x=[]
    for i in keys:
        x.append(i[1])
    x.sort()
    final_head=[]
    for i in range(len(x)):
        for j in range(len(x)):
            if x[i] == keys[j][1]:
                final_head.append(keys[j])
    keys=final_head
                                                  #This part of code determines the contents which lies under heading in the resume.
                                                  #Also it forms the dictionary having heading as keys and content as their values.  
    dic={}
    resume_len=len(resume)
    key_len=len(keys)
    for key in range(len(keys)-1):
        if keys[key][2]=='a':
            for i in range(keys[key][1]+1,keys[key+1][1]):
                value+=resume[i]
            dic[keys[key][0]]=value
            value=""
        elif keys[key][2]=='m':
            value=""
            resume_len=len(resume)
            for i in range(keys[key][1],keys[key+1][1]):
                if i==keys[key][1]:
                    value+=resume[i].replace(keys[key][0],"")
                else:
                    value+=resume[i]
            dic[keys[key][0]]=value
            value=""
    if keys[-1][2]=='a':
        for i in range(keys[key_len-1][1]+1,resume_len):
            value+=resume[i]
        dic[keys[key_len-1][0]]=value
    elif keys[-1][2]=='m':
        for i in range(keys[key_len-1][1],resume_len):
            value+=resume[i].replace(keys[key_len-1][0],"")
        dic[keys[key_len-1][0]]=value
    temp=resume[:keys[0][1]]
    about_cont=[]
    for i in temp:
        if i not in ['\n',' \n','\n ',' \n ']:
            about_cont.append(i)
    dic["about"]=''.join(about_cont)
    
    return dic                                         #It returns final dictionary with headings as keys and content as values.
