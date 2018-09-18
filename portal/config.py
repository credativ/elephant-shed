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
        {"address":"localhost:4433"},
        {"address":"localhorst"},
        {"address":"127.0.0.1:4433"},
        ]

# Lefthand-Side Navigation to the most important links.
navigation=[
        {"url" :"/", "label" :"Home"},
        {"url" :"/", "label" :"Support"},
        {"url" :"/", "label" :"elephantshed.io"},
        {"url" :"/", "label" :"postgresql.org"}, 
        ]

# Detail-views deeplinks to elephant-shed components for a given cluster.
deeplinks=[
        {"url" :"/", "label" : "Monitoring", "image": "button_grafana.png"},
        {"url" :"/", "label" : "Administration", "image": "button_pgadmin.png"},
        {"url" :"/", "label" : "Reports", "image": "button_pgbadger.png"},
        {"url" :"/", "label" : "Metrics", "image": "button_prometheus.png"},
        {"url" :"/", "label" : "Backups", "image": "button_pgbackrest.png"},
        {"url" :"/", "label" : "Shell", "image": "button_shellinabox.png"},
        {"url" :"/", "label" : "Cockpit", "image": "button_cockpit.png"},
        {"url" :"/", "label" : "Documentation", "image": "button_doc.png"},


        ]
