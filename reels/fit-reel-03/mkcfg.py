"""Scene plan for FIT reel 03, timed to each voiceover. Writes cfg-<lang>.json.
Times in the VO are word starts from words.json; O shifts the VO so the search bar starts typing first."""
import json, sys
O = 0.3
REAL, REP = "Actual site footage", "Representational model, not the actual site"
BW = "hue=s=0,curves=all='0/0 0.2/0.07 0.5/0.45 0.8/0.9 1/1'"
COL = "eq=contrast=1.06:saturation=1.04"

def plan(lang):
    w = json.load(open(f"../{ 'en-1' if lang == 'en' else 'hi-1' }/words.json"))
    vo_len = w[-1][2]
    T = lambda i: round(w[i][1] + O, 3)          # start of word i
    def find(s, k=0):
        ex = [i for i, x in enumerate(w) if x[0].strip('?.,।…') == s]
        return ex[k] if len(ex) > k else [i for i, x in enumerate(w) if x[0].strip('?.,।') .startswith(s)][k]
    if lang == "en":
        k = dict(found=find("Found"), forte=find("Forte"), ind=find("Industrial"), town=find("Township"), roh=find("Rohtak"),
                 a=find("A"), n138=find("thirty"), acres=find("acres"), planned=find("planned"), plots=find("Plots"), five=find("five"),
                 sq=find("square"), on=find("on"), e18=find("eighteen"), roads=find("roads"), built=find("built"), trucks=find("trucks"),
                 ten=find("Ten"), nh=find("NH"), tw=find("Twenty"), imt=find("IMT"), andw=find("And"), work=find("work"),
                 onthe=find("on", 1), rera=find("RERA"), tap=find("Tap"), wa=find("WhatsApp"))
        caps = {
            "nh": [["10 min to", "ten"], ["br"], ["NH-152D.", "nh", "red"]],
            "imt": [["25 min to", "tw"], ["br"], ["IMT Rohtak.", "imt", "red"]],
        }
    else:
        k = dict(found=find("मिल"), forte=find("फ़ोर्टे"), ind=find("इंडस्ट्रियल"), town=find("टाउनशिप"), roh=find("रोहतक"),
                 a=find("एक"), n138=find("अड़तीस"), acres=find("एकड़"), planned=find("इंडस्ट्री"), plots=find("पाँच"), five=find("पाँच"),
                 sq=find("स्क्वेयर"), on=find("अठारह"), e18=find("अठारह"), roads=find("सड़कों"), built=find("ट्रकों"), trucks=find("ट्रकों"),
                 ten=find("NH"), nh=find("NH"), tw=find("IMT"), imt=find("IMT"), andw=find("और", 1), work=find("काम"),
                 onthe=find("शुरू"), rera=find("RERA"), tap=find("नीचे"), wa=find("WhatsApp"))
        k["dus"] = find("दस"); k["pach"] = find("पच्चीस")
        caps = {
            "nh": [["NH-152D", "nh", "red"], ["br"], ["in 10 min.", "dus"]],
            "imt": [["IMT Rohtak", "imt", "red"], ["br"], ["in 25 min.", "pach"]],
        }
    t = {n: T(i) for n, i in k.items()}
    DROP, RERA, END = t["found"], t["rera"], t["tap"]
    D = round(O + vo_len + 1.6, 2)
    def cap(words):
        out = []
        for x in words:
            if x[0] == "br": out.append(["br"]); continue
            out.append([x[0], t[x[1]]] + ([x[2]] if len(x) > 2 else []))
        return out
    S = []  # caption scenes: a, b, size, ghost, chip, words, sub
    S.append(dict(a=DROP, b=t["forte"], sz=330, gh="FOUND", chip=REAL, w=cap([["Found", "found"], ["it.", "found", "red"]])))
    S.append(dict(a=t["forte"], b=t["a"], sz=150, gh="FIT", chip=REAL, w=cap([["Forteasia", "forte"], ["br"], ["Industrial", "ind"], ["br"], ["Township", "town", "red"]]), sub=["Kalanaur, Rohtak", t["roh"]]))
    S.append(dict(a=t["a"], b=t["plots"], sz=330, gh="138", chip=REAL, w=cap([["138+", "n138"], ["br"], ["acres", "acres", "red"]]), sub=["Planned for industry", t["planned"]]))
    S.append(dict(a=t["plots"], b=t["on"], sz=186, gh="PLOTS", chip=REAL, plot=1, w=cap([["Plots from", "plots", "sm"], ["500 to 4,000", "five"], ["br"], ["sq yd", "sq", "red"]])))
    S.append(dict(a=t["on"], b=t["built"], sz=205, gh="ROADS", chip=REAL, w=cap([["18 m & 24 m", "e18"], ["br"], ["roads.", "roads", "red"]])))
    S.append(dict(a=t["built"], b=t["ten"], sz=250, gh="TRUCKS", chip=REAL, w=cap([["Built for", "built"], ["br"], ["trucks.", "trucks", "red"]])))
    S.append(dict(a=t["ten"], b=t["tw"], sz=230, gh="NH-152D", chip=REAL, w=cap(caps["nh"])))
    S.append(dict(a=t["tw"], b=t["andw"], sz=200, gh="IMT", chip=REP, w=cap(caps["imt"])))
    S.append(dict(a=t["andw"], b=RERA, sz=200, gh="NOW", chip=REAL, w=cap([["Work is already", "work", "sm"], ["on the", "onthe"], ["br"], ["ground.", "onthe", "red"]])))
    # footage under each scene (a, b, clip, start offset, speed, grade, zoom)
    sh = [(0, DROP, "real-truck", 0.0, 0.6, BW + ",eq=brightness=-0.2,gblur=sigma=14", 1.0)]
    sh += [(DROP, t["forte"], "real-gate", 1.3, 1.0, BW, 1.0)]
    mid = round((t["forte"] + t["a"]) / 2, 3)
    sh += [(t["forte"], mid, "real-sign", 0.0, 0.75, BW, 1.0), (mid, t["a"], "real-office", 0.2, 1.0, BW, 1.0)]
    mid = round((t["a"] + t["plots"]) / 2, 3)
    sh += [(t["a"], mid, "real-aerial1", 0.3, 1.0, BW, 1.0), (mid, t["plots"], "real-aerial3", 3.0, 1.0, BW, 1.0)]
    sh += [(t["plots"], t["on"], "real-aerial3", 0.2, 1.1, BW, 1.0)]
    sh += [(t["on"], t["built"], "real-road", 0.2, 1.5, BW, 1.0)]
    sh += [(t["built"], t["ten"], "real-truck", 0.6, 1.2, BW, 1.0)]
    sh += [(t["ten"], t["tw"], "real-aerial2", 1.2, 1.0, BW, 1.0)]
    sh += [(t["tw"], t["andw"], "ai-02", 0.5, 1.2, COL, 1.0)]
    q = [t["andw"], round(t["andw"] + 0.75, 3), round(t["andw"] + 1.3, 3), RERA]
    sh += [(q[0], q[1], "real-road", 2.4, 1.4, BW, 1.0), (q[1], q[2], "real-aerial1", 1.8, 1.4, BW, 1.15), (q[2], q[3], "real-truck", 2.0, 1.2, BW, 1.1)]
    sh += [(RERA, D, None, 0, 1, None, 1)]
    cuts = sorted({round(x[0], 3) for x in sh[1:]} | {END})
    wipes = [t["a"], t["ten"], t["andw"], RERA]
    return dict(lang=lang, O=O, D=D, DROP=DROP, RERA=RERA, END=END, WA=t["wa"], SC=S, shots=sh, cuts=cuts, wipes=wipes,
                hook="Land for my factory", vo=f"../{'en-1' if lang == 'en' else 'hi-1'}/vo.wav", vo_len=vo_len)

for lang in sys.argv[1:] or ["en", "hi"]:
    c = plan(lang)
    json.dump(c, open(f"cfg-{lang}.json", "w"), indent=1, ensure_ascii=False)
    print(lang, "D", c["D"], "DROP", c["DROP"], "RERA", c["RERA"], "END", c["END"], "scenes", len(c["SC"]), "shots", len(c["shots"]))
    for s in c["SC"]:
        print("  %.2f-%.2f %.2fs %s" % (s["a"], s["b"], s["b"] - s["a"], " ".join(x[0] for x in s["w"] if x[0] != "br")))
