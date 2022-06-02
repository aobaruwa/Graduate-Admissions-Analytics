from bs4 import BeautifulSoup
from glob import glob
import pandas as pd
from tqdm import tqdm
import bs4
import csv
import os
import re

### regex commands: https://github.com/dnc1994/Grad-Cafe-Data-Analysis/blob/master/gradcafe.ipynb
re_decision = re.compile('((?:Accepted)|(?:Rejected)|(?:Interview)|(?:Wait listed)|(?:Other)) on ')
re_degree = re.compile('((?:PhD)|(?:Masters)|(?:MFA)|(?:MBA)|(?:JD)|(?:EdD)|(?:Other))')
re_gpa = re.compile('GPA ((?:[0-9]\.[0-9]{1,2})|(?:n/a))')

def contains_alpha(string):
    return any(list(filter(lambda x: str(x).isalpha(), string)))

def extract_major_and_school(strs):
    major_and_school = strs[0]
    try:
        major, school = major_and_school.split(',', maxsplit=1)
        return major.strip(), school.strip()
    except Exception as e:
        return None, None

def extract_degree(strs):
    re_degree = re.compile('((?:PhD)|(?:Masters)|(?:MFA)|(?:MBA)|(?:JD)|(?:EdD)|(?:Other))')
    for string in strs:
        degree = re_degree.search(string)
        if degree: 
            return degree.groups()[0].strip()

def extract_season(strs):
    season_literals = ["Fall", "Winter", "Spring"]
    for string in strs:
        if len(string.split())==2:
            for literal in season_literals:
                if string.startswith(literal):
                    return string.strip()

def extract_decision(strs):
    re_decision = re.compile(('((?:Accepted)|(?:Rejected)|(?:Interview)|(?:Wait listed)|(?:Other))'))  
    for string in strs:
        decision = re_decision.search(string)
        if decision:
            return decision.groups()[0].strip()

def extract_gpa(strs):
    re_gpa = re.compile('GPA ((?:[0-9]\.[0-9]{1,2})|(?:n/a))')
    for string in strs:
        gpa = re_gpa.search(string)
        if gpa:
            return float(gpa.groups()[0].strip())

def extract_gre(strs):  
    def _match(score): 
        if "AW" in score: # analytical_writing
            val = float(score.split()[-1])
            return "GRE_AW", val
        elif "V" in score: # verbal
            val = float(score.split()[-1])
            return "GRE_V", val
        else:  # Quant 
            val = float(score.split()[-1])
            return "GRE_Quant", val

    gre_score_details = {"GRE_AW":None, "GRE_V":None, "GRE_Quant":None}
    for string in strs:
        
        if string.startswith("GRE"):
            try:
                key, val = _match(string)
                gre_score_details[key] = val   
            except Exception as e:
                print(e, string)
                continue
    return gre_score_details

def extract_status(strs):
    status_types = ["American", "International", "Other"]
    for string in strs:
        if string in status_types:
            return string

def match_all(strings):
    """
    fields = {'school':None, 'major':None, 'degree':None, 
    'season':None, 'decision':None, 'gpa':None, 'status': None,
    "GRE_AW":None, "GRE_V":None, "GRE_Quant":None}
    """
    fields = {}
    major, school  = extract_major_and_school(strings)
    degree = extract_degree(strings) 
    season = extract_season(strings)
    decision = extract_decision(strings)
    gpa = extract_gpa(strings)
    gre_score = extract_gre(strings)
    status = extract_status(strings)
    
    fields['school']=school
    fields['major'] = major
    fields['degree'] = degree 
    fields['season'] = season
    fields['decision'] = decision
    fields['gpa'] = gpa
    fields['status'] = status
    
    for k, val in gre_score.items():
        fields[k] = val
    return fields

def recursive_gen(doc):
    keys = ['h6', 'span', 'p', 'i']
    collect = []
    for key in keys:
        for y in doc.find_all(key):
            if y:
                #print("y", y, type(y)) #x if isinstance(x, bs4.element.Tag') else 
                children = [x.text if isinstance(x, bs4.element.Tag) else x for x in y.descendants ]
                #print("ch",children)
                for ch in children:
                    ch = " ".join(word for word in ch.strip().split())
                    if ch and ch not in collect:#[key]: 
                        collect.append(ch)
    if not collect: 
        return None, None
    
    field_dict = match_all(collect)
    #print(field_dict)
    return collect, field_dict

def extract_fields(html_file):
    html_doc = open(html_file, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    all_entries = soup.find_all('div', 'col')
    output = []
    for i, entry in enumerate(all_entries):
        if entry:
            elements, field_dict = recursive_gen(entry)
            if elements and field_dict['school']: 
                output.append(field_dict)
    return output





if __name__=="__main__":
    data_dir = "/Users/abaruwa/Desktop/PERSONAL/Spring 2022/Data Science/Project/gradcafe_data/all/data"

    rows = []
    for html_file in tqdm(glob(os.path.join(data_dir, '*.html'))):
        #print(html_file)
        output = extract_fields(html_file)
        rows.extend(output)
    df = pd.DataFrame(rows)
    print(df.shape, len(rows))
    ## Write output to csv

    outfile = "gradCafe_2022.csv"
    df.to_csv(outfile, sep='\t', index=False, encoding='utf-8')
