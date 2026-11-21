from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")

def subs_list2(
    subs1: Sequence[int | None], subs2: Sequence[int | None],
    src1: Sequence[T], src2: Sequence[T], base: Sequence[T],
) -> list[T]:
  assert len(subs1) == len(subs2)
  base_ = iter(base)
  out = []
  for f1, f2 in zip(subs1, subs2):
    if f1 is not None:
      out.append(src1[f1])
    elif f2 is not None:
      out.append(src2[f2])
    else:
      out.append(next(base_))
  sentinel = object()
  assert next(base_, sentinel) is sentinel
  return out


def run(subs1, subs2, sources, base):
  """Builds the list taking each element from the first source, the second
  source or the base, as the two index lists say; sources is the pair
  (src1, src2). Public entry point of this unit."""
  src1, src2 = sources
  return subs_list2(subs1, subs2, src1, src2, base)
