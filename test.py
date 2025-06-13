import pyhepmc
import xml.etree.ElementTree as ET
import math
import pyhepmc.io  # 중요

def get_pt(px, py):
    return math.sqrt(px**2 + py**2)

def get_lhe_w_pts(lhe_file):
    with open(lhe_file) as f:
        in_event = False
        pts = []
        for line in f:
            if line.strip() == "<event>":
                in_event = True
                w_pts = []
                continue
            if line.strip() == "</event>":
                pts.append(w_pts)
                in_event = False
                continue
            if in_event:
                parts = line.strip().split()
                if len(parts) < 13:
                    continue
                pdg = int(parts[0])
                if abs(pdg) == 24:  # W boson
                    px, py = float(parts[6]), float(parts[7])
                    w_pts.append(get_pt(px, py))
    return pts

lhe_w_pts = get_lhe_w_pts("pwgevents-0001.lhe")

reader = pyhepmc.io.ReaderAscii("bb4l_pythia_0001_cleaned.hepmc")
i_event = 0

while not reader.failed():
    evt = pyhepmc.io.GenEvent()  # ✅ 이걸로 생성해야 함
    reader.read_event(evt)

    if reader.failed(): break

    w_pts_hepmc = []
    for p in evt.particles:
        if abs(p.pid) == 24:
            px, py = p.momentum.x, p.momentum.y
            w_pts_hepmc.append(get_pt(px, py))

    # 비교
    try:
        for i in range(min(len(w_pts_hepmc), len(lhe_w_pts[i_event]))):
            if w_pts_hepmc[i] > lhe_w_pts[i_event][i]:
                print(f"[Event {i_event}] HEPMC W pt ({w_pts_hepmc[i]:.2f}) > LHE W pt ({lhe_w_pts[i_event][i]:.2f})")
    except IndexError:
        print(f"[Event {i_event}] mismatch in W boson count")

    i_event += 1

