import logging
from typing import TypedDict

import dearpygui.dearpygui as dpg


class SplitUi:
    """
    Creates a dearpygui basic setup with 1, 2 or 3 panes layout
    """

    def __init__(self, panes=3, logger=logging.getLogger(__name__)):
        """
        Initialises polybiblioglot. Creates the Translator and Converter objects,
        initialises the main window
        :param panes: number of panes to use (integer between 1 and 3)
        :param logger:
        """
        self.panes = panes if 0 < panes <= 3 else 3
        self.logger = logger
        self.current_uid = 0

        self.Widgets = TypedDict('Widgets', {
            'mainWindow': int,
            'left': int,
            'center': int,
            'right': int,
            'menuBar': int
        })

        # list of items to be centered on each resize
        self.center_items = []

        self.__init_main_window()

    def __resize_windows(self):
        """
        This function is called every time the window is resized and when the application starts.
        This function handles the size of the 3 panels that constitute the application.
        The left and right panels are fixed size and the center panel scales as wide and high as possible.

        The sender and data parameters are here because this function is a dearpygui callback.
        :return:
        """
        width_main_window = dpg.get_item_width(self.Widgets.mainWindow)
        y_pos_panels = dpg.get_item_height(self.Widgets.menuBar)
        height_panels = dpg.get_item_height(self.Widgets.mainWindow) - y_pos_panels

        x_pos_left_panel = 0

        if self.panes == 1:
            dpg.set_item_pos(self.Widgets.left, [x_pos_left_panel, y_pos_panels])
            dpg.set_item_width(self.Widgets.left, width=width_main_window)
            dpg.set_item_height(self.Widgets.left, height=height_panels)
        if self.panes == 2:
            panel_width = int(width_main_window / 2)
            # Left panel
            dpg.set_item_pos(self.Widgets.left, [x_pos_left_panel, y_pos_panels])
            dpg.set_item_width(self.Widgets.left, width=panel_width)
            dpg.set_item_height(self.Widgets.left, height=height_panels)

            x_pos_right_panel = x_pos_left_panel + panel_width
            # Right panel
            dpg.set_item_pos(self.Widgets.right, [x_pos_right_panel, y_pos_panels])
            dpg.set_item_width(self.Widgets.right, width=panel_width)
            dpg.set_item_height(self.Widgets.right, height=height_panels)
        elif self.panes == 3:
            width_left_panel = 300
            width_middle_panel = int((width_main_window - width_left_panel) / 2)
            width_right_panel = int((width_main_window - width_left_panel) / 2)
            x_pos_middle_panel = x_pos_left_panel + width_left_panel
            x_pos_right_panel = x_pos_middle_panel + width_middle_panel

            # Left panel
            dpg.set_item_pos(self.Widgets.left, [x_pos_left_panel, y_pos_panels])
            dpg.set_item_width(self.Widgets.left, width=width_left_panel)
            dpg.set_item_height(self.Widgets.left, height=height_panels)

            # Middle panel
            dpg.set_item_pos(self.Widgets.center, [x_pos_middle_panel, y_pos_panels])
            dpg.set_item_width(self.Widgets.center, width=width_middle_panel)
            dpg.set_item_height(self.Widgets.center, height=height_panels)

            # Right panel
            dpg.set_item_pos(self.Widgets.right, [x_pos_right_panel, y_pos_panels])
            dpg.set_item_width(self.Widgets.right, width=width_right_panel)
            dpg.set_item_height(self.Widgets.right, height=height_panels)

    def __init_main_window(self):
        """
        Initialises the main window:
        - Creates the window menu
        - Creates the 3 pane layout
        - Sets up the resize callbacks

        This function is called at the end of the __init__() function, once most of the app is initialised
        :return:
        """
        with dpg.window(label="Main") as self.Widgets.mainWindow:
            # Create the menu
            with dpg.menu_bar() as self.Widgets.menuBar:
                pass

            with dpg.window(autosize=False, no_resize=True, no_title_bar=True, no_move=True,
                            no_scrollbar=True,
                            no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True,
                            no_bring_to_front_on_focus=False,
                            no_close=True, no_background=False, show=True) as self.Widgets.left:
                pass

            if self.panes == 3:
                with dpg.window(autosize=False, no_resize=True, no_title_bar=True, no_move=True,
                                no_scrollbar=True,
                                no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True,
                                no_bring_to_front_on_focus=False,
                                no_close=True, no_background=False, show=True) as self.Widgets.center:
                    pass

            if self.panes >= 2:
                with dpg.window(autosize=False, no_resize=True, no_title_bar=True, no_move=True,
                                no_scrollbar=True,
                                no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True,
                                no_bring_to_front_on_focus=False,
                                no_close=True, no_background=False,
                                show=True) as self.Widgets.right:
                    # no_background=False --> set to True to remove lines around window
                    pass
        dpg.set_start_callback(self.__resize_windows)
        dpg.add_resize_handler(parent=self.Widgets.mainWindow, callback=self.__resize_windows)

    def start(self):
        """
        Starts the app

        This function should be called after __init__()
        :return:
        """
        dpg.set_primary_window(self.Widgets.mainWindow, True)
        dpg.start_dearpygui()
