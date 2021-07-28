
# Installation

Elephant Shed consists of the following Debian packages and their dependencies:

  * `elephant-shed`:
    Metapackage that includes the following packages.
  * `elephant-shed-prometheus`:
    Configuration files and helper scripts for Prometheus and its exporters.
  * `elephant-shed-cockpit`:
    Configuration files for cockpit and cockpit-ws.
  * `elephant-shed-grafana`:
    Preconfigured Prometheus datasource and dashboard that includes various system
    and PostgreSQL metrics.
  * `elephant-shed-omnidb`:
    Configuration files for OmniDB.
  * `elephant-shed-pgbackrest`:
    Systemd service files and generators, helper scripts and preset configuration.
  * `elephant-shed-pgbadger`:
    Systemd service files, generators and helper scripts.
  * `elephant-shed-portal`:
    Elephant Shed web portal including Apache configuration.
  * `elephant-shed-postgresql`:
    Additional preset configuration files for PostgreSQL.
  * `elephant-shed-shellinabox`:
    Shell In A Box configuration files.
  * `elephant-shed-tmate`:
    Preconfigured tmate installation for easier support.

## Package Installation

Prebuilt packages are available from <https://packages.credativ.com/public/postgresql/>.

The repository also contains packages that the `elephant-shed` packages depend
on. This includes packages for Grafana, Cockpit and various python libraries.

### Installation on Debian and Ubuntu

```
# Install tools
sudo apt-get install curl ca-certificates apt-transport-https

# Use official PostgreSQL repo, apt.postgresql.org
echo "deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main" | sudo tee -a /etc/apt/sources.list.d/pgdg.list
curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Use credativ repo, packages.credativ.com
echo "deb https://packages.credativ.com/public/postgresql/ stretch-stable main" | sudo tee -a /etc/apt/sources.list.d/elephant-shed.list
curl https://packages.credativ.com/public/postgresql/aptly.key | sudo apt-key add -

# Install elephant-shed
sudo apt-get update
sudo apt-get install elephant-shed

# Choose desired PostgreSQL versions to install
sudo apt-get install postgresql-10

# Every user in the group "elephant-shed" is allowed to login at the portal
# Add all needed users to this group
sudo adduser <USERNAME> elephant-shed
```

### Installation on RedHat and CentOS

Elephant Shed works with the PostgreSQL packages from the PostgreSQL RPM building project.
Go to <a href="https://yum.postgresql.org/"><b>yum.postgresql.org</b></a> and
install the repository RPMs for the PostgreSQL versions you want to use.
Then proceed to install Elephant Shed as below.

```bash
# Use credativ repository (will also pull in EPEL)
sudo yum install https://packages.credativ.com/public/postgresql/yum/credativ-repo.rpm

# On RedHat, activate additional repositories (not on CentOS)
subscription-manager repos --enable=rhel-7-server-extras-rpms
subscription-manager repos --enable=rhel-7-server-optional-rpms

# Choose desired PostgreSQL versions to install
sudo yum install postgresql11-server postgresql11-contrib postgresql-common
sudo pg_createcluster 11 main --start

# Install elephant-shed
sudo yum install elephant-shed

# Every user in the group "elephant-shed" is allowed to login at the portal
# Add all needed users to this group
sudo vigr

# Unfortunately, shellinabox does not work with SELinux enabled
# Disable SELinux if you want to use this component
sudo setenforce 0
sudo sed -i -e 's/^SELINUX=.*/SELINUX=permissive/' /etc/selinux/config
```

## Installation from source

The source code is available on GitHub: <https://github.com/credativ/elephant-shed>

### Build Debian Packages

All Elephant Shed Debian packages can be built using the command `make deb`.

Requirements:

  - `dpkg-dev`
  - `devscripts`

### Build Documentation

To build the documentation in HTML format type `make docs`.

Requirements:

  - `sphinx`

### Create Testsystem with Vagrant

The `make vagrant` command builds all components, creates a new virtual machine using Vagrant and deploys the software using Ansible.
This can also be used to redeploy a already running machine.

The Vagrant configuration is located in `vagrant/Vagrantfile`.

Requirements:

  - `vagrant`
  - `virtualbox` or `libvirt`
  - `ansible`

### Deploy on remote machine

To deploy the software on any machine, enter the connection information in the inventory `vagrant/inventory`.
The deployment can than be started with the following command `make ansible`.

Requirements:

  - `ansible`
