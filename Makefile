# Default git branch to build in RPM
ifndef GITBRANCH
GITBRANCH=HEAD
endif

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
	rm -rf rpm/SOURCES/ rpm/SPECS rpm/BUILD rpm/BUILDROOT rpm/RPMS rpm/SRPMS

# rpm

DPKG_VERSION=$(shell sed -ne '1s/.*(//; 1s/).*//p' debian/changelog)
GIT_COMMITS=$(shell git log --oneline | wc -l)
RPMDIR=$(CURDIR)/rpm/
TARBALL=$(RPMDIR)/SOURCES/elephant-shed_$(DPKG_VERSION).tar.xz

rpmbuild: $(TMATESOURCE) $(TARBALL)
	rpmbuild -D"%_topdir $(RPMDIR)" --define='package_version $(DPKG_VERSION)' --define='package_release $(GIT_COMMITS)' -ba rpm/elephant-shed.spec

$(TARBALL):
	mkdir -p $(dir $(TARBALL))
	git archive --prefix=elephant-shed-$(DPKG_VERSION)/ $(GITBRANCH) | xz > $(TARBALL)

# tmate rpm

TMATESOURCE=$(CURDIR)/rpm/SOURCES/$(shell rpmspec --srpm --query --queryformat '%{Source}' rpm/tmate.spec)

rpmbuild-tmate: $(TMATESOURCE)
	rpmbuild -D"%_topdir $(RPMDIR)" --define='package_version $(DPKG_VERSION)' -ba rpm/tmate.spec

$(TMATESOURCE):
	mkdir -p rpm/SOURCES
	spectool -S -g -C rpm/SOURCES rpm/tmate.spec
