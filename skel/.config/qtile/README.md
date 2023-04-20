# Redcore's Qtile Config

## Dependencies
* Qtile
* rofi
* Alacritty
* JetBrainsMono Nerd Font
* Kvantum and QT5CT for applying themes to QT applications
* lxappearance for applying themes to GTK applications
* feh to set the wallpaper

## Assets
The wallpaper and font used in this config can be found in the assets directory.

## Changing Themes 
The current configuration comes with several pre-installed color schemes. The default theme is the Redcore theme. These are also included:
* Dracula
* Everforest
* Doom-One 
* Nord
* Gruvbox Dark
* Catppuccin 
* moonfly 
* retro
* whitey

To change a theme, locate the line below in your $HOME/.config/qtile/config.py file:

```colors, backgroundColor, foregroundColor, workspaceColor, chordColor = colors.redcore()```

Change the last word in that line to the color scheme you'd like to use.

## Changing the bar position

You can easily change the bar position by changing the word bottom to the word top in this line:

```Screen(bottom=bar.Bar(widgets=widgets_list, size=30, background=backgroundColor, margin=0, opacity=0.8),),```


# Credits

* Contributed by Matt Weber AKA [The Linux Cast](https://youtube.com/thelinuxcast).
* Original Design inspiration from Jeff Winget.
* Fonts from Nerd Fonts

