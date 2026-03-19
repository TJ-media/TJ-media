import re
import urllib.parse
from datetime import date
from dateutil.relativedelta import relativedelta

def update_readme():
    # 1. 날짜 계산 (기준일: 1999년 3월 12일)
    start_date = date(1999, 3, 12)
    current_date = date.today()
    diff = relativedelta(current_date, start_date)

    uptime_text = f"{diff.years}년 {diff.months}개월 {diff.days}일"
    encoded_uptime = urllib.parse.quote(uptime_text)

    # 2. README.md 파일 읽기
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 3. 정규식으로 배지 이미지 URL 부분만 찾아 교체
    pattern = r"(https://img\.shields\.io/badge/Uptime-).*?(-000000\?style=for-the-badge&logo=clock&logoColor=white)"
    replacement = rf"\g<1>{encoded_uptime}\g<2>"
    new_content = re.sub(pattern, replacement, content)

    # 4. 변경된 내용 저장
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    update_readme()