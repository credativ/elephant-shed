README = README.md
READMECSS = pandoc.css

all: grafana_prepare_dashboard

README.html: $(README) $(READMECSS)
	pandoc --number-sections --table-of-contents --toc-depth 2 -s -H $(READMECSS) $(README) > $@

README.pdf: $(README) $(READMECSS)
	pandoc --number-sections $(README) -o $@

README: README.html README.pdf

docs: README

doc: docs

deb:
	dpkg-buildpackage -us -uc
	lintian | tee -a lintian.log

grafana_prepare_dashboard: grafana/postgresql_server_overview.json.in
	# We need to modify the saved dashboard.
	#jq ".dashboard.id=null | .overwrite=true | .meta.updatedBy=\"credativ GmbH\" | .meta.createdBy=\"credativ GmbH\"" $< > grafana/postgresql_server_overview.json
	# Replace or placeholder (${DS_PROMETHEUS}) by prometheus. We
	# don't import the dashboard via the web interface so this is
	# nessasary.
	cat $< | sed 's;$${DS_PROMETHEUS};prometheus;g' > grafana/postgresql_server_overview.json

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
	rm -f README.html README.pdf grafana/postgresql_server_overview.json
