# framethrower.py

Nihat Engin Toklu < http://github.com/engintoklu >, 2015

## What is framethrower.py

This is a very simple Python library which extends the tkinter library
with the following widgets:

* GridFrame: a frame which makes it easier to order its contained widgets according to a grid layout
* ScrollingFrame: a frame which makes it easier to bind scrollbars to its contained widget

You can use the framethrower.py library from your Python program by simply
putting the file `framethrower.py` in the same directory with your
Python code file, and then by using the following import line:

    import framethrower as ft

You can also use `tkinter` itself with the help of framethrower.py if you wish:

    import framethrower as ft
    tk = ft.tk

I have tested the framethrower.py library with Python 2.7, Python 3.4, and PyPy 4.

## GridFrame

To have an area in your `tkinter` window where the widgets are ordered according
to a grid layout, you can use `GridFrame`.
It is a subclass of `tkinter.Frame`, only with an additional member function
named `put`.

Here is how it is defined:

    class GridFrame(tk.Frame):
        ...
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

## ScrollingFrame

To bind scrollbar(s) to a widget,
you can place that widget within a `ScrollingFrame`.
First, the `ft.ScrollingFrame` instance is initialized:

    myscroller = ft.ScrollingFrame(master=mywindow, orient=tk.VERTICAL)
    # orient=tk.VERTICAL means we want a vertical scrollbar attached
    # we could say orient=tk.HORIZONTAL if we wanted a horizontal scrollbar
    # or orient=tk.BOTH if we wanted both types of scrollbars
    # if orient is not specified, it defaults to tk.BOTH

Then, we initialize the widget for which we want attached scrollbars,
with the `ft.ScrollingFrame` as its master.
For example, it could be a `tk.Text`:

    mytext = ft.Text(master=myscroller, ...)

Finally, we say:

    myscroller.contain(mytext)

## An example

Here is an example Python code which demonstrates the usage of the
`framethrower.py` library:

    import framethrower as ft
    tk = ft.tk

    class MyMainWindow:
        def __init__(self):
            self.root = tk.Tk()
            self.table = ft.GridFrame(master=self.root)

            self.entry1 = tk.Entry(master=self.table)

            self.textscroller = ft.ScrollingFrame(master=self.table)
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

## License

I, Nihat Engin Toklu, put the `framethrower.py` library into the public domain,
by using the following unlicense statement:

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

    For more information, please refer to <http://unlicense.org/>
