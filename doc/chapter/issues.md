# Known Bugs and Issues

## PostgreSQL

  * The `prometheus-sql-exporter` monitoring agent is permanently keeping
    connections open to all databases, which prevents `DROP DATABASE` from
    working. To drop databases, stop `prometheus-sql-exporter` first.
    This is possible via the web interface Cockpit: [services#/prometheus-sql-exporter.service](/system/services#/prometheus-sql-exporter.service).

## pgadmin4

  * pgadmin4 does not use PAM authentication.
  * By default, pgadmin4 does not show local databases.

## Portal

  * A direct relogin after a logout does not work. Reloading the page is necessary.

## RedHat / CentOS

  * pgAdmin4 does not work when SELinux is enabled.
  * shellinabox does not work when SELinux is enabled.
