import math

def get_pt(px, py):
    return math.sqrt(px**2 + py**2)

# HepMC2에서 이벤트별 W boson 정보 추출
def extract_w_from_hepmc2(hepmc_file):
    with open(hepmc_file) as f:
        events = []
        current = []
        for line in f:
            line = line.strip()
            if line.startswith("E "):  # new event
                if current:
                    events.append(current)
                    current = []
            elif line.startswith("P "):
                parts = line.split()
                if len(parts) < 7:
                    continue
                try:
                    pdg_id = int(parts[2])
                    if abs(pdg_id) == 24:
                        px = float(parts[3])
                        py = float(parts[4])
                        pt = get_pt(px, py)
                        current.append({
                            "line": line,
                            "pt": pt
                        })
                except:
                    continue
        if current:
            events.append(current)
    return events

# LHE에서 이벤트별 W boson 정보 추출
def extract_w_from_lhe(lhe_file):
    with open(lhe_file) as f:
        in_event = False
        events = []
        current = []
        for line in f:
            line = line.strip()
            if line == "<event>":
                in_event = True
                current = []
                continue
            elif line == "</event>":
                events.append(current)
                in_event = False
                continue
            elif in_event:
                parts = line.split()
                if len(parts) < 10:
                    continue
                try:
                    pdg_id = int(parts[0])
                    if abs(pdg_id) == 24:
                        px = float(parts[6])
                        py = float(parts[7])
                        pt = get_pt(px, py)
                        current.append({
                            "line": line,
                            "pt": pt
                        })
                except:
                    continue
        return events

# 파일 경로 지정
hepmc_file = "bb4l_pythia_0001.hepmc"
lhe_file = "pwgevents-0001.lhe"

# 데이터 추출
hepmc_events = extract_w_from_hepmc2(hepmc_file)
lhe_events = extract_w_from_lhe(lhe_file)

# 비교 및 출력
for i, (hepmc_ws, lhe_ws) in enumerate(zip(hepmc_events, lhe_events), start=1):
    print(f"event{i}")
    for w in lhe_ws:
        print("lhe 정보")
        print(w["line"])
        print(f"pt = {w['pt']:.2f}")
    for w in hepmc_ws:
        print("hepmc 정보")
        print(w["line"])
        print(f"pt = {w['pt']:.2f}")
    print("-" * 40)

