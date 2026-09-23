#!/usr/bin/env python3
"""curation/*.json 에서 문제를 선별하고 오답 선택지를 배정해 quiz_data.json 생성."""
import json, glob, os

ORDER = ["냥냥 인천 여","닭발 수원 남","씽씽 신도림 여","우주 은평 여","늉니 가산 남",
         "라이언 강서 남","저당 수원 여","엠줴 인천 여","꿀꿀 양천 여","호두 용인 남"]

# 멤버별 선정 문제 인덱스 (curation 파일의 quiz_candidates 순서 기준)
PICKS = {
    "냥냥 인천 여": [0,1,3,4],
    "닭발 수원 남": [0,4,2,3],
    "씽씽 신도림 여": [0,1,3,4],
    "우주 은평 여": [0,1,2,4],
    "늉니 가산 남": [1,2,4,5],
    "라이언 강서 남": [1,3,4,5],
    "저당 수원 여": [0,1,3,4],
    "엠줴 인천 여": [0,1,2,3],
    "꿀꿀 양천 여": [1,2,3,4],
    "호두 용인 남": [0,1,3,4],
}

# 문제별 오답 3명 (선정 인덱스와 동일 순서). 중복 표현 사용자는 오답에서 제외함.
DISTRACTORS = {
    "냥냥 인천 여": [["엠줴 인천 여","꿀꿀 양천 여","씽씽 신도림 여"],
                     ["우주 은평 여","꿀꿀 양천 여","호두 용인 남"],
                     ["꿀꿀 양천 여","씽씽 신도림 여","엠줴 인천 여"],
                     ["씽씽 신도림 여","엠줴 인천 여","꿀꿀 양천 여"]],
    "닭발 수원 남": [["늉니 가산 남","호두 용인 남","라이언 강서 남"],
                     ["라이언 강서 남","우주 은평 여","호두 용인 남"],
                     ["늉니 가산 남","호두 용인 남","라이언 강서 남"],
                     ["호두 용인 남","늉니 가산 남","라이언 강서 남"]],
    "씽씽 신도림 여": [["냥냥 인천 여","우주 은평 여","엠줴 인천 여"],
                       ["냥냥 인천 여","저당 수원 여","꿀꿀 양천 여"],
                       ["호두 용인 남","닭발 수원 남","우주 은평 여"],
                       ["냥냥 인천 여","우주 은평 여","저당 수원 여"]],
    "우주 은평 여": [["늉니 가산 남","호두 용인 남","씽씽 신도림 여"],
                     ["저당 수원 여","씽씽 신도림 여","냥냥 인천 여"],
                     ["닭발 수원 남","늉니 가산 남","라이언 강서 남"],
                     ["호두 용인 남","닭발 수원 남","늉니 가산 남"]],
    "늉니 가산 남": [["닭발 수원 남","라이언 강서 남","호두 용인 남"],
                     ["호두 용인 남","닭발 수원 남","라이언 강서 남"],
                     ["닭발 수원 남","라이언 강서 남","호두 용인 남"],
                     ["호두 용인 남","닭발 수원 남","라이언 강서 남"]],
    "라이언 강서 남": [["늉니 가산 남","닭발 수원 남","우주 은평 여"],
                       ["닭발 수원 남","늉니 가산 남","호두 용인 남"],
                       ["닭발 수원 남","늉니 가산 남","호두 용인 남"],
                       ["호두 용인 남","늉니 가산 남","닭발 수원 남"]],
    "저당 수원 여": [["씽씽 신도림 여","꿀꿀 양천 여","엠줴 인천 여"],
                     ["우주 은평 여","씽씽 신도림 여","냥냥 인천 여"],
                     ["냥냥 인천 여","엠줴 인천 여","꿀꿀 양천 여"],
                     ["꿀꿀 양천 여","우주 은평 여","씽씽 신도림 여"]],
    "엠줴 인천 여": [["냥냥 인천 여","우주 은평 여","저당 수원 여"],
                     ["냥냥 인천 여","꿀꿀 양천 여","우주 은평 여"],
                     ["냥냥 인천 여","라이언 강서 남","우주 은평 여"],
                     ["우주 은평 여","냥냥 인천 여","꿀꿀 양천 여"]],
    "꿀꿀 양천 여": [["우주 은평 여","엠줴 인천 여","저당 수원 여"],
                     ["냥냥 인천 여","엠줴 인천 여","저당 수원 여"],
                     ["늉니 가산 남","닭발 수원 남","라이언 강서 남"],
                     ["닭발 수원 남","늉니 가산 남","라이언 강서 남"]],
    "호두 용인 남": [["늉니 가산 남","닭발 수원 남","라이언 강서 남"],
                     ["늉니 가산 남","라이언 강서 남","닭발 수원 남"],
                     ["냥냥 인천 여","엠줴 인천 여","꿀꿀 양천 여"],
                     ["늉니 가산 남","라이언 강서 남","닭발 수원 남"]],
}

# 프로필 카드용 이모지
EMOJI = {"냥냥 인천 여":"🐱","닭발 수원 남":"🍗","씽씽 신도림 여":"🎤","우주 은평 여":"🚀",
         "늉니 가산 남":"🧞","라이언 강서 남":"🏀","저당 수원 여":"🧋","엠줴 인천 여":"🐶",
         "꿀꿀 양천 여":"🏋️","호두 용인 남":"🌰"}

def load(member):
    path = "curation/" + member.replace(" ", "_") + ".json"
    return json.load(open(path, encoding="utf-8"))

members = []
questions = []
for m in ORDER:
    d = load(m)
    pe = d["persona"]
    members.append({
        "name": m,
        "emoji": EMOJI[m],
        "oneLiner": pe.get("one_liner", ""),
        "traits": pe.get("traits", [])[:3],
        "catchphrases": pe.get("catchphrases", [])[:4],
        "activeTime": pe.get("active_time", ""),
        "episodes": [{"title": e["title"], "summary": e["summary"]} for e in d.get("episodes", [])[:4]],
    })
    for qi, idx in enumerate(PICKS[m]):
        q = d["quiz_candidates"][idx]
        choices = [m] + DISTRACTORS[m][qi]
        questions.append({
            "type": q["type"],
            "difficulty": q["difficulty"],
            "question": q["question"],
            "choices": choices,
            "answer": 0,  # 셔플은 게임 쪽에서
            "answerName": m,
            "explanation": q.get("hint", ""),
        })

# 검증
for q in questions:
    assert len(q["choices"]) == 4 and len(set(q["choices"])) == 4, q["question"][:40]
    assert q["choices"][0] == q["answerName"]

out = {"members": members, "questions": questions}
json.dump(out, open("quiz_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"members: {len(members)}, questions: {len(questions)}")
import collections
print(collections.Counter(q["answerName"] for q in questions))
print(collections.Counter(q["difficulty"] for q in questions))
