#!/usr/bin/env python3
"""curation/*.json 의 episodes를 이상형 월드컵 카드 풀로 변환 → worldcup_data.json"""
import json

ORDER = ["냥냥 인천 여","닭발 수원 남","씽씽 신도림 여","우주 은평 여","늉니 가산 남",
         "라이언 강서 남","저당 수원 여","엠줴 인천 여","꿀꿀 양천 여","호두 용인 남"]
EMOJI = {"냥냥 인천 여":"🐱","닭발 수원 남":"🍗","씽씽 신도림 여":"🎤","우주 은평 여":"🚀",
         "늉니 가산 남":"🧞","라이언 강서 남":"🏀","저당 수원 여":"🧋","엠줴 인천 여":"🐶",
         "꿀꿀 양천 여":"🏋️","호두 용인 남":"🌰"}

# 결과 화면용 '어떤 타입에 끌렸는지' 한 줄 멘트 (캐릭터 반영)
MATCH_DESC = {
    "냥냥 인천 여": "귀엽고 애교 넘치는 말투에 약한 타입! 오타마저 사랑스러운 사람에게 끌리네요 🐱",
    "닭발 수원 남": "자학 개그와 허당미에 끌리는 타입! 웃기면서 어딘가 챙겨주고 싶은 사람이 취향이군요 🍗",
    "씽씽 신도림 여": "리더십 있고 챙김받는 느낌에 약한 타입! 분위기를 이끌어주는 언니/누나 스타일에 끌리네요 🎤",
    "우주 은평 여": "에너지 넘치고 취향 확고한 사람에게 끌리는 타입! 같이 있으면 지루할 틈이 없는 사람이 취향이에요 🚀",
    "늉니 가산 남": "든든한 맏형/오빠 스타일에 약한 타입! 묵묵히 챙겨주는 츤데레에 끌리네요 🧞",
    "라이언 강서 남": "울끈불끈 몸짱 + 가족사랑, 반전 매력에 약한 타입! 욜로 욜로 놀면서도 속은 따뜻한 사람에게 끌려요 🏀",
    "저당 수원 여": "장난기 많고 텐션 높은 사람에게 끌리는 타입! 매일이 시트콤 같은 연애를 원하시네요 🧋",
    "엠줴 인천 여": "하이텐션 + 솔직함에 끌리는 타입! 거절 없는 긍정 에너지의 소유자에게 빠지셨군요 🐶",
    "꿀꿀 양천 여": "웃음 많고 털털한 사람에게 끌리는 타입! 같이 있으면 하루종일 웃을 수 있는 사람이 취향이에요 🏋️",
    "호두 용인 남": "든든하고 먹는 것에 진심인 큰형 스타일에 약한 타입! 믿고 따라갈 수 있는 사람에게 끌리네요 🌰",
}

# 블라인드 모드 보정: 자기 이름이 인용에 포함된 카드 드롭/트림
DROP_CARDS = {
    ("씽씽 신도림 여", "방 전원 닮은꼴 총정리"),  # 인용에 '씽씽 = 박초롱' 포함 → 정체 노출
}
REPLACE_QUOTES = {
    ("닭발 수원 남", "수원 곱창벙 벙주의 고군분투"):
        "오늘의 메인 주제는\n왜수원벙에 사람이 안붙을까 입니다.",  # '정정) 닭발이...' 부분 제거
    ("호두 용인 남", "수원 곱창벙, 벙 장소가 문 닫혀버린 사건"):
        "소곱3 곱전 중짜리 ㄱㄱ\n자리잡음",  # @멘션 제거
}

members = []
for m in ORDER:
    d = json.load(open("curation/" + m.replace(" ", "_") + ".json", encoding="utf-8"))
    cards = []
    for e in d.get("episodes", []):
        quote = (e.get("quote") or "").strip()
        if not quote:
            continue
        if (m, e["title"]) in DROP_CARDS:
            continue
        quote = REPLACE_QUOTES.get((m, e["title"]), quote.replace(" / ", "\n"))
        cards.append({"title": e["title"], "quote": quote, "story": e["summary"]})
    members.append({
        "name": m,
        "emoji": EMOJI[m],
        "oneLiner": d["persona"].get("one_liner", ""),
        "matchDesc": MATCH_DESC[m],
        "cards": cards,
    })

for m in members:
    assert len(m["cards"]) >= 4, (m["name"], len(m["cards"]))

json.dump({"members": members}, open("worldcup_data.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("members:", len(members), "/ cards:", sum(len(m["cards"]) for m in members))
