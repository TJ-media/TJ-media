import re
import unicodedata
import math
from datetime import date
from dateutil.relativedelta import relativedelta

def get_display_width(text):
    width = 0.0
    for c in text:
        # 한글의 너비를 1.5칸으로 계산
        if unicodedata.east_asian_width(c) in 'WF':
            width += 1.5
        else:
            width += 1.0
    return width

def update_svg():
    start_date = date(1999, 3, 12)
    current_date = date.today()
    diff = relativedelta(current_date, start_date)

    uptime_text = f"{diff.years}년 {diff.months}개월 {diff.days}일"
    svg_files = ["dark_mode.svg", "light_mode.svg"]

    # Uptime 값을 업데이트하기 위한 정규식
    uptime_pattern = re.compile(r'(<tspan class="key">Uptime</tspan><tspan class="cc">[^<]*</tspan><tspan class="value">)[^<]+(</tspan>)', re.IGNORECASE)

    # 모든 라인을 찾아 점(.) 개수를 조절하기 위한 정규식
    align_pattern = re.compile(r'(<tspan class="key">)(.*?)(</tspan><tspan class="cc">)(.*?)(</tspan><tspan class="value">)(.*?)(</tspan>)')

    TARGET_WIDTH = 54  # 터미널 한 줄의 전체 목표 너비

    for file_name in svg_files:
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                content = f.read()

            # Uptime 값을 오늘 날짜로 업데이트
            content = uptime_pattern.sub(rf'\g<1>{uptime_text}\g<2>', content)

            # 모든 줄의 길이를 계산해 점(.)의 개수를 동적으로 맞춤
            def align_match(match):
                tag_key_open = match.group(1)
                key_text = match.group(2)
                tag_cc_open = match.group(3)
                cc_text = match.group(4)
                tag_value_open = match.group(5)
                value_text = match.group(6)
                tag_close = match.group(7)

                prefix = ": " if ":" in cc_text else " "

                key_width = get_display_width(key_text)
                value_width = get_display_width(value_text)
                prefix_width = get_display_width(prefix)

                dots_count = math.ceil(TARGET_WIDTH - key_width - value_width - prefix_width - 1)

                if dots_count < 0:
                    dots_count = 0

                new_cc_text = prefix + "." * dots_count + " "

                return f"{tag_key_open}{key_text}{tag_cc_open}{new_cc_text}{tag_value_open}{value_text}{tag_close}"

            # 전체 내용 치환 적용
            new_content = align_pattern.sub(align_match, content)

            # 변경된 파일 저장
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"{file_name} 정밀 양끝 정렬 완료: {uptime_text}")

        except FileNotFoundError:
            print(f"오류: {file_name} 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    update_svg()