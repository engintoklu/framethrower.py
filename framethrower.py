# This is the framethrower.py library
# Nihat Engin Toklu < http://github.com/engintoklu >, 2015

#################
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
#################

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

def is_string_data(x):
    return type(x) in [type(""), type(u"")]

BY_ORIENT = "BY_ORIENT"

default_stickies = [
    (tk.Label, tk.W + tk.N),
    (tk.Button, ""),
    (tk.Scrollbar, BY_ORIENT)]

def get_default_sticky(widget):
    global default_stickies
    for widget_type, sticky in default_stickies:
        if isinstance(widget, widget_type):
            if sticky == BY_ORIENT:
                if widget["orient"] == tk.VERTICAL:
                    return tk.N + tk.S
                else:
                    return tk.W + tk.E
            else:
                return sticky
    return tk.N + tk.S + tk.W + tk.E

class GridFrame(tk.Frame):
    """GridFrame is a class which extends Frame of tkinter.
    It is designed to quickly place widgets in a tabular fashion."""
    def __init__(self, *args, **opts):
        tk.Frame.__init__(self, *args, **opts)

    def put(self, table, rowweights=None, colweights=None):
        """Put the widgets specified within table in a tabular fashion.

        table is a sequence of sequence of tkinter widgets.
        For example, it can be a list of list of widgets like this:
            [ [widget1, widget2],     # row1
              [widget3, widget4] ]    # row2
        If, instead of a widget, a string is given,
        then a tkinter Label is automatically created and placed
        in that cell. If, instead of a widget, None is given,
        that cell is left empty.

        rowweights and colweights are sequences of numbers.
        Each number specify how much a widget in a row/column should
        grow vertically/horizontally when the GridFrame itself grows.
          0 means row/column should not grow
          1 means row/column will grow
          2 means row/column will grow
             twice as much compared to the ones with 1
          ...
        """
        rowindex = 0
        colindex = 0
        for row in table:
            colindex = 0
            for widget in row:
                if not (widget is None):
                    if is_string_data(widget):
                        widget = tk.Label(text=widget, master=self)
                    widget.grid(row=rowindex,
                                column=colindex,
                                sticky=get_default_sticky(widget))
                colindex += 1
            rowindex += 1

        if not (rowweights is None):
            i = 0
            for weight in rowweights:
                self.grid_rowconfigure(i, weight=weight)
                i += 1

        if not (colweights is None):
            j = 0
            for weight in colweights:
                self.grid_columnconfigure(j, weight=weight)
                j += 1

class ScrollingFrame(tk.Frame):
    """A Frame which automatically attaches scrollbars to the widget contained"""
    def __init__(self, *args, **opts):
        """Initialize the ScrollingFrame instance.
        As keyword argument, if you specify:
          orient=tkinter.HORIZONTAL, a horizontal scrollbar is attached;
          orient=tkinter.VERTICAL, a vertical scrollbar is attached;
          orient="", both vertical and horizontal scrollbars are attached;
          orient=None, same as above.
          orient=tkinter.BOTH, same as above.
          orient=tkinter.ALL, same as above.
        Other arguments/options are passed directly to the superclass
        (which is tkinter.Frame).
        """
        orient = None
        rest_opts = {}
        for opt in opts:
            if opt == "orient":
                orient = opts["orient"]
            else:
                rest_opts[opt] = opts[opt]

        has_vscroller = True
        has_hscroller = True
        if orient == tk.HORIZONTAL:
            has_vscroller = False
        elif orient == tk.VERTICAL:
            has_hscroller = False
        elif orient is None or orient in ("", tk.ALL, tk.BOTH):
            pass
        else:
            raise ValueError("Unexpected value is given for orient attribute: " + repr(orient))

        tk.Frame.__init__(self, *args, **rest_opts)

        if has_hscroller:
            self.hscroller = tk.Scrollbar(master=self, orient=tk.HORIZONTAL)
            self.hscroller.grid(row=1, column=0, sticky=tk.W+tk.E)

        if has_vscroller:
            self.vscroller = tk.Scrollbar(master=self, orient=tk.VERTICAL)
            self.vscroller.grid(row=0, column=1, sticky=tk.N+tk.S)

        self.__has_hscroller = has_hscroller
        self.__has_vscroller = has_vscroller

    def contain(self, widget):
        """Contain the widget for which the scrollbars will be attached"""
        if self.__has_vscroller:
            widget["yscrollcommand"] = self.vscroller.set
            self.vscroller["command"] = widget.yview
        if self.__has_hscroller:
            widget["xscrollcommand"] = self.hscroller.set
            self.hscroller["command"] = widget.xview
        widget.grid(row=0, column=0, sticky=get_default_sticky(widget))
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

def test1():
    class MyMainWindow:
        def __init__(self):
            self.root = tk.Tk()
            self.table = GridFrame(master=self.root)

            self.entry1 = tk.Entry(master=self.table)

            self.textscroller = ScrollingFrame(master=self.table)
            self.text1 = tk.Text(master=self.textscroller)
            self.textscroller.contain(self.text1)

            self.button1 = tk.Button(master=self.table, text="Test")

            self.table.put(
                [["Here is an Entry:"        , self.entry1],
                 ["Here is a scrolled Text:" , self.textscroller],
                 [None                       , self.button1]],
                rowweights=[0, 1, 0],
                colweights=[0, 1])

            self.table.place(x=0, y=0, relwidth=1, relheight=1)

        def show(self):
            self.root.mainloop()

    mywin = MyMainWindow()
    mywin.show()

if __name__ == "__main__":
    test1()
