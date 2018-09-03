all: docs

doc docs:
	$(MAKE) -C doc html

deb:
	dpkg-buildpackage -us -uc
	lintian | tee -a lintian.log

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
	$(MAKE) -C doc clean
	$(MAKE) -C grafana clean

# rpm

DPKG_VERSION=$(shell sed -ne '1s/.*(//; 1s/).*//p' debian/changelog)
RPMDIR=$(HOME)/rpmbuild
TARBALL=$(RPMDIR)/SOURCES/elephant-shed_$(DPKG_VERSION).tar.xz

rpmbuild: $(TARBALL)
	rpmbuild --define='version $(DPKG_VERSION)' -ba rpm/elephant-shed.spec

$(TARBALL):
	mkdir -p $(dir $(TARBALL))
	git archive --prefix=elephant-shed-$(DPKG_VERSION)/ HEAD | xz > $(TARBALL)
