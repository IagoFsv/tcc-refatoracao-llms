"""Table of the commits of a release, in Markdown or reStructuredText.

Public entry point: run(version, changes, base_url, markdown=True). Do not
change its name or signature; the rest of the file may be freely
reorganized.
"""

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


def _get_change_from_line(line: str, version: str) -> Change:
    split_line = line.split(" ", maxsplit=3)
    message = split_line[3]
    pr = None
    pr_match = PR_PATTERN.match(message)
    if pr_match:
        pr = pr_match.group(1)
    return Change(
        full_hash=split_line[0],
        short_hash=split_line[1],
        date=split_line[2],
        version=version,
        message=message,
        message_without_backticks=message.replace("`", "'").replace("&39;", "'"),
        pr=pr,
    )


def _convert_git_changes_to_table(
    version: str, changes: str, base_url: str, markdown: bool = True
) -> tuple[str, list[Change]]:
    """
    Converts list of changes from its string form to markdown/RST table and array of change information

    The changes are in the form of multiple lines where each line consists of:
    FULL_COMMIT_HASH SHORT_COMMIT_HASH COMMIT_DATE COMMIT_SUBJECT

    The subject can contain spaces but one of the preceding values can, so we can make split
    3 times on spaces to break it up.
    :param version: Version from which the changes are
    :param changes: list of changes in a form of multiple-line string
    :param base_url: base url for the commit URL
    :param markdown: if True, Markdown format is used else rst
    :return: formatted table + list of changes (starting from the latest)
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
        if markdown and change.pr:
            table_data.append(
                (
                    f"[{change.short_hash}]({base_url}{change.full_hash})",
                    change.date,
                    f"`{change.message_without_backticks}`",
                )
            )
        else:
            table_data.append(
                (
                    f"`{change.short_hash} <{base_url}{change.full_hash}>`_"
                    if markdown
                    else f"``{change.message_without_backticks}``",
                    change.date,
                    f"`{change.message_without_backticks}`"
                    if markdown
                    else f"``{change.message_without_backticks}``",
                )
            )
        changes_list.append(change)
    header = ""
    if not table_data:
        return header, []
    table = tabulate(table_data, headers=headers, tablefmt="pipe" if markdown else "rst")
    if not markdown:
        header += f"\n\n{version}\n" + "." * len(version) + "\n\n"
        release_date = table_data[0][1]
        header += f"Latest change: {release_date}\n\n"
    return header + table, changes_list


def run(version, changes, base_url, markdown=True):
    """Returns the table and the list of changes. Public entry point of this unit."""
    return _convert_git_changes_to_table(version, changes, base_url, markdown)
