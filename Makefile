README = README.md

all: grafana_prepare_dashboard

sphinx:
	$(MAKE) -C doc html

docs: sphinx

doc: docs

deb:
	dpkg-buildpackage -us -uc
	lintian | tee -a lintian.log

grafana_prepare_dashboard:
	$(MAKE) -C grafana

upload_packages: deb
	aptly/upload_packages.sh

include_packages:
	aptly/include_packages.sh

publish_packages:
	aptly/publish_packages.sh

vagrant: deb
	cd vagrant && vagrant up --provision

ansible: deb
	cd vagrant && ./elephant-shed.yml $(ANSIBLE_ARGS)

deploy_openpower: vagrant/inventory.openpower
	cd vagrant && ./elephant-shed.yml $(ANSIBLE_ARGS) \
	  -i inventory.openpower \
	  -e "repo=http"

clean:
	rm -f README.html README.pdf
	$(MAKE) -C doc clean
	$(MAKE) -C grafana clean
