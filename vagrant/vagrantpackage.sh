#!/bin/sh

rm -vf elephant-shed.box

vagrant package --vagrantfile Vagrantfile.template --output elephant-shed.box
