postgresql_server_overview.json: postgresql_server_overview.json.in
	# Replace or placeholder (${DS_PROMETHEUS}) by prometheus. We don't
	# import the dashboard via the web interface so this is necessary.
	sed 's;$${DS_PROMETHEUS};prometheus;g' < $< > postgresql_server_overview.json

clean:
	rm -f postgresql_server_overview.json
