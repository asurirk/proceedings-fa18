#! /usr/bin/env python
import glob
from pprint import pprint
import oyaml as yaml
import os
import sys

files = glob.glob("fa18*/README.yml")

ERROR=":o:"
SMILEY=":smiley:"
REVIEWED=":exclamation:"
WAVE=":wave:"
HAND=":hand:"

ERROR="![:o:](images/o.png)"
SMILEY="![:smiley:](images/smiley.png)"
REVIEWED="![:exclamation:](images/exclamation.png)"

def read_technology(url):
    filename = url.replace("https://github.com/cloudmesh/technologies/blob/master", "../../cloudmesh/technologies")
    with open(filename, "r") as f:
       content = f.read()
    return content
    
#pprint (files)
readmes = {}
for readme in files:
    with open(readme, 'r') as stream:
        filename = readme.replace("/README.yml","") # use dir name or so
        try:
            d = yaml.load(stream)
            readmes[filename] = d
        except yaml.YAMLError as exc:
            print(exc)


paper_template = '''
@InBook{open}{LABEL},
  author =       "{name}",
  editor =       "Gregor von Laszewski",
  title =        "{title}",
  publisher =    "Indiana University",
  year =         "2018",
  volume =       "Fall 2018",
  series =       "Class",
  type =         "Paper",
  address =      "Bloomington, IN 47408",
  month =        dec,
  note =         "Online",
  url =          "{url}"
{close}
'''

project_template = '''
@InBook{open}{LABEL},
  author =       "{name}",
  editor =       "Gregor von Laszewski",
  title =        "{title}",
  publisher =    "Indiana University",
  year =         "2018",
  volume =       "Fall 2018",
  series =       "Class",
  type =         "Project",
  address =      "Bloomington, IN 47408",
  month =        dec,
  note =         "Online",
  url =          "{url}"
{close}
'''

            
def print_ref(data, kind):
#    pprint(data)
    if kind in data:
        counter = 0
        for p in data[kind]:
            data["kind"] = kind
            data["close"] = "}"
            data["open"] = "{"            
            data["counter"] = counter
            data["LABEL"] = "{hid}-{kind}-{counter}".format(**data["owner"], **data)
            data["name"] = "{firstname} {lastname}".format(**data["owner"])
            if "url" not in data[kind][counter] or \
               "title" not in data[kind][counter]:
                pass
            else:
                print(paper_template.format(**data, **data[kind][counter]))
            counter = counter + 1    
            
# print(yaml.dump(readmes, default_flow_style=False))

for hid in readmes:

    print_ref(readmes[hid], "project")
    print_ref(readmes[hid], "paper")    



sys.exit()

def print_community(community):

    counter = 1
    for hid in readmes:
        entry = {
            "semester": ERROR,
            "readme": ERROR,
            "hid": ERROR,
            "firstname": ERROR,
            "lastname": ERROR,
            "community": ERROR,
            "t1": ERROR,
            "t2": ERROR,
            "t3": ERROR,
            "t4": ERROR,
            "t5": "N/A",
            "t6": "N/A",
            "paper": ERROR,
            "project": ERROR,
            "projectkey": "project",
            "paperkey": "paper",                                
            }

        try:
            s = readmes[hid]
            entry["readme"] = "[{hid}](https://github.com/cloudmesh-community/{hid}/blob/master/README.yml)".format(hid=hid)
            entry["hid"] = hid
            entry["lastname"] = s["owner"]["lastname"]
            entry["firstname"] = s["owner"]["firstname"]
            entry["community"] = s["owner"]["community"]
            if "semester" in s["owner"]:
                entry["semester"] = s["owner"]["semester"]

            #print (entry["community"])
            #if entry["community"] not hid:
            #    break;
            
            if "516" in entry["community"]:
                for t in ["t1", "t2", "t3", "t4", "t5", "t6"]:
                     entry[t] = "N/A"
            else:
                t = ""
                c = -1
                for t in ["t1", "t2", "t3", "t4", "t5", "t6"]:
                    c = c + 1
                    status = "?"
                    try:
                        url = s["technologies"][c]["url"]
                        content = read_technology(url)
                        
                        if ":smiley:" in content:
                            status = SMILEY
                        elif ":hand:" in content:
                            status = HAND
                        elif ":wave:" in content:
                            status = WAVE
                            
                        if ":exclamation:" in content:
                            status = status + REVIEWED
                        if ":o:" in content:
                            status = status + ERROR
                            
                        entry[t] = "{status}[{t}]({url})".format(t=t,url=url, status=status)
                            
                    except Exception as e:
                        pass

            # paper
            if "paper" in s:
              try:
                  
                  title = s["paper"][0]["title"]
                  url   = s["paper"][0]["url"]
                  if "keyword" in s["paper"][0]:
                      entry["paperkey"] = s["paper"][0]["keyword"]
                      
                  if "group" in ["paper"][0]:
                      if hid in url:
                          entry["paper"] = "[paper]({url})".format(**entry,url=url)
                      else:
                          entry["paper"] = "see [{paperkey}]({url})".format(**entry,url=url)
                  entry["paper"] = "[{paperkey}]({url})".format(**entry,url=url)
              except:
                  entry["paper"] = "TBD"

                          # paper
            if "project" in s:
              try:
                  title = s["project"][0]["title"]
                  url   = s["project"][0]["url"]
                  if "keyword" in s["project"][0]:
                      entry["projectkey"] = s["project"][0]["keyword"]
                      

                  if "group" in ["project"][0]:
                      if hid in url:
                          entry["project"] = "[{projectkey}]({url})".format(**entry, url=url)
                      else:
                          entry["project"] = "see [{projectkey}]({url})".format(**entry, url=url)
                  entry["project"] = "[{projectkey}]({url})".format(**entry,url=url)
              except:
                  entry["project"] = "TBD"


        except:
            pass

        if community in entry["hid"]:
            entry["counter"] = counter
            counter = counter + 1
            
            print ("| {counter} | {semester} | {readme} | {lastname} | {firstname} | {community} | {t1} | {t2} | {t3} | {t4} | {t5} | {t6} | {paper} | {project} |".format(**entry))

for c in ["523", "423", "516"]:
    print ("#", c)
    print("\n")
    print_community(c)
    print("\n")
