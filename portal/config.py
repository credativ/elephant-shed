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
        #{"address":"localhost"},
        {"address":"127.0.0.1"},
        ]

detailview_systeminformation=[
        {"label" : "HostFQDN",      "data" : "pg_hostname pg_fqdn"},
        {"label" : "CpuCount",  "formoverride" : '<span class="pg_cpu_config pg_cpu_count pg_addgraph"></span>'},
        {"label" : "OS",        "data" : "pg_uname pg_0"},
        {"label" : "Memory",       "formoverride": '<span class="pg_virtual_memory pg_available pg_addgraph"></span> (<span class="pg_virtual_memory pg_percent"></span>% Used)'}, 
        ]

detailview_clusterinformation=[
        {"label" : "shared_buffers",  "data" : "pg_config pg_shared_buffers" },
        {"label" : "max_connections",  "data" : "pg_config pg_max_connections"},
        {"label" : "wal-level",  "data" : "pg_config pg_wal_level"},
        {"label" : "max-wal-size",  "data" : "pg_config pg_max_wal_size"},
        {"label" : "synchronous_commit",  "data" : "pg_config pg_synchronous_commit"},
        {"label" : "data_directory",  "data" : "pg_config pg_data_dir"},
        {"label" : "JIT",  "data" : "pg_config pg_jit"},
        {"label" : "max_parallel_workers_per_gather",  "data" : "pg_config pg_max_parallel_workers_per_gather"},
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
        {"url" :"/grafana/", "label" : "Monitoring", "image": "button_grafana.png"},
        {"url" :"/pgadmin4/browser", "label" : "Administration", "image": "button_pgadmin.png"},
        {"url" :"/prometheus/", "label" : "Reports", "image": "button_pgbadger.png"},
        {"url" :"/pgbadger/", "label" : "Metrics", "image": "button_prometheus.png"},
        {"url" :"/", "label" : "Backups TODO", "image": "button_pgbackrest.png"},
        {"url" :"/shellinabox/", "label" : "Shell", "image": "button_shellinabox.png"},
        {"url" :"/system", "label" : "Cockpit", "image": "button_cockpit.png"},
        {"url" :"/doc/html/", "label" : "Documentation", "image": "button_doc.png"},


        ]
