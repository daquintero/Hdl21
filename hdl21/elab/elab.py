"""
# Elaboration 

Defines the primary `elaborate` method used to flesh out an in-memory `Module` or `Generator`. 
Internally defines and uses a number of hierarchical visitor-classes which traverse the hardware hierarchy, 
performing one or more transformation-passes.  
"""

# Std-Lib Imports
from typing import List, Optional, TypeVar

# Local imports
from .elaboratable import Elaboratable, Elaboratables, is_elaboratable
from .elabpass import ElabPass


ElaboratableType = TypeVar("ElaboratableType", bound=Elaboratables)


def elaborate(
    top: ElaboratableType,
    *,
    passes: Optional[List[ElabPass]] = None,
) -> ElaboratableType:
    """
    # Hdl21 Elaboration

    In-memory elaborates of `Module`s, calls to `Generator`s, and lists thereof.

    Optional `passes` lists the ordered `ElabPass`es to run. By default it runs the order specified by `ElabPass.default`.
    Note the order of passes is important; many depend upon others to have completed before they can successfully run.
    """

    # Expand default values
    passes = passes or ElabPass.default()

    # Check whether we are elaborating a single object or a list thereof
    tops: List[Elaboratable] = top if isinstance(top, List) else [top]

    # Pass `tops` through each of our passes, in order
    for elabpass in passes:
        tops = elabpass.elaborate(tops=tops)

    # Extract the single-element case
    if not isinstance(top, List):
        return tops[0]
    return tops
