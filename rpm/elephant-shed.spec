Name:           elephant-shed
Version:        %{version}
Release:        1%{?dist}
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
#Requires: adduser
Requires: httpd
Requires: mod_ssl
Requires: mod_authnz_pam
Requires: mod_authz_unixgroup
Requires: perl-Template-Toolkit
#Requires: libcgi-pm-perl
%description -n elephant-shed-portal
The Elephant Shed is a web-based PostgreSQL management front-end.
This package provides the web interface.

%package -n elephant-shed-postgresql
Requires: adduser
Requires: postgresql-common >= 183
Summary: PostgreSQL dashboard -- PostgreSQL integration
%description -n elephant-shed-postgresql
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with PostgreSQL.

%package -n elephant-shed-pgadmin4
Requires: pgadmin4-apache2
Summary: PostgreSQL dashboard -- pgAdmin4 integration
%description -n elephant-shed-pgadmin4
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This meta package provides the integration with pgAdmin4.

%package -n elephant-shed-pgbadger
Requires: pgbadger >= 9
Requires: postgresql-common
Summary: PostgreSQL dashboard -- pgBadger integration
%description -n elephant-shed-pgbadger
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with pgBadger.

%package -n elephant-shed-pgbackrest
Requires: pgbackrest
Requires: postgresql-common
Summary: PostgreSQL dashboard -- pgBackRest integration
%description -n elephant-shed-pgbackrest
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with pgBackRest.

%package -n elephant-shed-grafana
Requires: curl
Requires: grafana >= 5
Summary: PostgreSQL dashboard -- Grafana integration
%description -n elephant-shed-grafana
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with Grafana.

%package -n elephant-shed-prometheus
Requires: prometheus >= 2.0
Summary: PostgreSQL dashboard -- Prometheus integration
%description -n elephant-shed-prometheus
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with Prometheus.

%package -n elephant-shed-prometheus-node-exporter
Requires: prometheus-node-exporter >= 0.15.0
Summary: PostgreSQL dashboard -- Node exporter integration
%description -n elephant-shed-prometheus-node-exporter
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with the Prometheus node
 exporter.

%package -n elephant-shed-prometheus-sql-exporter
Requires: libyaml-perl
Requires: postgresql-common
Requires: prometheus-sql-exporter
Summary: PostgreSQL dashboard -- SQL exporter integration
%description -n elephant-shed-prometheus-sql-exporter
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This package provides the integration with the Prometheus SQL
 exporter.

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
systemctl enable cockpit.socket
systemctl start cockpit.socket

%package -n elephant-shed-shellinabox
Requires: shellinabox
Summary: PostgreSQL dashboard -- shellinabox integration
%description -n elephant-shed-shellinabox
 The Elephant Shed is a web-based PostgreSQL management front-end.
 .
 This meta package provides the integration with shellinabox.

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
        test -e $file || continue
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
  %{buildroot}/etc/httpd/conf.d/elephant-shed.conf
# load authnz_pam (it doesn't do that by itself)
mkdir -p %{buildroot}/etc/httpd/conf.modules.d
cp rpm/56-authnz_pam.conf %{buildroot}/etc/httpd/conf.modules.d
echo /etc/httpd/conf.modules.d/56-authnz_pam.conf >> files-elephant-shed-portal
# update PAM file
cat > %{buildroot}/etc/pam.d/apache <<EOF
#%PAM-1.0
auth		include		password-auth
account		include		password-auth
EOF

%files -n elephant-shed-portal                   -f files-elephant-shed-portal
%files -n elephant-shed-postgresql               -f files-elephant-shed-postgresql
#%files -n elephant-shed-pgadmin4                -f files-elephant-shed-pgadmin4
%files -n elephant-shed-pgbadger                 -f files-elephant-shed-pgbadger
%files -n elephant-shed-pgbackrest               -f files-elephant-shed-pgbackrest
%files -n elephant-shed-grafana                  -f files-elephant-shed-grafana
%files -n elephant-shed-prometheus               -f files-elephant-shed-prometheus
%files -n elephant-shed-prometheus-node-exporter -f files-elephant-shed-prometheus-node-exporter
%files -n elephant-shed-prometheus-sql-exporter  -f files-elephant-shed-prometheus-sql-exporter
%files -n elephant-shed-cockpit                  -f files-elephant-shed-cockpit
#%files -n elephant-shed-shellinabox             -f files-elephant-shed-shellinabox
%files -n elephant-shed-tmate                    -f files-elephant-shed-tmate
