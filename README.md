This is a personal Library I use to create split pane windows in [dearpygui](https://github.com/hoffstadt/DearPyGui).
Now works with dearpygui 0.8.x

It's usage is simple:
```python
from SplitUi import SplitUi


class InitialLoader(SplitUi):
    def __init__(self):
        super().__init__(panes=2)  # panes must be either 1, 2 or 3

il = InitialLoader()
il.start()
```

simply create a child class of SplitUI and initialize it with panes = 1, 2 or 3.
If not panes parameter is passed, it defaults to 3 panes.
