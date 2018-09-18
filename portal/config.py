debug=True
usemin=False
appkey="TEST"
application_root = "/portal"
hosts=[
        {"address":"localhost:4433"},
        {"address":"localhorst"},
        {"address":"127.0.0.1:4433"},
        ]

navigation=[
        {"url" :"/", "label" :"Home"},
        {"url" :"/", "label" :"Support"},
        {"url" :"/", "label" :"elephantshed.io"},
        {"url" :"/", "label" :"postgresql.org"}, 
        ]

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
