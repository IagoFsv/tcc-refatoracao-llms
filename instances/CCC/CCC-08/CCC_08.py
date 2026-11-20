"""Substitution of list elements from two sources and a fallback sequence.

Public entry point: run(subs1, subs2, sources, base). Do not change its name
or signature; the rest of the file may be freely reorganized.
"""

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
  out = [src1[f1] if f1 is not None else src2[f2] if f2 is not None else
         next(base_) for f1, f2, in zip(subs1, subs2)]
  sentinel = object()
  assert next(base_, sentinel) is sentinel
  return out


def run(subs1, subs2, sources, base):
  """Builds the list taking each element from the first source, the second
  source or the base, as the two index lists say; sources is the pair
  (src1, src2). Public entry point of this unit."""
  src1, src2 = sources
  return subs_list2(subs1, subs2, src1, src2, base)
