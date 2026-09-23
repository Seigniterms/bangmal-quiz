#!/usr/bin/env python3
"""밸런스 게임: 문제(교체 반영) + 10명 투표/반응 집계 → balance_data.json"""
import json, glob

EMOJI = {"냥냥 인천 여":"🐱","닭발 수원 남":"🍗","씽씽 신도림 여":"🎤","우주 은평 여":"🚀",
         "늉니 가산 남":"🧞","라이언 강서 남":"🏀","저당 수원 여":"🧋","엠줴 인천 여":"🐶",
         "꿀꿀 양천 여":"🏋️","호두 용인 남":"🌰"}

# 교체 문제
REPLACED = {
    11: {"id": 11, "a": "아재개그에 59명 중 혼자 빵터지기", "b": "아재개그 10개 연속 듣고 웃음 참기"},
    14: {"id": 14, "a": "벙 당일에 장소 가게가 문 닫혀 있기", "b": "벙 가는 날 KTX 놓치기"},
}

qs = {q["id"]: q for q in json.load(open("balance_questions_draft.json", encoding="utf-8"))}
qs.update(REPLACED)

# 투표 병합 (보충 파일이 원본보다 우선)
votes = {}  # id -> list of {member, pick, reaction}
for p in glob.glob("balance_votes/*.json"):
    d = json.load(open(p, encoding="utf-8"))
    member = d["member"]
    supp = "_보충" in p
    for v in d["votes"]:
        qid = v["id"]
        votes.setdefault(qid, {})
        if qid in REPLACED and not supp:
            continue  # 구 문제 투표는 버림
        votes[qid][member] = {"member": member, "pick": v["pick"], "reaction": v["reaction"]}

questions = []
for qid in sorted(qs):
    q = qs[qid]
    vmap = votes.get(qid, {})
    assert len(vmap) == 10, f"Q{qid}: 투표 {len(vmap)}개"
    va = sum(1 for v in vmap.values() if v["pick"] == "a")
    reactions = [{"member": v["member"], "emoji": EMOJI[v["member"]],
                  "side": v["pick"], "text": v["reaction"]} for v in vmap.values()]
    questions.append({"id": qid, "a": q["a"], "b": q["b"],
                      "votesA": va, "votesB": 10 - va, "reactions": reactions})

members = [{"name": m, "emoji": e} for m, e in EMOJI.items()]
json.dump({"members": members, "questions": questions},
          open("balance_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"문제 {len(questions)}개")
for q in questions:
    print(f"  Q{q['id']:>2}: {q['votesA']}:{q['votesB']}  {q['a'][:22]} vs {q['b'][:22]}")
