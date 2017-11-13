#!/bin/bash

# This script should be initiated inside the go src path of grafana!
# For more information on building grafana "the grafana-way" see
# https://github.com/grafana/grafana-packer.

sudo apt install golang npm gem ruby ruby-dev
sudo npm install -g yarn

# This fails on ppc64el, since fpm isn't available on that platform.
sudo gem install fpm -v 1.4

go run build.go build
yarn install

# Because we don't have fpm on ppc64el the following step fails
# horible on this architecture.
go run build.go pkg-deb latest
