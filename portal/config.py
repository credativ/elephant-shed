#######
debug=True                      # Enable this to flip flasks internal debug-mode.
                                # Greatly slows down the system but allows for on-line
                                # Reload of templates.

usemin=False                    # Use Minified versions of JS-Libraries where available.

appkey="TEST"                   # App-Key for encryption. Change in production.

application_root = "/portal"    # Root-Folder this application resides in.
                                # Should match with apache.conf.

# Hosts we consider beeing part of a Cluster.
hosts=[
        {"address":"localhost"},
        {"address":"localhost"},
        ]

detailview_systeminformation=[
        {"label" : "Hostname (FQDN)",      "data" : "pg_hostname pg_fqdn"},
        {"label" : "VCPU Count",  "data" : "pg_cpu_config pg_cpu_count_logical"},
        {"label" : "Kernel",        "formoverride" : '<span class="pg_uname pg_kernel_name"></span> <span class="pg_uname pg_kernel_version"</span> <span class="pg_uname pg_machine"></span>'},
        {"label" : "Load Average",  "formoverride" : '<span class="pg_load pg_15min pg_addgraph"></span>'},
        {"label" : "vFS Cache", "data": 'pg_virtual_memory pg_cached pg_addgraph'}, 
        {"label" : "Memory Active",       "data": 'pg_virtual_memory pg_used pg_addgraph'},
        {"label" : "Memory Shared",       "data": 'pg_virtual_memory pg_shared pg_addgraph'},        
        {"label" : "Disk Usage (%)", "data" : "pg_disk_usage pg__s_ pg_percent"},


        ]

detailview_clusterinformation=[
        #{"label" : "data_directory",  "data" : "pg_config pg_data_directory"},
        {"label" : "listen_addresses",  "data" : "pg_config pg_listen_addresses" },
        {"label" : "port",  "data" : "pg_config pg_port" },
        {"label" : "shared_buffers",  "data" : "pg_config pg_shared_buffers" },
        {"label" : "max_connections",  "data" : "pg_config pg_max_connections"},
        {"label" : "work_mem",  "data" : "pg_config pg_work_mem"},
        {"label" : "wal_level",  "data" : "pg_config pg_wal_level"},
        {"label" : "max_wal_size",  "data" : "pg_config pg_max_wal_size"},
        {"label" : "synchronous_commit",  "data" : "pg_config pg_synchronous_commit"},
        ]




# Lefthand-Side Navigation to the most important links.
navigation=[
        #{"url" :"/", "label" :"Home"},
        #{"url" :"/", "label" :"Support"},
        #{"url" :"/", "label" :"elephantshed.io"},
        #{"url" :"/", "label" :"postgresql.org"}, 
        ]

# Detail-views deeplinks to elephant-shed components for a given cluster.
deeplinks=[
        {"url" :":4433/grafana/", "label" : "Monitoring", "image": "button_grafana.png"},
        {"url" :":4433/pgadmin4/browser", "label" : "Administration", "image": "button_pgadmin.png"},
        {"url" :":4433/pgbadger/", "label" : "Reports", "image": "button_pgbadger.png"},
        # {"url" :":4433/prometheus/", "label" : "Metrics", "image": "button_prometheus.png"},
        # {"url" :":4433/", "label" : "Backups TODO", "image": "button_pgbackrest.png"},
        {"url" :":4433/shellinabox/", "label" : "Shell", "image": "button_shellinabox.png"},
        {"url" :":4433/system", "label" : "Cockpit", "image": "button_cockpit.png"},
        {"url" :":4433/doc/html/", "label" : "Documentation", "image": "button_doc.png"},


        ]
