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
        {"label" : "CpuCount",  "data" : "pg_cpu_config pg_cpu_count"},
        {"label" : "OS",        "data" : "pg_uname pg_0"},
        {"label" : "Memory",       "formoverride": '<span class="pg_virtual_memory pg_available"></span> (<span class="pg_virtual_memory pg_percent"></span>% Used)'}, 
        ]

detailview_clusterinformation=[
        {"label" : "Shared_Buffers",  "data" : "pg_config pg_shared_buffers",
                                "formoverride" : '<font color="red"><span class="pg_config pg_shared_buffers"></span></font>'},
        {"label" : "Max_Connections",  "data" : "pg_config pg_max_connections"},
        {"label" : "Wal-Level",  "data" : "pg_config pg_wal_level"},
        {"label" : "Max-Wal-Size",  "data" : "pg_config pg_max_wal_size"},
        {"label" : "Synchronous_Commit",  "data" : "pg_config pg_synchronous_commit"},
        {"label" : "Data_Directory",  "data" : "pg_config pg_data_dir"},
        {"label" : "JIT",  "data" : "pg_config pg_jit"},
        {"label" : "Max_Parallel_Workers_Per_Gather",  "data" : "pg_config pg_max_parallel_workers_per_gather"},
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
