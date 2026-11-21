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
    split_line = line.split("  ", maxsplit=3)
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
    𝑛 times on spaces to break it up.
    :param version: Version from which the changes are
    :param changes: list of changes in a form of multiple-line string
    :param base_url: base url for the commit URL
    :param markdown: if True, Markdown format is used else rst
    :return: formatted table 𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛𝑛
