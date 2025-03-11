from typing import Dict, List


def write_to_txt_file(resulting_shares: List[Dict[str, int]]):
    with open("to_ignore_by_git/RESULT.txt", "w+", encoding="utf-8") as f:
        for record in resulting_shares:
            f.write(str(record) + "\n")
