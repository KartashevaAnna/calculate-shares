import xlsxwriter
from typing import Dict, List
from all_shares import ALL_SHARES
from pydantic import (
    BaseModel,
    computed_field,
)

DIVISOR = 5  # количество наследников


class Share(BaseModel):
    total_shares: int

    @computed_field
    @property
    def divided(cls) -> int:
        """Cколько акций получает каждый наследник."""
        return cls.total_shares // DIVISOR

    @computed_field
    @property
    def to_split_after_withdrawal(cls) -> int:
        """Cколько акций нужно снять и поделить на пятерых после получения в банке."""
        return cls.total_shares % DIVISOR

    @computed_field
    @property
    def maximum_shares_inherited(cls) -> int:
        """Cколько акций получает тот, кто забирает не делящиеся на 5 акции."""

        return cls.divided + cls.to_split_after_withdrawal


def know_shares(shares_list: List[Dict[str, int]]):
    result = []
    for share in shares_list:
        share_name = list(share.keys())[0]
        each_share = Share(total_shares=share[share_name])
        pretty_dict = {}
        pretty_dict["название"] = share_name
        pretty_dict["всего акций"] = each_share.total_shares
        pretty_dict["акций каждому"] = each_share.divided
        pretty_dict["акций Ане"] = each_share.maximum_shares_inherited
        pretty_dict["разделить после получения"] = each_share.to_split_after_withdrawal
        result.append(pretty_dict)
    return result


def write_to_file(resulting_shares: List[Dict[str, int]]):
    with open("RESULT.txt", "w+", encoding="utf-8") as f:
        for record in resulting_shares:
            f.write(str(record) + "\n")


def write_to_excel(resulting_shares: List[Dict[str, int]]):
    workbook = xlsxwriter.Workbook("RESULT.xlsx")
    worksheet = workbook.add_worksheet()

    row = 0
    column = 0
    col_names = [
        "Название",
        "Всего акций",
        "Акций каждому",
        "Акций Ане",
        "Разделить после получения",
    ]
    for name in col_names:
        worksheet.write(row, column, name)
        column += 1
    for item in resulting_shares:
        column = 0
        row += 1
        for key in item:
            worksheet.write(row, column, item[key])
            column += 1
    worksheet.autofit()
    workbook.close()


if __name__ == "__main__":
    resulting_shares = know_shares(ALL_SHARES)
    write_to_file(resulting_shares)
    write_to_excel(resulting_shares)
