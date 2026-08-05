from pathlib import Path

ROOT=Path(".")
SRC=ROOT/"PROJECT_FULL_CONTEXT_PACK.md"
OUT=ROOT/"AUDIT_PACKS"

OUT.mkdir(exist_ok=True)

MAX=180000

ALLOW={
"A_01_CORE",
"A_02_MANAGERS",
"A_03_ORCHESTRATION",
"A_04_AGENTS",
"A_05_STORAGE",
"A_07_CONFIG",
"A_07_MEMORY",
"A_09_GUARDIANS",
"A_10_BUTLER_OS"
}

text=SRC.read_text(encoding="utf-8")

blocks=text.split("\n---\n")

packs={}
current={}
sizes={}

for b in blocks:

    if "## FILE:" not in b:
        continue

    line=b.splitlines()[0]

    try:
        rel=line.split("## FILE:")[1].strip()
    except:
        continue

    top=rel.split("/")[0].split("\\")[0]

    if top not in ALLOW:
        continue

    current.setdefault(top,[])
    sizes.setdefault(top,0)

    if sizes[top]+len(b)>MAX:

        idx=len(current[top])+1

        fn=OUT/f"{top}_part_{idx:03d}.md"

        fn.write_text(
            "\n---\n".join(current[top]),
            encoding="utf-8"
        )

        print(fn.name,"OK",sizes[top])

        current[top]=[]
        sizes[top]=0

    current[top].append(b)
    sizes[top]+=len(b)

for top in sorted(current):

    if current[top]:

        idx=len(list(OUT.glob(f"{top}_part_*.md")))+1

        fn=OUT/f"{top}_part_{idx:03d}.md"

        fn.write_text(
            "\n---\n".join(current[top]),
            encoding="utf-8"
        )

        print(fn.name,"OK",sizes[top])

print()
print("FINISHED")
