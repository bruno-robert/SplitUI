import logging
from enum import Enum, unique

from dearpygui.core import *
from dearpygui.simple import *


@unique
class Panes(Enum):
    """
    This enum stores the names of important widgets such as tabs or reusable windows
    """
    # The main window panels
    left = "Left panel"
    center = "Middle panel"
    right = "Right panel"


class SplitUi:
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

        # list of items to be centered on each resize
        center_items = []
        add_data('item_center_list', center_items)
        set_render_callback(self._apply_centering)

        self.__init_main_window()

    @staticmethod
    def _apply_centering():
        """
        Centers all the items in the item_center_list. this function is usually caleld to refresh the centering
        when the window is resized.
        :return:
        """
        items = list(get_data("item_center_list"))
        if not items:
            return
        for item in items:
            if not does_item_exist(item):  # if the item no longer exists, remove it
                items.remove(item)
                add_data('item_center_list', items)
                continue
            container_width = get_item_rect_size(get_item_parent(item))[0]
            item_width, item_height = get_item_rect_size(item)
            set_item_height(f'{item}_container', int(item_height))
            pos = int((container_width / 2) - (item_width / 2))
            set_item_width(f'{item}_dummy', pos)

    @staticmethod
    def _center_item(name: str):
        """
        Centers a widget by creating a parent for it and making the item centered in the parent
        :param name: id of the widget to center
        :return:
        """
        with child(f'{name}_container', autosize_x=True, no_scrollbar=True, border=False):
            add_dummy(name=f'{name}_dummy')
            add_same_line(name=f'{name}_sameline')
            move_item(name, parent=f'{name}_container')
        items = list(get_data('item_center_list'))
        items.append(name)
        add_data('item_center_list', items)
        y_space = get_style_item_spacing()[1]
        set_item_style_var(f'{name}_container', mvGuiStyleVar_ItemSpacing, [0, y_space])

    @staticmethod
    def _clear_widget(panel: Panes):
        """
        Clears a panel by deleting all it's children.
        :param panel:
        """
        delete_item(panel.value, children_only=True)

    def __resize_windows(self, sender, data):
        """
        This function is called every time the window is resized and when the application starts.
        This function handles the size of the 3 panels that constitute the application.
        The left and right panels are fixed size and the center panel scales as wide and high as possible.

        The sender and data parameters are here because this function is a dearpygui callback.
        :param sender:
        :param data:
        :return:
        """
        width_main_window = get_main_window_size()[0]
        height_panels = get_main_window_size()[1] - 60  # get_item_height('Main') - y_pos_panels
        y_pos_panels = get_item_height('Main menu')

        x_pos_left_panel = 0

        if self.panes == 1:
            set_window_pos(Panes.left.value, x=x_pos_left_panel, y=y_pos_panels)
            set_item_width(Panes.left.value, width=width_main_window)
            set_item_height(Panes.left.value, height=height_panels)
        if self.panes == 2:
            panel_width = int(width_main_window / 2)
            # Left panel
            set_window_pos(Panes.left.value, x=x_pos_left_panel, y=y_pos_panels)
            set_item_width(Panes.left.value, width=panel_width)
            set_item_height(Panes.left.value, height=height_panels)

            x_pos_right_panel = x_pos_left_panel + panel_width
            # Right panel
            set_window_pos(Panes.right.value, x=x_pos_right_panel, y=y_pos_panels)
            set_item_width(Panes.right.value, width=panel_width)
            set_item_height(Panes.right.value, height=height_panels)
        elif self.panes == 3:
            width_left_panel = 300
            width_middle_panel = int((width_main_window - width_left_panel) / 2)
            width_right_panel = int((width_main_window - width_left_panel) / 2)
            x_pos_middle_panel = x_pos_left_panel + width_left_panel
            x_pos_right_panel = x_pos_middle_panel + width_middle_panel

            # Left panel
            set_window_pos(Panes.left.value, x=x_pos_left_panel, y=y_pos_panels)
            set_item_width(Panes.left.value, width=width_left_panel)
            set_item_height(Panes.left.value, height=height_panels)

            # Middle panel
            set_window_pos(Panes.center.value, x=x_pos_middle_panel, y=y_pos_panels)
            set_item_width(Panes.center.value, width=width_middle_panel)
            set_item_height(Panes.center.value, height=height_panels)

            # Right panel
            set_window_pos(Panes.right.value, x=x_pos_right_panel, y=y_pos_panels)
            set_item_width(Panes.right.value, width=width_right_panel)
            set_item_height(Panes.right.value, height=height_panels)

    def __init_main_window(self):
        """
        Initialises the main window:
        - Creates the window menu
        - Creates the 3 pane layout
        - Sets up the resize callbacks

        This function is called at the end of the __init__() function, once most of the app is initialised
        :return:
        """
        with window("Main"):
            # Create the menu
            with menu_bar('Main menu'):
                with menu('File'):
                    add_menu_item('Preferences')
                with menu('Edit'):
                    add_menu_item('Item 1##Edit')
                with menu('Help'):
                    add_menu_item('About')

        with window(Panes.left.value, autosize=False, no_resize=True, no_title_bar=True, no_move=True,
                    no_scrollbar=True,
                    no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True,
                    no_bring_to_front_on_focus=False,
                    no_close=True, no_background=False, show=True):
            add_text('left')
            pass

        if self.panes == 3:
            with window(Panes.center.value, autosize=False, no_resize=True, no_title_bar=True, no_move=True,
                        no_scrollbar=True,
                        no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True,
                        no_bring_to_front_on_focus=False,
                        no_close=True, no_background=False, show=True):
                add_text('center')
                pass

        if self.panes >= 2:
            with window(Panes.right.value, autosize=False, no_resize=True, no_title_bar=True, no_move=True,
                        no_scrollbar=True,
                        no_collapse=True, horizontal_scrollbar=False, no_focus_on_appearing=True,
                        no_bring_to_front_on_focus=False,
                        no_close=True, no_background=False,
                        show=True):  # no_background=False --> set to True to remove lines around window
                add_text('right')
                pass
        set_start_callback(self.__resize_windows)
        set_resize_callback(self.__resize_windows)

    def start(self):
        """
        Starts the app

        This function should be called after __init__()
        :return:
        """
        start_dearpygui(primary_window="Main")

    def _get_uid(self):
        """
        Returns a unique ID that can be used to create unique element names. The ID is only unique to the object
        instance and should not be used outside of the instance itself.
        :return: A array of unique IDs [window title, top copy button id, bottom copy button id]
        """
        uid = self.current_uid
        self.current_uid += 1
        return uid

