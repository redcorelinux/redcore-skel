#!/bin/bash

set_wallpaper() {
	if [[ "$(loginctl show-session "$XDG_SESSION_ID" -p Type --value)" != wayland ]]; then
		if [[ -x /usr/bin/feh ]] ; then # x11
			/usr/bin/feh --bg-scale /usr/share/backgrounds/redcore-community/0.png & disown
		fi
	else
		if [[ -x /usr/bin/swaybg ]] ; then # wayland
			/usr/bin/swaybg --image /usr/share/backgrounds/redcore-community/0.png & disown
		fi
	fi
}

start_polkit_agent() {
	if [[ -x /usr/libexec/polkit-kde-authentication-agent-1 ]] ; then
		pkill -f /usr/libexec/polkit-kde-authentication-agent-1
		/usr/libexec/polkit-kde-authentication-agent-1 & disown
	elif [[ -x /usr/libexec/polkit-gnome-authentication-agent-1 ]] ; then
		pkill -f /usr/libexec/polkit-gnome-authentication-agent-1
		/usr/libexec/polkit-gnome-authentication-agent-1 & disown
	fi
}

start_notification_daemon() {
	if [[ -x /usr/bin/dunst ]] ; then
		pkill -f dunst
		/usr/bin/dunst & disown
	fi
}

start_compositor() {
	if [[ "$(loginctl show-session "$XDG_SESSION_ID" -p Type --value)" != wayland ]]; then
		if [[ -x /usr/bin/picom ]] ; then # x11
			pkill -f picom
			/usr/bin/picom --vsync & disown
		fi
	fi
}

start_nm-applet() {
	if [[ -x /usr/bin/nm-applet ]] ; then
		pkill -f nm-applet
		/usr/bin/nm-applet & disown
	fi
}

start_pipewire() {
	if [[ -x /usr/bin/gentoo-pipewire-launcher ]] ; then
		/usr/bin/gentoo-pipewire-launcher restart
	fi
}

start_xdg-desktop-portal() {
	if [[ -x /usr/libexec/xdg-desktop-portal-wlr ]] ; then
		pkill -f xdg-desktop-portal-wlr
		/usr/libexec/xdg-desktop-portal-wlr & disown
	fi
}

main() {
	set_wallpaper
	start_polkit_agent
	start_notification_daemon
	start_compositor
	start_nm-applet
	start_pipewire
	start_xdg-desktop-portal
}

main
