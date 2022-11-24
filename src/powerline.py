# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# MY CODE ==================================================
from collections import namedtuple


# https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim
GRUVBOX = {
    "dark0_hard": "#1d2021",
    "dark0": "#282828",
    "dark0_soft": "#32302f",
    "dark1": "#3c3836",
    "dark2": "#504945",
    "dark3": "#665c54",
    "dark4": "#7c6f64",
    "dark4_256": "#7c6f64",
    "gray_245": "#928374",
    "gray_244": "#928374",
    "light0_hard": "#f9f5d7",
    "light0": "#fbf1c7",
    "light0_soft": "#f2e5bc",
    "light1": "#ebdbb2",
    "light2": "#d5c4a1",
    "light3": "#bdae93",
    "light4": "#a89984",
    "light4_256": "#a89984",
    "bright_red": "#fb4934",
    "bright_green": "#b8bb26",
    "bright_yellow": "#fabd2f",
    "bright_blue": "#83a598",
    "bright_purple": "#d3869b",
    "bright_aqua": "#8ec07c",
    "bright_orange": "#fe8019",
    "neutral_red": "#cc241d",
    "neutral_green": "#98971a",
    "neutral_yellow": "#d79921",
    "neutral_blue": "#458588",
    "neutral_purple": "#b16286",
    "neutral_aqua": "#689d6a",
    "neutral_orange": "#d65d0e",
    "faded_red": "#9d0006",
    "faded_green": "#79740e",
    "faded_yellow": "#b57614",
    "faded_blue": "#076678",
    "faded_purple": "#8f3f71",
    "faded_aqua": "#427b58",
    "faded_orange": "#af3a03",
}

GRUVBOX = {
    # key: hex color
    "bg": "#282828",
    "bg0_h": "#1d2021",
    "bg1": "#3c3836",
    "bg2": "#504945",
    "bg3": "#665c54",
    "bg4": "#7c6f64",
    "fg": "#ebdbb2",
    "bg0_s": "#32302f",
    "red": "#fb4934",
    "green": "#b8bb26",
    "yellow": "#fabd2f",
    "blue": "#83a598",
    "purple": "#d3896b",
    "aqua": "#8ec07c",
    "gray": "#a89984",
    "orange": "#fe8019",
}
COLORS = {
    "pink": "#D97E96",
    "magenta": "#A36584",
    "purple": "#635373",
    "blue": "#496886",
    "slate": "#152B42",
    "gray": "#1A2133",
    "black": "#000000",
}
GRADIENT = {
    4: "#FCE2DB",
    3: "#FF8FB1",
    2: "#B270A2",
    1: "#7A4495",
    # 0: "#152B42",
}
GRADIENT2 = {
    0: GRUVBOX["bg0_h"],
    1: "#5B6153",
    2: "#9C9E93",
    3: GRUVBOX["fg"],
    4: "#D17F98",
    #    5: "#B1415E"
}
GRADIENT3 = {
    0: GRUVBOX["bg0_h"],
    1: GRUVBOX["bg2"],
    2: GRUVBOX["bg4"],
    3: "#DEBFCD",
    4: "#dda2b2",
    # cf7d93
    5: "#cf7d93",
    #    6: "#b1415e", # don't like this one
}
SYMBOLS = {
    # str: str
    "left-circle": "\ue0b6",
    "right-circle": "\ue0b4",
    "left-triangle": "◀",
    "right-triangle": "▶",
    "square": "■",
    "brightness": "\ufaa7 ",
    "cpu": "\uf2db",
    "thermometer": "\uf2c7",
    "degrees": "°",
    "swap": "",
    "power": "\uf011 ",
}
VOLUME_COMMANDS: {str: str} = {
    # str: str
    "up": "sh -c 'pactl set-sink-mute @DEFAULT_SINK@ false; pactl set-sink-volume @DEFAULT_SINK@ +10%'",
    "down": "sh -c 'pactl set-sink-mute @DEFAULT_SINK@ false; pactl set-sink-volume @DEFAULT_SINK@ -10%'",
    "toggle": "pactl set-sink-mute @DEFAULT_SINK@ toggle",
    "toggle-mic": "pactl set-source-mute @DEFAULT_SOURCE@ toggle",
}
WIDTH = 28  # 32 with font=12
FONTSIZE = 12
DEBUG = "#00ff00"
MARGIN = 15
BACKGROUND = GRUVBOX["bg0_h"] + "00"

YOFFSET = 0  # offset from top of the screen
SCREENDIM = (1366, 768)  # (1366, 768)
FakeScreenDimDim = namedtuple("FakeScreenDimDim", "x y width height")
DUMMY = FakeScreenDimDim(0, YOFFSET + MARGIN, SCREENDIM[0], WIDTH)
MAIN = FakeScreenDimDim(
    DUMMY.x,
    DUMMY.y + DUMMY.height + MARGIN,
    SCREENDIM[0],
    SCREENDIM[1] - DUMMY.y - DUMMY.height - MARGIN,
)


def text_color_transition(color_1, color_2, symbol):
    """Return circle textbox instance. Transition from color 1 to color 2."""
    return widget.TextBox(
        symbol, foreground=color_1, background=color_2, fontsize=25, padding=-1
    )


def get_endcap(color_1, color_2, symbol, left=True) -> tuple:
    """Get endcap of powerline esque widget line.
    @param left: for left endcaps. Set left=False for right endcaps."""
    if left:
        return (
            widget.Spacer(length=MARGIN),
            # widget.TextBox(" ", fontsize=1),    # need to get a rounded look. otherwise the end is pointed
            text_color_transition(color_1, color_2, symbol),
        )
    return (
        text_color_transition(color_1, color_2, symbol),
        widget.Spacer(length=MARGIN)
        # widget.TextBox(" ", fontsize=1)    # needed to get a rounded look. otherwise the end is pointed
    )


def truncate_text(text: str) -> str:
    ELLIPSIS = "..."
    MAX = 10
    if len(text) > MAX:
        return text[:MAX] + ELLIPSIS
    return text


def init_fake_screens():
    main_screen = Screen(
        top=init_bar(init_1st_bar_widgets()),
        x=MAIN.x,
        y=MAIN.y,
        height=MAIN.height,
        width=MAIN.width,
        bottom=init_bar(init_gradient_bar_widgets()),
    )
    dummy_screen = Screen(
        bottom=init_bar(init_2nd_bar_widgets()),
        x=DUMMY.x,
        y=DUMMY.y,
        height=DUMMY.height,
        width=DUMMY.width,
    )
    return [main_screen, dummy_screen]


def init_treelayout():
    return layout.TreeTab(
        panel_width=panel_width,
        active_bg=GRADIENT[3],
        active_fg=GRUVBOX["bg0_h"],
        bg_color=GRUVBOX["bg0_h"] + "00",
        border_width=border_width,
        # font
        fontshadow=None,
        place_right=False,
        previous_on_rm=False,
        # tab settings
        fontsize=fontsize,
        inactive_bg=GRUVBOX["bg0_h"],
        inactive_fg=GRUVBOX["fg"],
        level_shift=TENPERCENT,
        margin_left=0,
        margin_y=0,
        padding_left=0,
        padding_x=0,
        padding_y=padding_y,
        # section settings
        section_bottom=6,
        section_fg="#00ff0000",
        section_fontsize=0,
        section_left=4,
        section_padding=4,
        section_top=4,
        sections=[""],
        urgent_bg="#ff0000",
        urgent_fg="#ffffff",
        vspace=-TENPERCENT,
    )


def init_bar(widgets) -> bar.Bar:
    return bar.Bar(
        widgets,
        WIDTH,
        background=GRUVBOX["bg0_h"] + "00",  # make color transparent
        border_width=0,  # [N E S W]
        border_color=[GRUVBOX["bg0_s"] + "00"] * 4,  # make border transparent
    )


def init_1st_bar_widgets() -> list:
    return [
        *get_endcap(GRADIENT3[0], BACKGROUND, SYMBOLS["left-circle"]),
        widget.CheckUpdates(
            distro="Arch", no_update_string="0 updates", background=GRADIENT3[0]
        ),
        text_color_transition(GRADIENT3[0], GRADIENT3[1], SYMBOLS["right-circle"]),
        widget.TextBox(" ", background=GRADIENT3[1]),
        widget.CurrentLayoutIcon(scale=0.65, background=GRADIENT3[1]),
        widget.CurrentLayout(background=GRADIENT3[1]),
        widget.TextBox(" ", background=GRADIENT3[1]),
        text_color_transition(GRADIENT3[1], GRADIENT3[2], SYMBOLS["right-circle"]),
        widget.TextBox(" ", background=GRADIENT3[2]),
        widget.GroupBox(
            background=GRADIENT3[2],
            foreground="#ffff00",
            highlight_method="block",
            active="#ff0000",
            inactive="#00ffff",
            disable_drag=True,
            block_highlight_text_color=GRUVBOX["bg0_h"],
            highlight_color=[GRADIENT3[2], GRADIENT[3]],
            this_current_screen_border=GRADIENT[3],
            this_screen_border="#00ff00",
            other_current_screen_border="#ff00ff",
            other_screen_border=GRADIENT3[3],
        ),
        text_color_transition(
            GRADIENT3[2], GRADIENT3[3] + "00", SYMBOLS["right-circle"]
        ),
        widget.TextBox(" "),
        widget.TaskList(
            # background=GRADIENT3[1],
            border=GRADIENT[3],
            # borderwidth=[1, BORDERWIDTH, 1, 1],
            foreground=GRUVBOX["bg0_h"],
            highlight_method="block",
            icon_size=None,
            margin=3,
            # max_title_width=200,
            padding=3,
            parse_text=truncate_text,
            rounded=True,
            spacing=None,
            theme_mode=None,
            # title_width_method="uniform",
            unfocused_border=GRADIENT3[3],
            urgent_alert_method="border",
            urgent_border=GRUVBOX["red"],
        ),
        # text_color_transition(GRADIENT3[2], GRADIENT3[3], SYMBOLS["right-circle"]),
        # text_color_transition(GRADIENT3[3], GRADIENT3[4], SYMBOLS["right-circle"]),
        # END LEFT BLOCK
        # widget.Spacer(),
        widget.TextBox(" "),
        # text_color_transition(
        #    GRADIENT3[5], GRADIENT3[0] + "00", SYMBOLS["left-circle"]
        # ),
        # text_color_transition(GRADIENT3[4], GRADIENT3[5], SYMBOLS["left-circle"]),
        widget.Systray(),
        widget.StatusNotifier(),
        widget.TextBox(" "),
        # text_color_transition(GRADIENT3[4], BACKGROUND, SYMBOLS["left-circle"]),
        # widget.TextBox(
        #    "\uea99 ",
        #    foreground=GRUVBOX["bg0_h"],
        #    background=GRADIENT3[4],
        #    fontsize=int(1.5 * FONTSIZE),
        # ),
        # widget.StatusNotifier(background=GRADIENT3[4], foreground=GRUVBOX["bg0_h"], icon_theme=None),   # needs python-pyxdg, and python-dbus-next
        # widget.TextBox(" ", background=GRADIENT3[4]),
        text_color_transition(
            GRADIENT3[3], GRADIENT3[4] + "00", SYMBOLS["left-circle"]
        ),
        widget.TextBox(
            " ",
            foreground=GRUVBOX["bg0_h"],
            background=GRADIENT3[3],
            fontsize=FONTSIZE,
        ),
        widget.PulseVolume(foreground=GRUVBOX["bg0_h"], background=GRADIENT3[3]),
        widget.TextBox(" ", background=GRADIENT3[3], fontsize=FONTSIZE),
        text_color_transition(GRADIENT3[2], GRADIENT3[3], SYMBOLS["left-circle"]),
        widget.Backlight(
            format=SYMBOLS["brightness"] + "{percent:2.0%} ",
            change_command="brightnessctl set {}%",
            backlight_name="intel_backlight",
            background=GRADIENT3[2],
            # foreground=GRUVBOX["bg0_h"],
        ),
        text_color_transition(GRADIENT3[1], GRADIENT3[2], SYMBOLS["left-circle"]),
        widget.Battery(
            # foreground=GRUVBOX["bg0_h"],
            background=GRADIENT3[1],
            show_short_text=False,
            low_percentage=0.15,
            charge_char="\uf0e7",
            discharge_char="\uf242",
            empty_char="\uf244",
            full_char="\uf240",
            format="{char}  {percent:2.0%} ",
            unkown_char="?",
            low_foreground=GRUVBOX["red"],
            update_interval=30,
        ),
        text_color_transition(GRADIENT3[0], GRADIENT3[1], SYMBOLS["left-circle"]),
        widget.Spacer(length=int(FONTSIZE / 2), background=GRADIENT3[0]),
        widget.QuickExit(
            default_text=SYMBOLS["power"],
            countdown_format="({})",
            fontsize=int(1.5 * FONTSIZE),
            foreground=GRADIENT3[5],
            background=GRUVBOX["bg0_h"],
        ),
        *get_endcap(GRADIENT3[0], BACKGROUND, SYMBOLS["right-circle"], left=False),
    ]


def init_2nd_bar_widgets() -> list:
    return [
        *get_endcap(GRADIENT3[0], BACKGROUND, SYMBOLS["left-circle"]),
        # widget.TextBox(" ", background=GRADIENT3[0], fontsize=FONTSIZE),
        widget.CPU(
            format="CPU {freq_current}GHz {load_percent}%",
            background=GRADIENT3[0],
        ),
        text_color_transition(GRADIENT3[0], GRADIENT3[1], SYMBOLS["right-circle"]),
        widget.TextBox(" ", background=GRADIENT3[1], fontsize=FONTSIZE),
        widget.Memory(
            measure_mem="G",
            measure_swap="G",
            background=GRADIENT3[1],
            # RAM|SWP
            format="RAM {MemUsed:.0f}/{MemTotal:.0f}{mm} SWP {SwapUsed:.0f}/{SwapTotal:.0f}{mm}",
        ),
        text_color_transition(GRADIENT3[1], GRADIENT3[2], SYMBOLS["right-circle"]),
        widget.TextBox(" ", background=GRADIENT3[2], fontsize=FONTSIZE),
        widget.ThermalZone(
            fgcolor_normal=GRUVBOX["fg"],
            background=GRADIENT3[2],
            format=SYMBOLS["thermometer"] + " " + "{temp}°F",
        ),
        # widget.Load(background=GRADIENT3[2]),  # what is this even measuring
        text_color_transition(GRADIENT3[2], GRADIENT3[3], SYMBOLS["right-circle"]),
        widget.TextBox(
            " ",
            background=GRADIENT3[3],
        ),
        widget.Net(
            foreground=GRUVBOX["bg0_h"],
            background=GRADIENT3[3],
            format="↓↑ {total}",
        ),
        text_color_transition(GRADIENT3[3], GRADIENT3[4], SYMBOLS["right-circle"]),
        # widget.TextBox(
        #    " ",
        #    background=GRADIENT3[4],
        # ),
        widget.DF(
            visible_on_warn=False,
            background=GRADIENT3[4],
            foreground=GRUVBOX["bg0_h"],
            format=" \uf0c7" + " {f}{m}|{r:.0f}%",
        ),
        text_color_transition(GRADIENT3[4], GRADIENT3[5], SYMBOLS["right-circle"]),
        widget.TextBox(" ", background=GRADIENT3[5], fontsize=int(FONTSIZE / 2)),
        widget.TextBox(
            "\uf120",
            foreground=GRUVBOX["bg0_h"],
            background=GRADIENT3[5],
            fontsize=2 * FONTSIZE,
        ),
        widget.Prompt(
            prompt="",
            background=GRADIENT3[5],
            foreground=GRUVBOX["bg0_h"],
            fontsize=FONTSIZE + 4,
            cursor_color=GRUVBOX["bg0_h"],
            bell_style="visual",
            visual_bell_color=DEBUG,
        ),
        text_color_transition(
            GRADIENT3[5], GRADIENT3[0] + "00", SYMBOLS["right-circle"]
        ),
        # widget.LaunchBar(BACKGROUND=DEBUG),
        # widget.Notify(),
        # widget.TextBox(" "),
        # MIDDLE
        widget.Spacer(),
        # text_color_transition(
        #    GRADIENT3[2], GRADIENT3[0] + "00", SYMBOLS["left-circle"]
        # ),
        # text_color_transition(GRADIENT3[2], GRADIENT3[3] + "00", SYMBOLS["left-circle"]),
        text_color_transition(
            GRADIENT3[1], GRADIENT3[2] + "00", SYMBOLS["left-circle"]
        ),
        widget.OpenWeather(
            location="Berkeley, US",
            metric=False,
            # format="{main_temp}°{units_temperature} {icon} {weather_details}",
            format="{location_city} {main_temp}°{units_temperature} {weather_details}",
            background=GRADIENT3[1],
        ),
        widget.TextBox(" ", background=GRADIENT3[1]),
        text_color_transition(GRADIENT3[0], GRADIENT3[1], SYMBOLS["left-circle"]),
        widget.Clock(background=GRADIENT3[0], format="%Y/%m/%d %a %I:%M %p"),
        *get_endcap(GRADIENT3[0], BACKGROUND, SYMBOLS["right-circle"], left=False),
    ]


def rgba_to_hex(color: tuple) -> str:
    """Convert rga or rgba to hex. If rgb then a=255 is assumed."""
    if len(color) == 3:
        # rgb
        return "#{:02x}{:02x}{:02x}".format(*color)
    # rgba
    return "#{:02x}{:02x}{:02x}{:02x}".format(*color)


def init_gradient_bar_widgets() -> list:
    colors = []
    rgb = (150, 150, 150)
    for i in range(0, 255, 20):
        colors.append(widget.TextBox(" ", background=rgba_to_hex((*rgb, i))))
    return colors


# MY CODE ==================================================

mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Key("alt", "Tab", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # control screen brightness, needs brightnessctl to work
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 10%+")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    # control volume, needs pactl to work
    Key([], "XF86AudioRaiseVolume", lazy.spawn(VOLUME_COMMANDS["up"])),
    Key([], "XF86AudioLowerVolume", lazy.spawn(VOLUME_COMMANDS["down"])),
    Key([], "XF86AudioMute", lazy.spawn(VOLUME_COMMANDS["toggle"])),
    Key([], "XF86AudioMicMute", lazy.spawn(VOLUME_COMMANDS["toggle-mic"])),
]

groups = [Group(i) for i in ["1", "2"]]  # number of groups default="123456789"

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

# tree tab settings
panel_width = 200
percent = 0.1  # controls spacing between absolute rect and tabs
TENPERCENT = panel_width * percent
border_width = panel_width * percent
padding_y = panel_width * percent
fontsize = FONTSIZE  # int(panel_width*percent/2)
layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=10),
    layout.Max(margin=MARGIN),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(margin=MARGIN, border_focus=GRUVBOX["orange"], border_width=0),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(panel_width=200, font_size),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=FONTSIZE,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# fake_screens = [
#    Screen(height=200, top=bar.Bar(widget.TextBox("Screen1"), 200)),
#    Screen(y=200, top=bar.Bar(widget.TextBox("Screen2"), 200)),
# ]

# screens look like this
#     600         300
#  |-------------|-----|
#  |          480|     |580
#  |   A         |  B  |
#  |----------|--|     |
#  |       400|--|-----|
#  |   C      |        |400
#  |----------|   D    |
#     500     |--------|
#                 400
#
# Notice there is a hole in the middle
# also D goes down below the others
fake_screens = init_fake_screens()
"""
screens = [
    Screen(
        y=200,
        top=bar.Bar(
            [
                text_color_transition(
                    GRADIENT3[0], BACKGROUND, SYMBOLS["left-circle"]
                ),
                widget.CurrentLayoutIcon(background=GRUVBOX["bg0_h"], scale=0.75),
                widget.CurrentLayout(background=GRUVBOX["bg0_h"]),
                text_color_transition(
                    GRADIENT3[0], GRADIENT3[1], SYMBOLS["right-circle"]
                ),
                # widget.GroupBox(), # I don't use this
                widget.TextBox(" ", background=GRADIENT3[1], fontsize=FONTSIZE),
                widget.CPU(format="CPU {freq_current}GHz {load_percent}%", background=GRADIENT3[1]),
                text_color_transition(
                    GRADIENT3[1], GRADIENT3[2], SYMBOLS["right-circle"]
                ),
                widget.TextBox(" ", background=GRADIENT3[2], fontsize=FONTSIZE),
                widget.Memory(measure_mem="G", swap_mem="G", background=GRADIENT3[2], format="RAM {MemUsed:.0f}/{MemTotal:.0f}{mm} SWP {SwapUsed:.0f}/{SwapTotal:.0f}{mm}"),
                text_color_transition(
                    GRADIENT3[2], GRADIENT3[3], SYMBOLS["right-circle"]
                ),
                widget.TextBox(
                    " ",
                    foreground=GRUVBOX["bg0_h"],
                    background=GRADIENT3[3],
                    fontsize=FONTSIZE,
                ),
                widget.ThermalZone(
                    fgcolor_normal=GRUVBOX["bg0_h"], background=GRADIENT3[3], format=SYMBOLS["thermometer"] + " " + "{temp}°F"
                ),
                text_color_transition(
                    GRADIENT3[3], GRADIENT3[4], SYMBOLS["right-circle"]
                ),
                widget.TextBox(
                    " ",
                    foreground=GRUVBOX["bg0_h"],
                    background=GRADIENT3[4],
                    fontsize=FONTSIZE,
                ),
                widget.TextBox(
                    "\uf120",
                    foreground=GRUVBOX["bg0_h"],
                    background=GRADIENT3[4],
                    fontsize=2 * FONTSIZE,
                ),
                widget.Prompt(
                    prompt="",
                    background=GRADIENT3[4],
                    foreground=GRUVBOX["bg0_h"],
                    fontsize=FONTSIZE+4,
                    cursor_color=GRUVBOX["bg0_h"],
                    bell_style="visual"
                ),
                text_color_transition(
                    GRADIENT3[4], GRADIENT3[0] + "00", SYMBOLS["right-circle"]
                ),
                # widget.WindowName(),
                # widget.WindowTabs(separator="|"),
                #text_color_transition(
                #    GRADIENT3[4], GRADIENT3[5], SYMBOLS["right-circle"]
                #),
                #widget.TextBox(
                #    " ",
                #    foreground=GRUVBOX["bg0_h"],
                #    background=GRADIENT3[5],
                #    fontsize=FONTSIZE,
                #),
                #widget.TextBox(
                #    "\uf120",
                #    foreground=GRUVBOX["bg0_h"],
                #    background=GRADIENT3[5],
                #    fontsize=2 * FONTSIZE,
                #),
                #widget.Prompt(
                #    prompt="",
                #    background=GRADIENT3[5],
                #    foreground=GRUVBOX["bg0_h"],
                #    fontsize=FONTSIZE+4,
                #    cursor_color=GRUVBOX["bg0_h"],
                #    bell_style="visual"
                #),
                #text_color_transition(
                #    GRADIENT3[5], GRADIENT3[0] + "00", SYMBOLS["right-circle"]
                #),
                widget.TextBox(" "),
                widget.OpenWeather(
                    location="Berkeley, US",
                    metric=False,
                    #format="{main_temp}°{units_temperature} {icon} {weather_details}",
                    format="{location_city}: {main_temp}°{units_temperature} {icon} {weather_details}",
                    #background=GRADIENT3[4],
                    #foreground=GRUVBOX["bg0_h"]
                ),
                # widget.TextBox(" ", background=GRADIENT3[6], fontsize=30),
                # widget.Chord(
                #    chords_colors={
                #        "launch": ("#ff0000", "#ffffff"),
                #    },
                #    name_transform=lambda name: name.upper(),
                # ),
                # widget.TextBox("default config", name="default"),
                # widget.Volume(),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(background=DEBUG),
                # widget.Net(),
                # widget.Wttr(),
                widget.Spacer(),
                text_color_transition(
                    GRADIENT3[5], GRADIENT3[0] + "00", SYMBOLS["left-circle"]
                ),
                widget.Backlight(
                    format=SYMBOLS["brightness"] + "{percent:2.0%}",
                    change_command="brightnessctl set {}%",
                    backlight_name="intel_backlight",
                    background=GRADIENT3[5],
                    foreground=GRUVBOX["bg0_h"]
                ),
                widget.TextBox(" ", background=GRADIENT3[5], fontsize=FONTSIZE),
                text_color_transition(
                    GRADIENT3[4], GRADIENT3[5], SYMBOLS["left-circle"]
                ),
                # widget.TextBox(" ", background=GRADIENT3[4], fontsize=30),
                widget.Battery(
                    foreground=GRUVBOX["bg0_h"],
                    background=GRADIENT3[4],
                    show_short_text=False,
                    low_percentage=0.15,
                    charge_char="\uf0e7",
                    discharge_char="\uf242",
                    empty_char="\uf244",
                    full_char="\uf240",
                    format="{char}  {percent:2.0%} ",
                    unkown_char="?",
                    low_foreground=GRUVBOX["red"],
                ),
                text_color_transition(
                    GRADIENT3[3], GRADIENT3[4], SYMBOLS["left-circle"]
                ),
                widget.Net(
                    foreground=GRUVBOX["bg0_h"],
                    background=GRADIENT3[3],
                    format="↓↑ {total}",
                ),
                widget.TextBox(" ", background=GRADIENT3[3], fontsize=FONTSIZE),
                text_color_transition(
                    GRADIENT3[2], GRADIENT3[3], SYMBOLS["left-circle"]
                ),
                # widget.Wlan(foreground=DEBUG),
                # widget.Volume(),
                widget.TextBox(" ", background=GRADIENT3[2], fontsize=FONTSIZE),
                widget.PulseVolume(background=GRADIENT3[2]),
                #widget.Volume(background=GRADIENT3[2], emoji=True),     # doesnt work with nerdfonts
                widget.TextBox(" ", background=GRADIENT3[2], fontsize=FONTSIZE),
                text_color_transition(
                    GRADIENT3[1], GRADIENT3[2], SYMBOLS["left-circle"]
                ),
                widget.Clock(background=GRADIENT3[1], format="%Y-%m-%d %a %I:%M %p"),
                widget.TextBox(" ", background=GRADIENT3[1], fontsize=FONTSIZE),
                text_color_transition(
                    GRADIENT3[0], GRADIENT3[1], SYMBOLS["left-circle"]
                ),
                widget.QuickExit(
                    default_text=SYMBOLS["power"],
                    countdown_format="({})",
                    fontsize=2 * FONTSIZE,
                    foreground=GRADIENT3[5],
                    background=GRUVBOX["bg0_h"]
                ),
                #widget.TextBox(" ", background=GRADIENT3[0], fontsize=int(FONTSIZE/2)),
                text_color_transition(
                    GRADIENT3[0], BACKGROUND, SYMBOLS["right-circle"]
                ),
            ],
            WIDTH,
            opacity=100,
            background=GRUVBOX["bg0_h"] + "00",  # make color transparent
            border_width=MARGIN,   # [BARBORDERWIDTH, BARBORDERWIDTH, MARGIN, BARBORDERWIDTH],   # [N E S W]
            border_color=[GRUVBOX["bg0_s"] + "00"] * 4
            # ["ff00ff", "ff00ff", "ff00ff", "ff00ff"]  # Borders are magenta
        ),
    ),
]
"""
# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
