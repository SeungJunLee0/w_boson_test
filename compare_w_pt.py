import math

def get_pt(px, py):
    return math.sqrt(px**2 + py**2)

# LHE 파일에서 W boson의 pt 정보 추출
def get_lhe_w_pts(lhe_file):
    with open(lhe_file) as f:
        in_event = False
        w_pts_all = []
        current_pts = []
        for line in f:
            line = line.strip()
            if line == "<event>":
                in_event = True
                current_pts = []
                continue
            elif line == "</event>":
                w_pts_all.append(current_pts)
                in_event = False
                continue
            elif in_event:
                parts = line.split()
                if len(parts) < 10:
                    continue
                pdg_id = int(parts[0])
                if pdg_id == 24:
                    px = float(parts[6])
                    py = float(parts[7])
                    current_pts.append(get_pt(px, py))
        return w_pts_all

# HepMC2 파일에서 W boson의 pt 정보 추출
def get_hepmc2_w_pts(hepmc_file):
    w_pts_all = []
    current_pts = []
    with open(hepmc_file) as f:
        for line in f:
            line = line.strip()
            if line.startswith("E "):  # 이벤트 시작
                if current_pts:
                    w_pts_all.append(current_pts)
                    current_pts = []
            elif line.startswith("P "):  # particle entry
                parts = line.split()
                if len(parts) < 13:
                    continue
                pid = int(parts[2])
                if pid == 24:
                    px = float(parts[3])
                    py = float(parts[4])
                    current_pts.append(get_pt(px, py))
        # 마지막 이벤트 추가
        if current_pts:
            w_pts_all.append(current_pts)
    return w_pts_all

# 파일 경로
lhe_file = "pwgevents-0001.lhe"
hepmc2_file = "bb4l_pythia_0001.hepmc"  # HepMC2 형식

# 데이터 수집
lhe_pts = get_lhe_w_pts(lhe_file)
hepmc_pts = get_hepmc2_w_pts(hepmc2_file)

# 비교 출력
k = 0
stop = False
for i, (lhe_event, hepmc_event) in enumerate(zip(lhe_pts, hepmc_pts)):
    for j, (lhe_pt, hepmc_pt) in enumerate(zip(lhe_event, hepmc_event)):
        if hepmc_pt > lhe_pt:
            print(f"[Event {i}, W {j}] HEPMC2 pt = {hepmc_pt:.2f} > LHE pt = {lhe_pt:.2f}")
            k +=1
        if k > 10:
            stop = True
            break
    if stop:
        break
