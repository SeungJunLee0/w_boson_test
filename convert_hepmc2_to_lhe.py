import sys

def extract_events_from_hepmc2(hepmc_file, output_file):
    allowed_status_codes = {1, 2, 23, 44, 62}

    def is_float(x):
        try:
            float(x)
            return True
        except:
            return False

    with open(hepmc_file) as f, open(output_file, "w") as out:
        particles = []
        for line in f:
            if line.startswith("E "):  # 이벤트 시작
                if particles:
                    out.write("<event>\n")
                    out.write(f"{len(particles)} 1 0 0 0 0\n")
                    out.writelines(p + "\n" for p in particles)
                    out.write("</event>\n")
                    particles = []
            elif line.startswith("P "):
                parts = line.strip().split()
                if len(parts) < 13:
                    continue
                pid = int(parts[2])
                px = float(parts[3])
                py = float(parts[4])
                pz = float(parts[5])
                E  = float(parts[6])
                m  = float(parts[7])
                # 상태 코드가 위치가 변할 수 있어서 뒤에서 숫자형인 항목을 찾음
                status = None
                for val in parts[8:]:
                    if val.isdigit():
                        status = int(val)
                        break
                if status is None or status not in allowed_status_codes:
                    continue
                lhe_line = f"{pid:>8} 1 0 0 0 0 {px:>14.8e} {py:>14.8e} {pz:>14.8e} {E:>14.8e} {m:>10.5f} 0.0 0.0"
                particles.append(lhe_line)

        # 마지막 이벤트
        if particles:
            out.write("<event>\n")
            out.write(f"{len(particles)} 1 0 0 0 0\n")
            out.writelines(p + "\n" for p in particles)
            out.write("</event>\n")

if __name__ == "__main__":
    hepmc_file = "bb4l_pythia_0001.hepmc"
    output_file = "converted_from_hepmc2.lhe"
    extract_events_from_hepmc2(hepmc_file, output_file)
    print(f"✅ 완료: {output_file} 생성됨.")

