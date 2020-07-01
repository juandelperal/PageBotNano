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
#   codeblock.py
#
#   This source contains the class with knowledge about elements that
#   can be placed on a page.
#
import sys
import drawBot

if __name__ == '__main__':
    sys.path.insert(0, "../..") # So we can import pagebotnano without installing.

from pagebotnano_010.babelstring import BabelString
from pagebotnano_010.elements import Text
from pagebotnano_010.toolbox.color import noColor, color

class CodeBlock(Text):

    DEFAULT_CODE_STYLE = dict(font='Courier', fontSize=9, textFill=0.2, textStroke=noColor)

    isText = False # It's not a normal text box, even while inheriting functionnally from Text

    def __init__(self, code, tryExcept=True, fill=None, style=None, **kwargs):
        if fill is None:
            fill = color(0.9)
            if style is None:
                style = self.DEFAULT_CODE_STYLE
        # Use a Text to store the code on the parent galley.
        bs = BabelString(code, style)
        Text.__init__(self, bs, fill=fill, **kwargs)
        assert isinstance(code, str)
        self.code = code
        self.tryExcept = False# tryExcept

    def __repr__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.code.replace('\n',';')[:200])

    def build(self, view, origin, drawElements=True, **kwargs):
        """Run the code block. If the view.showSourceCode is True, then just export the code
        for debugging."""
        if not view.showSourceCode:
            self.run()
        else:
            Text.build(self, view, origin, drawElements, **kwargs)

    def run(self, targets=None, verbose=False):
        """Execute the code block. Answer a set of compiled methods, as found in the <code class="Python">...</code>,
        made by Markdown with
        ~~~
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        ~~~
        block code. In this case the MacDown and MarkDown extension libraries
        convert this codeblock to
        <pre><code>
        cid = 'NameOfBlock'
        doc = Document(w=300, h=500)
        </code></pre>
        This way authors can run PageBot generators controlled by content.
        Note that it is the author's responsibility not to overwrite global values
        that are owned by the calling composer instance.

        >>> from pagebotnano_010.document import Document
        >>> doc = Document(w=500, h=500)
        >>> page = doc.newPage()
        >>> code = 'a = 100 * 300\\npage = doc.newPage()\\npage.w = 300'
        >>> cb = CodeBlock(code, x=0, y=0, tryExcept=False)
        >>> page.addElement(cb)
        >>> cb
        <CodeBlock:a = 100 * 300;page = doc.newPage();page.w = 300>
        >>> # Create globals dictionary for the script to work with
        >>> g = dict(page=page, doc=doc)
        >>> result = cb.run(g) # Running the code selects 3 pages ahead
        >>> result is g # Result global dictionary is same object as g
        True
        >>> sorted(result.keys())
        ['__code__', 'a', 'doc', 'page']
        >>> resultPage = result['page']
        >>> resultPage # Running code block changed width of new selected page.
        <Page pn=2 w=300 h=500 elements=0>
        >>> resultPage.w, resultPage.pn
        (300, 2)
        >>> cb.code = 'aa = 200 * a' # Change code of the code block, using global
        >>> result = cb.run(g) # And run with the same globals dictionary
        >>> sorted(result.keys()), g['aa'] # Result is added to the globals
        (['__code__', 'a', 'aa', 'doc', 'page'], 6000000)
        """
        if targets is None:
            # If no globals defined, create a new empty dictionary as storage of result
            # and try to fill it in case we are part of a page, e.g. for debugging.
            targets = {}
            doc = self.doc
            if doc is not None:
                targets['doc'] = doc
        if not self.tryExcept: # For debugging show full error of code block run.
            exec(self.code, targets) # Execute code block, where result goes dict.
            if '__builtins__' in targets:
                del targets['__builtins__'] # We don't need this set of globals in the returned results.
        else:
            error = None
            try:
                exec(self.code, targets) # Execute code block, where result goes dict.
                if '__builtins__' in targets:
                    del targets['__builtins__'] # We don't need this set of globals in the results.
            except TypeError:
                error = 'TypeError'
            except NameError:
                error = 'NameError'
            except SyntaxError:
                error = 'SyntaxError'
            except AttributeError:
                error = 'AttributeError'
            except:
                error = 'Unknown Error'
            targets['__error__'] = error
            if error is not None:
                print(u'### %s ### %s' % (error, self.code))
            # TODO: insert more possible exec() errors here.

        # For convenience, store the last source code of the block in the result dict.
        if '__code__' not in targets:
            targets['__code__'] = self.code

        return targets # Answer the globals attribute, in case it was created.

if __name__ == '__main__':
    import doctest
    doctest.testmod()[0]
