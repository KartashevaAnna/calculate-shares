from write_to_excel import write_to_excel
from write_to_txt_file import write_to_txt_file
from typing import Dict, List
from to_ignore_by_git.all_shares import ALL_SHARES
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


if __name__ == "__main__":
    resulting_shares = know_shares(ALL_SHARES)
    write_to_txt_file(resulting_shares)
    write_to_excel(resulting_shares)
