#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#   P A G E B O T  N A N O
#
#   Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#   www.pagebot.io
#   Licensed under MIT conditions
#
#   Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#   backtothecity.py
#
import sys

if __name__ == "__main__":
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.themes.theme import BaseTheme
from pagebotnano_010.toolbox.color import spotColor

class BackToTheCity(BaseTheme):
    """The BackToTheCity theme is ..."""

    NAME = 'Back to the City'
    BASE_COLORS = dict(
        base0=spotColor(476),
        base1=spotColor(1405),
        base2=spotColor(139),
        base3=spotColor(480),
        base4=spotColor(421), # Supporter1
        base5=spotColor(157),
    )

if __name__ == "__main__":
    import doctest
    doctest.testmod()[0]
