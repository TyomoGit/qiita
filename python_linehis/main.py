import re
from datetime import datetime

DATE_PATTERN: str = r'^\d{4}/\d{2}/\d{2}\(.+\)$'
YMD_PATTERN: str = "%Y/%m/%d"

class History:
    history_data: list[str]
    
    def __init__(self, data: str) -> None:
        lines = data.splitlines()

        if "のトーク履歴" in lines[0]:
            self.history_data = lines[3:]
        else:
            self.history_data = lines

    def search_by_date(self, date: datetime) -> str:
        target_date = date
        count_start: int = -1
        count_end: int = -1
        collect_flag: bool = False
        output: str = ""

        for i, line in enumerate(self.history_data):
            if not re.match(DATE_PATTERN, line):
                continue

            current_date = datetime.strptime(line[:10], YMD_PATTERN)

            if current_date == target_date:
                count_start = i
                collect_flag = True
            elif collect_flag and target_date < current_date:
                count_end = i-1
                break
        else:
            count_end = len(self.history_data)
        
        if count_start == -1:
            output = "There is no history of this date.\n"
        else:
            output += "\n".join(self.history_data[count_start:count_end])
            output += f"\n\n{count_end - count_start}行\n"
        return output
    
    def search_by_keyword(self, keyword: str) -> str:
        LOWER_LIMIT = 1
        if len(keyword) < LOWER_LIMIT:
            return "Please enter more than one character."
        
        count = 0
        output = ''
        max_date = datetime.min
        for line in self.history_data:
            if re.match(DATE_PATTERN, line):
                date = datetime.strptime(line[:10], YMD_PATTERN)
                if date >= max_date:
                    max_date = date
            else:
                if not keyword in line:
                    continue
                count += 1
                if re.match(r'^\d{2}:\d{2}.*', line):
                    line = line[6:]
                if len(line) >= 61:
                    line = line[:60] + '…'
                output += str(max_date)[:11].replace('-', '/') + " " + line + '\n'

        if output == '':
            output = 'Not found.'

        return f"{count}件\n{output}"

def main() -> None:
    with open("/Users/riku/Library/Mobile Documents/com~apple~CloudDocs/🐸GAshare/history.txt", "r", encoding="utf-8") as f:
        history = History(f.read())
    
    # 日付による検索
    print(history.search_by_date(datetime(2022, 3, 15)))

    # キーワードによる検索
    # print(history.search_by_keyword("こんにちは"))

if __name__ == "__main__":
    main()