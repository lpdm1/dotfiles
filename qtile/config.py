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


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
#import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    Key([mod,"shift"], "Right", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod,"shift"], "Left", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
#group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#5e81ac",
            "border_normal": "#4c566a"
            }

layout_theme = init_layout_theme()


layouts = [
    #layout.MonadTall(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadTall(**layout_theme),
    #layout.MonadWide(margin=8, border_width=2, border_focus="#5e81ac", border_normal="#4c566a"),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Floating(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Default
def init_colors():
    return [
        ["#282a36", "#282c34"], #0 background_1
        ["#f8f8f2", "#f8f8f2"], #1 foreground_1
        ["#44475a", "#44475a"], #2 inactive
        ["#6272a4", "#6272a4"], #3 active
        ["#8be9fd", "#8be9fd"], #4 highlight
        ["#50fa7b", "#50fa7b"], #5 highlight_2
        ["#ffb86c", "#ffb86c"], #6 
        ["#ff79c6", "#ff79c6"], #7 this_current
        ["#bd93f9", "#bd93f9"], #8 other_current
        ["#ff5555", "#ff5555"], #9 urgent
        ["#f1fa8c", "#f1fa8c"], #10
        ["#1e1f35", "#1e1f35"], #11
        ["#392e4d", "#392e4d"], #12
        ["#606061", "#606061"], #13
        ["#3f528a", "#3f528a"], #14
        ["#b16286", "#b16286"], #15
        ["#8f3f71", "#8f3f71"], #16
        ["#427b58", "#427b58"], #17
        ["#fe8019", "#fe8019"], #18
        ["#d65d0e", "#d65d0e"], #19
        ["#af3a03", "#af3a03"]  #20
          ]


colors = init_colors()


# WIDGETS FOR THE BAR

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
            #   widget.Sep(
            #            linewidth = 0,
            #            padding = 6,
            #            foreground = colors[2],
            #            background = colors[0]
            #            ),
            #   widget.Image(
            #            filename = "~/.config/qtile/icons/python-white.png",
            #            scale = "False",
            #            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
            #            ),
            #   widget.Sep(
            #            linewidth = 0,
            #            padding = 6,
            #            foreground = colors[2],
            #            background = colors[0]
            #            ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[1],
                       background = colors[0],
                       padding = 5,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       font = "Fira Code",
                       foreground = colors[1],
                       background = colors[0],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[1],
                       foreground = colors[0],
                       padding = -8,
                       fontsize = 40
                       ),
              widget.GroupBox(
                       font = "FontAwesome",
                       fontsize = 15,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[7],
                       inactive = colors[13],
                       rounded = False,
                       highlight_color = colors[3],
                       highlight_method = "line",
                       block_highlight_text_color = colors[7],
                       urgent_border = colors[9],
                       this_current_screen_border = colors[7],
                       this_screen_border = colors [7],
                       other_current_screen_border = colors[8],
                       other_screen_border = colors[8],
                       foreground = colors[1],
                       background = colors[1]
                       ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[1],
                       padding = -8,
                       fontsize = 40
                       ),
            #  widget.TextBox(
            #            text = '|',
            #            font = "Ubuntu Mono",
            #            background = colors[0],
            #            foreground = '474747',
            #            padding = 2,
            #            fontsize = 14
            #            ),
            #   widget.TextBox(
            #            text = '◤',
            #            font = "Ubuntu Mono",
            #            background = colors[4],
            #            foreground = colors[0],
            #            padding = -8,
            #            fontsize = 40
            #            ),
            #  widget.TextBox(
            #            text = '|',
            #            font = "Ubuntu Mono",
            #            background = colors[0],
            #            foreground = '474747',
            #            padding = 2,
            #            fontsize = 14
            #            ),
              widget.WindowName(
                       font = "Fira Code",
                       fontsize = 10,
                       foreground = colors[1],
                       background = colors[0],
                       padding = 0
                       ),
            #   widget.Sep(
            #            linewidth = 0,
            #            padding = 6,
            #            foreground = colors[0],
            #            background = colors[0]
            #            ),
             #widget.TextBox(
             #          text = '◤',
             #          font = "Ubuntu Mono",
             #          background = colors[0],
             #          foreground = colors[3],
             #          padding = -1,
             #          fontsize = 37
             #          ),
             #widget.Net(
             #          interface = "enp5s0",
             #          format = 'Net: {down} ↓↑ {up}',
             #          foreground = colors[1],
             #          background = colors[3],
             #          padding = 5
             #          ),
            #   widget.TextBox(
            #            text = '◤',
            #            font = "Ubuntu Mono",
            #            background = colors[0],
            #            foreground = colors[4],
            #            padding = -6.5,
            #            fontsize = 40
            #            ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[4],
                       foreground = colors[0],
                       padding = -8,
                       fontsize = 40
                       ),
              widget.ThermalSensor(
                       font = "Fira Code",
                       fontsize = 10,
                       foreground = colors[11],
                       background = colors[4],
                       threshold = 90,
                       fmt = 'Temp: {}',
                       padding = 5,
                       ),
              widget.TextBox(
                       text='◤',
                       font = "Ubuntu Mono",
                       background = colors[5],
                       foreground = colors[4],
                       padding = -8,
                       fontsize = 40
                       ),
              widget.CheckUpdates(
                       font = "Fira Code",
                       fontsize = 10,
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Updates: {updates} ",
                       foreground = colors[1],
                       colour_have_updates = colors[11],
                       colour_no_updates = colors[11],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       padding = 5,
                       background = colors[5]
                       ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[6],
                       foreground = colors[5],
                       padding = -8,
                       fontsize = 40
                       ),
              widget.Memory(
                       font = "Fira Code",
                       fontsize = 10,
                       foreground = colors[11],
                       background = colors[6],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       fmt = 'Mem: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[7],
                       foreground = colors[6],
                       padding = -8,
                       fontsize = 40
                       ),
              widget.Volume(
                       font = "Fira Code",
                       fontsize = 10,
                       foreground = colors[11],
                       background = colors[7],
                       fmt = 'Vol: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[9],
                       foreground = colors[7],
                       padding = -8,
                       fontsize = 40
                       ),
              #widget.KeyboardLayout(
              #         foreground = colors[1],
              #         background = colors[8],
              #         fmt = 'Keyboard: {}',
              #         padding = 5
              #         ),
              #widget.TextBox(
              #         text = '◤',
              #         font = "Ubuntu Mono",
              #         background = colors[8],
              #         foreground = colors[9],
              #         padding = 0,
              #         fontsize = 37
              #         ),
              widget.Clock(
                       font = "Fira Code",
                       fontsize = 10,
                       foreground = colors[11],
                       background = colors[9],
                       format = "%A, %B %d - %H:%M "
                       ),
              widget.TextBox(
                       text = '◤',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[9],
                       padding = -8,
                       fontsize = 40
                       ),
               widget.Systray(
                        background=colors[0],
                        icon_size=20,
                        padding = 4
                        ),
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    #del widgets_screen1[9:50]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[6:25]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=20, opacity=1)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=20, opacity=1))]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
#@hook.subscribe.client_new
#def assign_app_group(client):
#    d = {}
#    #####################################################################################
#    ### Use xprop fo find  the value of WM_CLASS(STRING) -> First field is sufficient ###
#    #####################################################################################
#    d[group_names[0]] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#              "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#    d[group_names[1]] = [ "Atom", "Subl", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#               "atom", "subl", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#    d[group_names[2]] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#              "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#    d[group_names[3]] = ["Gimp", "gimp" ]
#    d[group_names[4]] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#    d[group_names[5]] = ["Vlc","vlc", "Mpv", "mpv" ]
#    d[group_names[6]] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#              "virtualbox manager", "virtualbox machine", "vmplayer", ]
#    d[group_names[7]] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#              "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#    d[group_names[8]] = ["Evolution", "Geary", "Mail", "Thunderbird",
#              "evolution", "geary", "mail", "thunderbird" ]
#    d[group_names[9]] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#              "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#    ######################################################################################
#
#wm_class = client.window.get_wm_class()[0]
#
#    for i in range(len(d)):
#        if wm_class in list(d.values())[i]:
#            group = list(d.keys())[i]
#            client.togroup(group)
#            client.group.cmd_toscreen(toggle=False)
#
# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]


follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),    
    Match(wm_class='ulauncher'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"

