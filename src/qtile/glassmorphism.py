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


# MY CODE ========================================================================================================================
from collections import namedtuple
from qtile_extras import widget
from qtile_extras.widget.decorations import (
    PowerLineDecoration,
    RectDecoration,
    BorderDecoration,
)

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

BACKGROUND = "#00000000"
DARK_BACKGROUND = GRUVBOX["dark0_hard"]
FOREGROUND = GRUVBOX["light0_hard"]
#FOREGROUND = "#000000"
ACCENT = GRUVBOX["faded_purple"]
#FOREGROUND = GRUVBOX["bright_orange"]
DEBUG = "#00ff00"
BORDER_COLOR = GRUVBOX["light0_hard"] + "00"
ICON_PATHS = []
WALLPAPER = '~/.config/qtile/awesome.png'

if 0:
    # set lightmode colors
    ACCENT = GRUVBOX["bright_orange"]
    WHITE = GRUVBOX["light0_hard"]
    FOREGROUND = GRUVBOX["dark0_hard"]
    ICON_PATHS = ["/home/saccharine/.config/qtile/qtile-layout-icons/layout-icons/gruvbox-dark0"]
    WALLPAPER = '~/.config/qtile/background.jpg'
DECOR = {
    "decorations": [
        RectDecoration(
            colour=FOREGROUND + "32",
            radius=10,
            filled=True,
            padding_x=0,
            padding_y=0,
            group=False,
            use_widget_background=False,
        ),
        # BorderDecoration(colour=DEBUG)
    ],
    "padding": 0,
}

ENDCAPL = {
    "decorations": [PowerLineDecoration(path="rounded_right", shift=40, size=25)],
    "padding": 0,
}
FONTSIZE = 12
PADDING = 14
widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=FONTSIZE,
    padding=PADDING,
    background=BACKGROUND,
    foreground=FOREGROUND,
)

SCREENDIM = (1366, 768)  # (1366, 768)
FakeScreenDim = namedtuple("FakeScreenDimDim", "x y width height")

MAIN = FakeScreenDim(
    PADDING,
    PADDING,
    SCREENDIM[0]-2*PADDING,
    SCREENDIM[1] -PADDING,
)
LMARGIN = int(PADDING)
HIGHLIGHT=BorderDecoration(border_width=[4, 0, 0, 0], colour=WHITE + "32")  #"08"


def val_to_hex(val) -> str:
    return "{:02x}".format(val)


def get_endcap(left) -> dict:
    path = "rounded_right" if left else "rounded_left"
    background = BORDER_COLOR if left else BACKGROUND
    params = {"decorations": [PowerLineDecoration(path=path, shift=40, size=25)]}
    if not left:
        params = {"decorations": [PowerLineDecoration(path=path, shift=0, size=25)]}
    return widget.Spacer(
        widget_defaults["fontsize"], background=background, foreground=DEBUG, **params
    )


def init_widgets() -> list:
    NUM_WIDGETS = 8
    # transparency settings
    MAX_ALPHA, STEPS, COLOR = 50, NUM_WIDGETS, FOREGROUND
    STEP = int(MAX_ALPHA / STEPS)
    PRIGHT = dict(decorations=[PowerLineDecoration(path="rounded_left")])
    PLEFT = dict(decorations=[PowerLineDecoration(path="rounded_right")])
    # params2 = dict(decorations=[RectDecoration(colour=color + dalpha, filled=True, padding_y=10, group=False, radius=20)])
    background_1 = []  # ["#ff0000"] *4
    background_2 = []
    g1 = lambda pop=0: background_1.pop() if pop else background_1[-1]
    g2 = lambda pop=0: background_2.pop() if pop else background_2[-1]
    for i in range(STEPS):
        bg_1 = COLOR + val_to_hex((i + 1) * STEP)
        bg_2 = COLOR + val_to_hex(30)
        background_1.insert(0, bg_1)
        background_2.insert(0, bg_2)
    items = [
        *build_transition(BACKGROUND, g1(), 1),
        widget.CheckUpdates(
            distro="Arch", no_update_string="0 updates", colour_no_updates=FOREGROUND, **build_dict(g1(), g2(1))
        ),
        *build_transition(g1(1), g1(), 0),
        widget.CurrentLayoutIcon(
            scale=0.35, padding=0, **build_dict(g1(), g2(), group=True), custom_icon_paths=ICON_PATHS
        ),
        widget.CurrentLayout(**build_dict(g1(), g2(1), group=True)),
        *build_transition(g1(1), g1(), 0),
        widget.Spacer(length=int(1.5*FONTSIZE), **build_dict(g1(), g2(), group=True)),
        widget.TaskList(
            # background=g1(),
            border=ACCENT + "aa",
            # foreground=DARK_BACKGROUND,
            borderwidth=0,
            highlight_method="block",
            icon_size=0,  # 4*FONTSIZE,
            padding=6,
            margin_x=9,
            margin=16,
            # margin_y=15,
            # max_title_width=200,
            parse_text=lambda string: string
            if len(string) < 10
            else string[:10] + "...",
            rounded=True,
            spacing=None,
            theme_mode=None,
            # title_width_method="uniform",
            unfocused_border=g2(),
            urgent_alert_method="border",
            urgent_border=GRUVBOX["bright_red"],
            **build_dict(g1(), g2(), group=True)
        ),
        widget.Spacer(length=int(1.5*FONTSIZE), **build_dict(g1(), g2(1), group=True)),
        *build_transition(g1(1), g1(), 0),
        widget.TextBox(
            "\uf120 ",
            fontsize=2 * FONTSIZE,
            **build_dict(g1(), g2(), group=True)
        ),
        widget.Prompt(
            prompt="",
            fontsize=FONTSIZE + 4,
            cursor_color=FOREGROUND,
            bell_style="visual",
            visual_bell_color=DEBUG,
            **build_dict(g1(), g2(1), group=True)
        ),
        widget.Spacer(background=g1(), **dict(decorations=[HIGHLIGHT])),
        *build_transition(g1(1), g1(), 0),
        widget.TextBox(
            "", fontsize=FONTSIZE, **build_dict(g1(), g2(), group=True)
        ),
        widget.PulseVolume(**build_dict(g1(), g2(1), group=True)),
        *build_transition(g1(1), g1(), 0),
        # widget.TextBox("foo", **build_dict(g1(), g2(1))),
        widget.Backlight(
            format=SYMBOLS["brightness"]+" {percent:2.0%}",
            backlight_name="intel_backlight",
            **build_dict(g1(), g2(1), group=True)
        ),
        *build_transition(g1(1), g1(), 0),
        widget.Battery(
            # foreground=GRUVBOX["bg0_h"],
            show_short_text=False,
            low_percentage=0.15,
            charge_char="\uf0e7",
            discharge_char="\uf242",
            empty_char="\uf244",
            full_char="\uf240",
            format="{char}  {percent:2.0%} ",
            unkown_char="?",
            low_foreground=GRUVBOX["bright_red"],
            update_interval=30,
            **build_dict(g1(), g2(1), group=True)
        ),
        *build_transition(g1(1), g1(), 0),
        widget.QuickExit(
            default_text= " "+ SYMBOLS["power"],
            countdown_format="({})",
            fontsize=int(2 * FONTSIZE),
            **build_dict(g1(), g2(1))
        ),
        #widget.Spacer(length=FONTSIZE, background=g1(), **dict(decorations=[HIGHLIGHT])),
        #*build_transition(g1(), DEBUG, 0),
        widget.Spacer(length=1, background=g1(), **dict(decorations=[PowerLineDecoration(path="rounded_left"), HIGHLIGHT]))
    ]
    return items


def rgba_to_hex(color: tuple) -> str:
    """Convert rga or rgba to hex. If rgb then a=255 is assumed."""
    if len(color) == 3:
        # rgb
        return "#{:02x}{:02x}{:02x}".format(*color)
    # rgba
    return "#{:02x}{:02x}{:02x}{:02x}".format(*color)


def hex_to_rgba(string) -> tuple:
    h = string.lstrip("#")
    if len(string) == 6:
        h += "ff"
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4, 6))


def double_alpha(string) -> str:
    r, g, b, a = hex_to_rgba(string)
    return rgba_to_hex((r, g, b, a * 2))


def build_dict(color_1, color_2, group=False):
    # padding = 0 if group else PADDING
    PADDING = 3
    return dict(
        background=color_1,
        decorations=[
            RectDecoration(
                colour=color_2,
                filled=True,
                padding_x=PADDING,
                padding_y=3 * PADDING,
                group=group,
                radius=20,
                use_widget_background=False,
            ),
            HIGHLIGHT
        ],
    )


def build_transition(color_1, color_2, left):
    path = "rounded_right" if left else "rounded_left"
    params = dict(decorations=[PowerLineDecoration(path=path), HIGHLIGHT])
    p = dict(decorations=[HIGHLIGHT])
    length = 1 if left else FONTSIZE
    return [
        widget.Spacer(length=1, background=color_1, **params),
        widget.Spacer(length=length, background=color_2, **p),
    ]


def init_bar() -> bar.Bar:
    """
    widgets = []
    max_alpha = 40
    steps = 5
    step = int(max_alpha / steps)
    color = FOREGROUND
    widgets.append(widget.Spacer(1, background=BORDER_COLOR))
    widgets.append(get_endcap(True))
    #for i in range(steps, 0, -1):
    for i in range(steps):
        alpha = "{:02x}".format((i + 1) * step)
        dalpha = "{:02x}".format((steps - i + 1) * step)
        params = dict(decorations=[PowerLineDecoration(path="rounded_left")])
        params2 = dict(decorations=[RectDecoration(colour=color + dalpha, filled=True, padding_y=10, group=False, radius=20)])
        if i != steps:
            widgets.append(widget.Spacer(length=FONTSIZE, background=color+alpha))
        widgets.append(
            widget.TextBox("Hello World!", foreground=FOREGROUND, padding=10, background=color+alpha, **params2)
        )
        widgets.append(widget.TextBox(" ",background=color+alpha, **params))
    widgets.append(widget.Spacer())
    widgets.append(get_endcap(False))
    widgets.append(widget.Spacer(1, background=BORDER_COLOR))
    """
    return bar.Bar(
        init_widgets(),
        60,
        background=BACKGROUND,  # make color transparent
        border_width=0,#PADDING,
        border_color="#00000000",
    )


def get_widgets() -> list:
    return [widgets.TextBox(" ")]


# MY CODE ========================================================================================================================

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
]

groups = [Group(i) for i in "123456789"]

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

layouts = [
    layout.MonadTall(margin=LMARGIN, border_focus=WHITE, border_normal=GRUVBOX["dark1"], border_width=2),
    #layout.Columns(border_focus_stack=[FOREGROUND, "#8f3d3d"], border_width=4, margin=LMARGIN),
    layout.Max(margin=LMARGIN),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

extension_defaults = widget_defaults.copy()

screens = [
    Screen(top=init_bar(), x=MAIN.x, y=MAIN.y, width=MAIN.width, height=MAIN.height,
        wallpaper=WALLPAPER,
        wallpaper_mode='fill',
          ),
]

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
