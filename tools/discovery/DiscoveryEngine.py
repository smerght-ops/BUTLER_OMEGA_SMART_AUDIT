#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()

ARTIFACTS = {
    "PhysicalMap": "Inspector0_PhysicalMap.json",
    "EntityMap": "Inspector1_EntityMap.json",
    "ImportMap": "Inspector2_ImportMap.json",
    "RegistrationAST": "Inspector3_RegistrationAST.json",
    "CallGraph": "Inspector4_CallGraph.json",
    "LinkMap": "LinkMap.json",
    "DependencyModel": "DependencyModel.json",
}

def load(name):
    p = ROOT / ARTIFACTS[name]
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except:
        try:
            return json.loads(p.read_text(encoding="utf-8-sig"))
        except:
            return None


def split_identifier(text):

    if not text:
        return []

    text = text.replace("\\"," ")
    text = text.replace("/"," ")
    text = text.replace("."," ")
    text = text.replace("_"," ")

    return [
        x.lower()
        for x in re.findall(
            r"[A-Z]+(?=[A-Z][a-z]|\\d|$)|[A-Z]?[a-z]+|\\d+",
            text
        )
        if len(x)>1
    ]


def add(db,name,kind,source):

    if not name:
        return

    if name not in db:
        db[name]={
            "kind":set(),
            "sources":set()
        }

    db[name]["kind"].add(kind)
    db[name]["sources"].add(source)


def build():

    db={}

    em=load("EntityMap")
    if em:
        for item in em.get("payload",[]):

            src=item["id"]

            for c in item.get("classes",[]):
                add(db,c["name"],"class",src)

            for f in item.get("functions",[]):
                add(db,f["name"],"function",src)

    im=load("ImportMap")
    if im:
        for item in im.get("payload",[]):

            src=item["id"]

            for imp in item.get("imports",[]):
                add(db,imp.get("module",""),"import",src)

    rm=load("RegistrationAST")
    if rm:
        for item in rm.get("payload",[]):

            src=item["id"]

            for reg in item.get("registrations",[]):
                add(db,reg.get("function",""),"registration",src)

    cg=load("CallGraph")
    if cg:
        for item in cg.get("payload",[]):

            src=item["id"]

            for call in item.get("calls",[]):
                add(db,call.get("callee",""),"call",src)

    dm=load("DependencyModel")
    if dm:
        for node in dm.get("nodes",{}):
            add(db,node,"dependency","DependencyModel")

    return db


def search(query,db):

    q=split_identifier(query)

    result={}

    for obj,data in db.items():

        terms=split_identifier(obj)

        score=0

        for a in q:
            for b in terms:

                if a==b:
                    score+=10
                elif a in b:
                    score+=5
                elif b in a:
                    score+=5

        if score:

            result[obj]={
                "score":score,
                "kind":sorted(data["kind"]),
                "sources":sorted(map(str, data["sources"]))
            }

    return dict(
        sorted(
            result.items(),
            key=lambda x:x[1]["score"],
            reverse=True
        )
    )


def main():

    if len(sys.argv)<2:
        print("Usage: python DiscoveryEngine.py <query>")
        sys.exit(1)

    db=build()

    print("OBJECTS :",len(db))
    print()

    res=search(sys.argv[1],db)

    if not res:
        print("NOT FOUND")
        return

    for name,data in res.items():

        print("="*60)
        print(name)
        print("Score :",data["score"])
        print()

        print("Kinds")
        for k in data["kind"]:
            print("  ",k)

        print()

        print("Evidence")
        for s in data["sources"]:
            print("  ",s)

    print("="*60)

if __name__=="__main__":
    main()
