#!/bin/sh

killbrowser() {
	ps aux | grep -i librewolf | grep -i marionette | cut -d ' ' -f 1 | xargs kill
}

#rm -rf ./marionette.sock
killbrowser
sleep 2

flatpak run io.gitlab.librewolf-community -P marionette --marionette &
#sleep 2
#socat UNIX-LISTEN:./marionette.sock TCP:localhost:2828

#sleep 2
#killbrowser
#sleep 2

#exit 0

# in container:
#socat TCP-LISTEN:2828,fork UNIX-CONNECT:./marionette.sock
# also put ,fork after unix-listen
