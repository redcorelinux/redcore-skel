#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $@&
  fi
}


dunst &

#starting utility applications at boot time
picom --vsync &
/usr/libexec/polkit-gnome-autentication-agent-1 &
#/usr/lib/xfce4/notifyd/xfce4-notifyd &
~/.fehbg &
