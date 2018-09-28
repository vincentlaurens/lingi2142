#!/bin/bash

# Take an argument which the commit message version


if $# != 1
then
	echo "You should enter only 1 argument!!!"
else
	echo "git commit -m $1"
	git commit -m $1

	git push https://github.com/vincentlaurens/lingi2142.git master
fi
