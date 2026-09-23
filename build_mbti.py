import json, glob, os, sys

questions = json.load(open("mbti_questions_draft.json", encoding="utf-8"))
types = json.load(open("mbti_types.json", encoding="utf-8"))

votes = {}
for f in glob.glob("mbti_votes/*.json"):
    d = json.load(open(f, encoding="utf-8"))
    key = os.path.basename(f).replace(".json", "")
    assert len(d["answers"]) == 12, f
    votes[key] = d["answers"]

def code_of(ans):
    # 축별 a 개수 2 이상이면 앞극 글자
    out = []
    for axis, qs in [("O", [1,2,3]), ("V", [4,5,6]), ("D", [7,8,9]), ("N", [10,11,12])]:
        a = sum(1 for q in qs if ans[str(q)] == "a")
        out.append((axis if a >= 2 else {"O":"J","V":"T","D":"R","N":"M"}[axis]))
    return "".join(out)

members = []
for m in types["members"]:
    key = m["name"].replace(" ", "_")
    assert key in votes, key
    ans = votes[key]
    members.append({"name": m["name"], "emoji": m["emoji"], "blurb": m["blurb"],
                    "code": code_of(ans), "answers": [ans[str(i)] for i in range(1, 13)]})

# 답안지 유일성 + 셀프매칭 검증
sheets = ["".join(m["answers"]) for m in members]
assert len(set(sheets)) == 10, "중복 답안지 있음"
for i, m in enumerate(members):
    dists = sorted(sum(a != b for a, b in zip(m["answers"], n["answers"])) for n in members if n is not m)
    assert dists[0] >= 1, m["name"]
    print(m["emoji"], m["name"], m["code"], "최근접 거리:", dists[0])

out = {"axes": questions["axes"], "questions": questions["questions"],
       "types": types["types"], "members": members}
json.dump(out, open("mbti_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("mbti_data.json OK — members:", len(members), "types:", len(types["types"]))
