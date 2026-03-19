import re
from datetime import date
from dateutil.relativedelta import relativedelta

def update_svg():
    start_date = date(1999, 3, 12)
    current_date = date.today()
    diff = relativedelta(current_date, start_date)

    uptime_text = f"{diff.years}년 {diff.months}개월 {diff.days}일"
    svg_files = ["dark_mode.svg", "light_mode.svg"]

    pattern = re.compile(r'(Uptime</tspan>.*?<tspan class="value">)[^<]+(</tspan>)', re.DOTALL)

    for file_name in svg_files:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = pattern.sub(rf'\g<1>{uptime_text}\g<2>', content)

            with open(file_name, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"{file_name} 업데이트 완료: {uptime_text}")

        except FileNotFoundError:
            print(f"오류: {file_name} 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    update_svg()