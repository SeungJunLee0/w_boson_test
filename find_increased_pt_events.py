def parse_log_and_find_increased_events(log_path, threshold=0.0):
    with open(log_path) as f:
        lines = f.readlines()

    events = []
    current_event = None
    hepmc_pts = []
    lhe_pts = []
    mode = None  # "hepmc" or "lhe"

    for line in lines:
        line = line.strip()
        if line.startswith("event"):
            if current_event is not None and len(hepmc_pts) == len(lhe_pts):
                if any(h > l + threshold for h, l in zip(hepmc_pts, lhe_pts)):
                    events.append(current_event)
            current_event = int(line.replace("event", ""))
            hepmc_pts = []
            lhe_pts = []
        elif "hepmc 정보" in line:
            mode = "hepmc"
        elif "lhe 정보" in line:
            mode = "lhe"
        elif line.startswith("pt ="):
            pt = float(line.replace("pt = ", ""))
            if mode == "hepmc":
                hepmc_pts.append(pt)
            elif mode == "lhe":
                lhe_pts.append(pt)

    # 마지막 이벤트 처리
    if current_event is not None and len(hepmc_pts) == len(lhe_pts):
        if any(h > l + threshold for h, l in zip(hepmc_pts, lhe_pts)):
            events.append(current_event)

    return events

# 사용 예시
if __name__ == "__main__":
    log_file = "log.log"
    threshold = 10.0  # 여기를 원하는 값으로 설정하세요
    events = parse_log_and_find_increased_events(log_file, threshold=threshold)
    print("LHE보다 HepMC에서 W boson pt가 증가한 이벤트:")
    k=0
    for e in events:
        print(f"event{e}")
        k+=1
        if k > 10:
            break

