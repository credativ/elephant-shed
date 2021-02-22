# Intro
Elephant Shed is a web-based PostgreSQL management front-end that bundles
several utilities and applications for use with PostgreSQL. It currently
manages single-node Debian/Ubuntu PostgreSQL servers and appliances.

The main components are:

* PostgreSQL - <https://www.postgresql.org/>
* OmniDB - <https://omnidb.org/>
* postgresql-common - <https://anonscm.debian.org/cgit/pkg-postgresql/postgresql-common.git>
* pgBadger - <http://dalibo.github.io/pgbadger/>
* pgBackRest - <http://www.pgbackrest.org/>
* Grafana - <https://grafana.com/>
* Prometheus - <https://prometheus.io/>
* Cockpit - <http://cockpit-project.org/>
* Shell In A Box - <https://github.com/shellinabox/shellinabox>

In addition several other tools are included for configuration management and setup.

The number of components bundled and tasks handled add some overhead compared
to running just the database server. It is therefore only recommended for
adequately sized systems.

This document describes the current version.
Updated versions of this document will be shipped with the elephant-shed packages and can be found in `/usr/share/doc/elephant-shed-portal` (`/usr/share/doc/elephant-shed*`) and in the web portal under <https://your-server/doc/>.
