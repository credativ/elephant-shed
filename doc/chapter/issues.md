# Known Bugs and Issues

## PostgreSQL

  * The `prometheus-sql-exporter` monitoring agent is permanently keeping
    connections open to all databases, which prevents `DROP DATABASE` from
    working. To drop databases, stop `prometheus-sql-exporter` first.
    This is possible via the web interface Cockpit: [services#/prometheus-sql-exporter.service](/system/services#/prometheus-sql-exporter.service).

## OmniDB

  * OmniDB does not use PAM authentication.

## Portal

  * A direct relogin after a logout does not work. Reloading the page is necessary.

## RedHat / CentOS

  * shellinabox does not work when SELinux is enabled.
