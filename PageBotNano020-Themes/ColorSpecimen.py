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
#   ColorSpecimen.py
#
#   This ColorSpecimen.py shows samples of all standard theme colors,
#   with their closest spot color, CMYK, RGB, CSS hex-color and CSS name.
#
from pagebotnano.document import Document
from pagebotnano.themes import AllThemes, BackToTheCity
from pagebotnano.constants import *
from pagebotnano.elements import Rect, Text
from pagebotnano.babelstring import BabelString
from pagebotnano.toolbox import pt

h, w = A4
PADDING = pt(40)
FONT_NAME = 'Verdana'
TITLE_SIZE = 18
LABEL_SIZE = 8
LEADING = 11

doc = Document(w=w, h=h)
for Theme in AllThemes:
    for mood in (DARK, LIGHT):
        theme = Theme(mood=mood)
        page = doc.newPage()
        page.padding = PADDING
        cw = page.pw/len(theme.colors[0]) # Column width
        ch = page.ph/len(theme.colors) # Column height
        for shade in range(len(theme.colors[0])):
            for base in range(len(theme.colors)):
                # Get the color from the theme color matrix and add as rectangle
                c = theme.colors[base][shade]
                e = Rect(x=page.pl+shade*cw, y=page.pb+base*ch, w=cw, h=ch, fill=c)
                page.addElement(e)

                labelStyle = dict(font=FONT_NAME, fontSize=LABEL_SIZE, lineHeight=LEADING, 
                    fill=theme.textColor(base, shade), align=CENTER)
                bs = BabelString('#%s\n%s\nSpot %s\nRAL %s\nColor[%d][%d]' % 
                    (c.hex, c.name.capitalize(), c.spot, c.ral, base, shade), 
                    labelStyle)
                tw, th = bs.textSize
                e = Text(bs, x=page.pl+shade*cw+cw/2, y=page.pb+base*ch+th, w=cw, h=th)
                page.addElement(e)
                
        # Add background rectangle on top with theme name and mood. getColor(shade, base)
        e = Rect(x=page.pl, y=page.h-page.pt, w=page.pw, h=page.pt, fill=theme.getColor(0,2))
        page.addElement(e)
        titleStyle = dict(font=FONT_NAME, fontSize=TITLE_SIZE, fill=theme.getColor(-2,2), indent=20)
        bs = BabelString('%s – %s' % (theme.name, mood), titleStyle)
        tw, th = bs.textSize
        e = Text(bs, x=page.pl, y=page.h-page.pt*2/3)
        page.addElement(e)

doc.export('_export/ColorSpecimen.pdf')

print('Done')