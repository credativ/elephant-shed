Name:           elephant-shed
Version:        %{package_version}
Release:        3%{?dist}
BuildArch:      noarch
Summary:        PostgreSQL dashboard
Packager:       Debian PostgreSQL Maintainers <pkg-postgresql-public@lists.alioth.debian.org>
License:        GPLv3+
URL:            https://packages.debian.org/sid/%{name}
Source0:        http://ftp.debian.org/debian/pool/main/p/%{name}/%{name}_%{version}.tar.xz
BuildRequires:  python-sphinx
Requires: elephant-shed-cockpit
Requires: elephant-shed-grafana
Requires: elephant-shed-pgadmin4
Requires: elephant-shed-pgbackrest
Requires: elephant-shed-pgbadger
Requires: elephant-shed-portal
Requires: elephant-shed-postgresql
Requires: elephant-shed-prometheus
Requires: elephant-shed-prometheus-node-exporter
Requires: elephant-shed-prometheus-sql-exporter
Requires: elephant-shed-shellinabox
Requires: elephant-shed-tmate

%description
The Elephant Shed is a web-based PostgreSQL management front-end.
This meta package depends on all Elephant Shed components.

%package -n elephant-shed-portal
Summary: PostgreSQL dashboard -- web interface
Requires: shadow-utils
Requires: httpd
Requires: mod_ssl
#Requires: mod_authnz_pam
Requires: mod_authnz_external
Requires: pwauth
Requires: mod_authz_unixgroup
Requires: perl-Template-Toolkit
#Requires: libcgi-pm-perl
%description -n elephant-shed-portal
The Elephant Shed is a web-based PostgreSQL management front-end.
This package provides the web interface.
%post -n elephant-shed-portal
groupadd --system elephant-shed || :
systemctl enable httpd
systemctl restart httpd

%package -n elephant-shed-postgresql
Requires: shadow-utils
Requires: postgresql-common >= 183
Summary: PostgreSQL dashboard -- PostgreSQL integration
%description -n elephant-shed-postgresql
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with PostgreSQL.

%post -n elephant-shed-postgresql

sed -i -e 's/use C as lc_messages/use en_US as lc_messages/i;s/C\.UTF-8/en_US\.UTF-8/' \
/etc/postgresql-common/createcluster.d/elephant-shed.conf

%package -n elephant-shed-pgadmin4

Requires: pgadmin4-web
Summary: PostgreSQL dashboard -- pgAdmin4 integration
%description -n elephant-shed-pgadmin4
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This meta package provides the integration with pgAdmin4.
%post -n elephant-shed-pgadmin4
test -f /etc/httpd/conf.d/pgadmin4.conf || cp /etc/httpd/conf.d/pgadmin4.conf.sample /etc/httpd/conf.d/pgadmin4.conf
systemctl restart httpd
install -d -o apache -g apache /var/lib/pgadmin /var/log/pgadmin
su apache -c "PGADMIN_SETUP_EMAIL=admin@localhost PGADMIN_SETUP_PASSWORD=admin python /usr/lib/python2.7/site-packages/pgadmin4-web/setup.py" -s /bin/bash

%package -n elephant-shed-pgbadger
Requires: pgbadger >= 9
Requires: postgresql-common
Summary: PostgreSQL dashboard -- pgBadger integration
%description -n elephant-shed-pgbadger
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with pgBadger.
%post -n elephant-shed-pgbadger
install -d -o postgres -g postgres /var/lib/pgbadger
systemctl daemon-reload
systemctl enable pgbadger.timer
systemctl start pgbadger.timer
systemctl start pgbadger

%package -n elephant-shed-pgbackrest
Requires: pgbackrest
Requires: postgresql-common
Summary: PostgreSQL dashboard -- pgBackRest integration
%description -n elephant-shed-pgbackrest
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with pgBackRest.
%post -n elephant-shed-pgbackrest
systemctl daemon-reload
install -d -o postgres -g postgres /var/lib/pgbackrest /var/www/html/pgbackrest
chown postgres: /etc/pgbackrest.conf

%package -n elephant-shed-grafana
Requires: curl
Requires: grafana >= 5
Summary: PostgreSQL dashboard -- Grafana integration
%description -n elephant-shed-grafana
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with Grafana.
%post -n elephant-shed-grafana
systemctl daemon-reload
systemctl enable grafana-server.service
systemctl start grafana-server.service

%package -n elephant-shed-prometheus
Requires: prometheus2
Summary: PostgreSQL dashboard -- Prometheus integration
%description -n elephant-shed-prometheus
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with Prometheus.
%post -n elephant-shed-prometheus
systemctl daemon-reload
systemctl enable prometheus
systemctl start prometheus

%package -n elephant-shed-prometheus-node-exporter
Requires: node_exporter >= 0.16.0
Summary: PostgreSQL dashboard -- Node exporter integration
%description -n elephant-shed-prometheus-node-exporter
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with the Prometheus node
 exporter.
%post -n elephant-shed-prometheus-node-exporter
systemctl daemon-reload
systemctl enable node_exporter
systemctl start node_exporter

%package -n elephant-shed-prometheus-sql-exporter
Requires: perl-YAML
Requires: postgresql-common
Requires: sql_exporter
Summary: PostgreSQL dashboard -- SQL exporter integration
%description -n elephant-shed-prometheus-sql-exporter
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with the Prometheus SQL
 exporter.
%post -n elephant-shed-prometheus-sql-exporter
systemctl daemon-reload
systemctl enable prometheus-sql-exporter
systemctl start prometheus-sql-exporter
systemctl enable prometheus-sql-exporter-restart.timer
systemctl start prometheus-sql-exporter-restart.timer

%package -n elephant-shed-cockpit
Requires: cockpit
Requires: cockpit-packagekit
Summary: PostgreSQL dashboard -- cockpit integration
%description -n elephant-shed-cockpit
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with cockpit.
%post -n elephant-shed-cockpit
systemctl daemon-reload
# create /run/cockpit
systemd-tmpfiles --create
# allow cockpit to use port 10090
semanage port -a -t websm_port_t -p tcp 10090
# allow apache to connect to any port
setsebool -P httpd_can_network_connect true
systemctl enable cockpit.socket
systemctl start cockpit.socket

%package -n elephant-shed-shellinabox
Requires: shellinabox
Summary: PostgreSQL dashboard -- shellinabox integration
%description -n elephant-shed-shellinabox
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This meta package provides the integration with shellinabox.
%post -n elephant-shed-shellinabox
systemctl daemon-reload
systemctl enable shellinaboxd
systemctl start shellinaboxd

%package -n elephant-shed-tmate
Requires: tmate
Summary: PostgreSQL dashboard -- tmate integration
%description -n elephant-shed-tmate
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with tmate.

%prep
# unpack tarball, ignoring the name of the top level directory inside
%setup -c
mv */* .

%build
#make

%install
rm -rf %{buildroot}
# install in subpackages using the Debian files
for inst in debian/*.install; do
    pkg=$(basename $inst .install)
    echo "### Reading $pkg files list from $inst ###"
    while read file dir; do
        [ "$file" = "doc/_build/html" ] && continue
        case $file in
          portal/cgi-bin) dir="var/www" ;;
          portal/elephant-shed.conf) dir="etc/httpd/conf.d" ;;
        esac
        mkdir -p %{buildroot}/$dir
        cp -r $file %{buildroot}/$dir
        echo "/$dir/${file##*/}" >> files-$pkg
    done < $inst
done

# update httpd paths for CentOS
sed -i -e 's!SSLCertificateFile.*!SSLCertificateFile /etc/pki/tls/certs/localhost.crt!' \
       -e 's!SSLCertificateKeyFile.*!SSLCertificateKeyFile /etc/pki/tls/private/localhost.key!' \
       -e 's!ErrorLog.*!ErrorLog /var/log/httpd/error_log!' \
       -e 's!CustomLog.*!CustomLog /var/log/httpd/access_log combined!' \
       -e 's!Header edit.*Content-Security-Policy.*!#&!' \
       -e '/Header unset Content-Security-Policy/s/#//' \
       -e 's!AuthBasicProvider.*!AuthBasicProvider external!' \
       -e 's!AuthPAMService.*!AuthExternal pwauth!' \
       -e '/VirtualHost.*:443/a DefineExternalAuth pwauth pipe \/usr\/bin\/pwauth' \
  %{buildroot}/etc/httpd/conf.d/elephant-shed.conf
# load authnz_external (it doesn't do that by itself)
mkdir -p %{buildroot}/etc/httpd/conf.modules.d
cp rpm/56-authnz_external.conf %{buildroot}/etc/httpd/conf.modules.d
echo /etc/httpd/conf.modules.d/56-authnz_external.conf >> files-elephant-shed-portal
# update PAM file
cat > %{buildroot}/etc/pam.d/apache <<EOF
#%PAM-1.0
auth		include		password-auth
account		include		password-auth
EOF

# prometheus2.rpm uses a different variable for extra arguments
# preserve storage.tsdb.path from /etc/default/prometheus
sed -i -e 's!^ARGS="!PROMETHEUS_OPTS="--storage.tsdb.path=/var/lib/prometheus/data !' %{buildroot}/etc/default/elephant-shed-prometheus

# node exporter service is named differently on CentOS, and uses a different variable for extra arguments
mv %{buildroot}/etc/systemd/system/prometheus-node-exporter.service.d %{buildroot}/etc/systemd/system/node_exporter.service.d
sed -i -e 's!prometheus-node-exporter.service.d!node_exporter.service.d!' files-elephant-shed-prometheus-node-exporter
sed -i -e 's!^ARGS=!NODE_EXPORTER_OPTS=!' %{buildroot}/etc/default/elephant-shed-prometheus-node-exporter

%files -n elephant-shed-portal                   -f files-elephant-shed-portal
%files -n elephant-shed-postgresql               -f files-elephant-shed-postgresql
%files -n elephant-shed-pgadmin4
%files -n elephant-shed-pgbadger                 -f files-elephant-shed-pgbadger
%files -n elephant-shed-pgbackrest               -f files-elephant-shed-pgbackrest
%files -n elephant-shed-grafana                  -f files-elephant-shed-grafana
%files -n elephant-shed-prometheus               -f files-elephant-shed-prometheus
%files -n elephant-shed-prometheus-node-exporter -f files-elephant-shed-prometheus-node-exporter
%files -n elephant-shed-prometheus-sql-exporter  -f files-elephant-shed-prometheus-sql-exporter
%files -n elephant-shed-cockpit                  -f files-elephant-shed-cockpit
%files -n elephant-shed-shellinabox
%files -n elephant-shed-tmate                    -f files-elephant-shed-tmate
%files -n elephant-shed
