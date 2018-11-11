# This is the framethrower.py library
# Nihat Engin Toklu < http://github.com/engintoklu >, 2018

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


def make_sure_widget(x, master):
    if is_string_data(x):
        return tk.Label(text=x, master=master)
    else:
        return x


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


class GridCell(object):
    """A GridCell represents a cell within a GridFrame.
    A GridCell instance can be used instead of a regular widget
    with the put() method of a GridFrame,
    so that the behavior of that GridFrame cell is configured.
    See also the __init__() method's documentation.
    """

    def __init__(self,
                 widget,
                 grow_vertically=False,
                 grow_horizontally=False,
                 min_width=None,
                 min_height=None,
                 sticky=None):
        """Initialize the GridCell instance.

        Arguments:

        widget
            Expected as a tkinter widget or an str.
            If given as an str, it is assumed that the cell
            will contain a tkinter Label widget with the specified
            text.
            Otherwise, if given as a tkinter widget,
            the cell contains the specified widget.

        grow_vertically
            Expected as bool.
            If set as True, the cell grows vertically
            with the GridFrame.

        grow_horizontally
            Expected as bool.
            If set as True, the cell grows horizontally
            with the GridFrame.

        min_width
            Expected as None, or as an int.
            An integer given here specifies the minimum allowed
            width of the cell.

        min_height
            Expected as None, or as an int.
            An integer given here specifies the minimum allowed
            height of the cell.

        sticky
            Expected as None, or an str.
            The string should be a combination of the following characters:
            'n' for north, 's' for south, 'e' for east, 'w' for west.
            Specifies in which directions the widget will be stretched
            as the size of the cell changes.
        """
        self.widget = widget
        self.grow_vertically = grow_vertically
        self.grow_horizontally = grow_horizontally
        self.min_width = min_width
        self.min_height = min_height
        self.sticky = sticky

    def _put_into_grid(self, grid, rowindex, colindex):
        widget = make_sure_widget(self.widget, grid)
        if self.sticky is not None:
            sticky = self.sticky
        else:
            sticky = get_default_sticky(widget)
        widget.grid(row=rowindex, column=colindex, sticky=sticky)
        if self.grow_vertically:
            grid.grid_rowconfigure(rowindex, weight=1)
        if self.grow_horizontally:
            grid.grid_columnconfigure(colindex, weight=1)
        if self.min_height is not None:
            grid.grid_rowconfigure(rowindex, minsize=self.min_height)
        if self.min_width is not None:
            grid.grid_columnconfigure(colindex, minsize=self.min_width)


class GridFrame(tk.Frame):
    """GridFrame is a class which extends Frame of tkinter.
    It is designed to quickly place widgets in a tabular fashion."""
    def __init__(self, *args, **opts):
        tk.Frame.__init__(self, *args, **opts)

    def put(self, *table):
        """Put the widgets specified within table in a tabular fashion.

        table is a sequence of sequence of tkinter widgets,
        to be passed as an argument list.
        For example, the put method of a GridFrame gf can be called like this:

        gf.put(
            [widget1, widget2],     # row1
            [widget3, widget4]      # row2
        )

        Instead of a widget:
        - If a string is given,
          then a tkinter Label is automatically created and placed
          in that cell.
        - If None is given, that cell is left empty.
        - If a GridCell instance is given, the widget contained by
          that GridCell instance is placed into the grid,
          and the cell is configured according to the attributes
          specified by that GridCell instance.
        """
        rowindex = 0
        colindex = 0
        for row in table:
            colindex = 0
            for widget in row:
                if widget is not None:
                    if isinstance(widget, GridCell):
                        widget._put_into_grid(self, rowindex, colindex)
                    else:
                        widget = make_sure_widget(widget, self)
                        widget.grid(row=rowindex,
                                    column=colindex,
                                    sticky=get_default_sticky(widget))
                colindex += 1
            rowindex += 1


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


class ButtonFrame(tk.Frame):
    """A Frame which is used to contain horizontally ordered command buttons"""

    def __init__(self, **opts):
        """Initialize the ButtonFrame.
        All initialization options are directly passed to the
        initialization procedure of the tkinter.Frame class"""

        tk.Frame.__init__(self, **opts)

    def put(self, *buttons):
        """Create and put buttons with the specified
        label texts and callback functions.
        buttons is a list of pairs, to be given as an argument list.

        For example, the put() method of a ButtonFrame bf can be called
        like this:
        bf.put(
            (button1LabelString, button1CallbackFunction),
            (button2LabelString, button2CallbackFunction),
            ...
            (buttonNLabelString, buttonNCallbackFunction),
        )
        """

        for (text, command) in buttons:
            tk.Button(master=self, text=text, command=command).pack(
                side=tk.LEFT)


default_stickies.append((ButtonFrame, ""))


def demo1():
    try:
        import tkMessageBox as tkmsg
    except ImportError:
        import tkinter.messagebox as tkmsg

    class MyMainWindow(object):
        def new_click(self):
            tkmsg.showinfo("Info", "Clicked on 'New'")

        def open_click(self):
            tkmsg.showinfo("Info", "Clicked on 'Open'")

        def __init__(self):
            self.root = tk.Tk()
            self.table = GridFrame(master=self.root)

            self.commands = ButtonFrame(master=self.table)
            self.commands.put(
                ("New", self.new_click),
                ("Open", self.open_click)
            )

            self.entry1 = tk.Entry(master=self.table)

            self.textscroller = ScrollingFrame(master=self.table)
            self.text1 = tk.Text(master=self.textscroller)
            self.textscroller.contain(self.text1)

            self.button1 = tk.Button(master=self.table, text="Test")

            self.table.put(
                [
                    None,
                    self.commands
                ],
                [
                    "Here is an Entry:",
                    GridCell(
                        self.entry1,
                        grow_horizontally=True,
                        min_width=200
                    )
                ],
                [
                    "Here is a scrolled Text:" ,
                    GridCell(
                        self.textscroller,
                        grow_horizontally=True,
                        grow_vertically=True
                    )
                ],
                [
                    None,
                    self.button1
                ]
            )

            self.table.place(x=0, y=0, relwidth=1, relheight=1)
            self.root.geometry("640x480")

        def show(self):
            self.root.mainloop()

    mywin = MyMainWindow()
    mywin.show()

if __name__ == "__main__":
    demo1()
