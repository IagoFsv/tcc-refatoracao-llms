from __future__ import annotations

import re
from typing import NamedTuple

PR_PATTERN = re.compile(r".*\(#(\d+)\)")


class Change(NamedTuple):
    """Stores details about commits"""

    full_hash: str
    short_hash: str
    date: str
    version: str
    message: str
    message_without_backticks: str
    pr: str | None


def _get_pr_from_message(message: str) -> str | None:
    pr_match = PR_PATTERN.match(message)
    return pr_match.group(1) if pr_match else None


def _get_change_from_line(line: str, version: str) -> Change:
    split_line = line.split(" ", maxsplit=3)
    message = split_line[3]
    return Change(
        full_hash=split_line[0],
        short_hash=split_line[1],
        date=split_line[2],
        version=version,
        message=message,
        message_without_backticks=message.replace("`", "'").replace("&39;", "'"),
        pr=_get_pr_from_message(message),
    )


def _convert_git_changes_to_table(
    version: str, changes: str, base_url: str, markdown: bool = True
) -> tuple[str, list[Change]]:
    """
    Converts list of changes from its string form to markdown/RST table and array of change information

    The changes are in the form of multiple lines where each line consists of:
    FULL_COMMIT_HASH SHORT_COMMIT_HASH COMMIT_DATE COMMIT_SUBJECT

    The subject can contain spaces but one of the preceding values can, so we can make split
    …
    """
    from tabulate import tabulate

    lines = changes.splitlines()
    headers = ["Commit", "Committed", "Subject"]
    table_data = []
    changes_list: list[Change] = []
    for line in lines:
        if line == "":
            continue
        change = _get_change_from_line(line, version)
        table_data.append(
            (
                f"[{change.short_hash}]({base_url}{change.full_hash})"
                if markdown
                else f"`{change.short_hash} …
