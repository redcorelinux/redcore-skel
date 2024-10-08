# Qtile Config. Original concept done by Jeff Winget and Matt Weber (The Linux Cast).


from typing import List  # noqa: F401
import os
import subprocess
from os import path

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, ScratchPad, DropDown, Key, Match, Screen
from libqtile.lazy import lazy
from settings.path import qtile_path
import colors

# Variables. Change mod key, terminal and app launcher here.
mod = "mod4"
terminal = "alacritty"
rofi = "rofi -show drun -show-icons"

# Alternate colors are located in colors.py. You can change your colorscheme by changing the last word to one of the available colorschemes.
# Currently Available Colorschemes
# Redcore, Dracula, Everforest, Doom-One, Nord, Gruvbox Dark, Catppuccin, moonfly, retro, whitey.

colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.redcore()

keys = [
    # Open terminal
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "d",      lazy.spawn(rofi)),
    # Qtile System Actions
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "x", lazy.shutdown()),
    # Active Window Actions
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod, "control"], "h",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete()
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete()
        ),
    Key([mod, "control"], "l",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add()
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add()
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster()
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster()
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster()
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster()
        ),

    # Window Focus (Arrows and Vim keys)
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # Qtile Layout Actions
    Key([mod], "r", lazy.layout.reset()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "f", lazy.layout.flip()),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    # Move windows around MonadTall/MonadWide Layouts
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),

    # Switch focus to specific monitor (out of three)
    Key([mod], "i", lazy.to_screen(0)),
    Key([mod], "o", lazy.to_screen(1)),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),
]

# Create labels for groups and assign them a default layout.
groups = []

group_names = ["1", "2", "3", "4", "5", "6",
               "7", "8", "9", "0", "minus", "equal"]

# Change out these two lines to change between icons and numbers in the workspace section of the bar.
# group_labels = ["", "", "", "", "", "", "", "", "ﭮ", "", "", "﨣"]
group_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

# Change these to change the default layout per workspace. Do not delete.
group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",
                 "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall"]

# Add group names, labels, and default layouts to the groups object.
for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

# Add group specific keybindings
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(),
            desc="Mod + number to move to that group."),
        Key(["mod1"], "Tab", lazy.screen.next_group(),
            desc="Move to next group."),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group(),
            desc="Move to previous group."),
        Key([mod, "shift"], i.name, lazy.window.togroup(
            i.name), desc="Move focused window to new group."),
    ])

# Define scratchpads. Section can be deleted if you do not intend to use scratchpads.
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "alacritty --class=scratch", width=0.8,
             height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("term2", "alacritty --class=scratch",
             width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
]))

# Scratchpad keybindings
keys.extend([
    Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod, "shift"], "n", lazy.group['scratchpad'].dropdown_toggle('term2')),
])


# Define layouts and layout themes
layout_theme = {
    "margin": 5,
    "border_width": 2,
    "border_focus": colors[9],
    "border_normal": backgroundColor
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# Mouse callback functions


def launch_menu():
    qtile.cmd_spawn("rofi -show drun -show-icons")


# Define Widgets
widget_defaults = dict(
    font="Noto Sans",
    fontsize=14,
    padding=2,
    background=backgroundColor
)


def init_widgets_list(monitor_num):
    widgets_list = [
        widget.GroupBox(
            font="Noto Sans",
            fontsize=14,
            margin_y=2,
            margin_x=4,
            padding_y=5,
            padding_x=5,
            borderwidth=2,
            disable_drag=True,
            active=colors[9],
            inactive=foregroundColor,
            hide_unused=False,
            rounded=True,
            this_current_screen_border=colors[9],
            this_screen_border=colors[7],
            other_screen_border=colors[6],
            other_current_screen_border=colors[6],
            urgent_alert_method="line",
            urgent_border=colors[9],
            urgent_text=colors[1],
            foreground=foregroundColor,
            background=backgroundColor,
            use_mouse_wheel=False
        ),
        widget.TaskList(
            icon_size=0,
            font="Noto Sans",
            foreground=colors[10],
            background=colors[9],
            borderwidth=0,
            border=colors[9],
            margin=0,
            padding=10,
            highlight_method="block",
            title_width_method="uniform",
            urgent_alert_method="border",
            urgent_border=colors[1],
            rounded=False,
            txt_floating="🗗 ",
            txt_maximized="🗖 ",
            txt_minimized="🗕 ",
        ),
        widget.CurrentLayoutIcon(
            scale=0.5,
            foreground=colors[9],
            background=colors[9]
        ),
        widget.Sep(
            linewidth=0,
            padding=10
        ),
        widget.Systray(
            background=backgroundColor,
            icon_size=20,
            padding=10
        ),
        widget.Sep(
            linewidth=0,
            padding=10
        ),
        widget.TextBox(
            text=" ",
            fontsize=14,
            font="FontAwesome",
            foreground=colors[0]
        ),
        widget.PulseVolume(
            font="Noto Sans",
            limit_max_volume=True,
            mute_format='Mute',
            volume_app='pavucontrol-qt',
            foreground=foregroundColor
        ),
        widget.Sep(
            linewidth=0,
            padding=10
        ),
        widget.TextBox(
            text=" ",
            fontsize=14,
            font="FontAwesome",
            foreground=colors[0]
        ),
        widget.CPU(
            font="Noto Sans",
            update_interval=1.0,
            format='{freq_current}Ghz / {load_percent}%',
            foreground=foregroundColor,
            padding=1
        ),
        widget.Sep(
            linewidth=0,
            padding=10
        ),
        widget.TextBox(
            text=" ",
            fontsize=14,
            font="FontAwesome",
            foreground=colors[0]
        ),
        widget.Memory(
            font="Noto Sans",
            foreground=foregroundColor,
            format='{MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}',
            measure_mem='G',
            padding=1,
        ),
        widget.Sep(
            linewidth=0,
            padding=10
        ),
        widget.TextBox(
            text=" ",
            fontsize=14,
            font="FontAwesome",
            foreground=colors[0]
        ),
        widget.Clock(
            format='%I:%M %p',
            font="Noto Sans",
            padding=10,
            foreground=colors[0]
        ),
        widget.Sep(
            linewidth=0,
            padding=10,
        ),
        widget.QuickExit(
            countdown_start=15,
            countdown_format='{}',
            default_text=" ",
            fontsize=14,
            font="FontAwesome",
            foreground=colors[0]
        ),
    ]

    return widgets_list


def init_secondary_widgets_list(monitor_num):
    secondary_widgets_list = init_widgets_list(monitor_num)
    del secondary_widgets_list[13:15]
    return secondary_widgets_list


widgets_list = init_widgets_list("1")
secondary_widgets_list = init_secondary_widgets_list("2")

# Commeont out second Screen line if you do not have second monitor
screens = [
    Screen(bottom=bar.Bar(widgets=widgets_list, size=30,
           background=backgroundColor, margin=0, opacity=0.8),),
    Screen(bottom=bar.Bar(widgets=secondary_widgets_list, size=30,
           background=backgroundColor, margin=0, opacity=0.8),),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.run([home])


dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], fullscreen_border_width=0, border_width=0)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True
wmname = "Qtile 0.21.0"
