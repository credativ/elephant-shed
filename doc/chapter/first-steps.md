# First Steps

Log into your web browser and go to the server's IP address (e.g.
<https://your-server/>). The default setup will redirect HTTP requests to
HTTPS.

The Elephant Shed portal provides information about
running PostgreSQL instances and their status. Moreover you get
access to all other installed components.

The server will ask you for your user credentials. Depending on the
deployment process the required user will differ. On a test
installation (e.g. using Vagrant) the initial user is **admin** with
password **admin**. See also: [Users](users.md). All bundled components except
for OmniDB have been configured to use PAM authentication.

OmniDB doesn't support PAM authentication yet. It has its own user
management system which is decoupled from all system users.
The default initial user is **admin** with **admin** as password.

![Figure: Elephant Shed portal](images/el-portal.png)

On a new installation you will find one cluster running the current PostgreSQL major version with the name `main`.

The configuration for clusters can be found in `/etc/postgresql/<major version>/<name>/`.

To use PostgreSQL from external application servers only a few steps are needed.

1. Open a shell connection to the server using SSH or shellinabox <https://your-server/shellinabox>.

2. Switch to user `postgres` and launch psql:
    * `sudo -u postgres psql`

3. Create a database and corresponding application user, options:
    * `psql: CREATE ROLE appuser1 WITH LOGIN PASSWORD 'testpass';`
    * `psql: CREATE DATABASE appdb1 OWNER appuser1;`

4. Allow external access for your application servers, your network or everyone. Configuration file: `/etc/postgresql/<major version>/<name>/pg_hba.conf`

5. (optional) Make desired configuration changes and tuning. `/etc/postgresql/<major version>/<name>/postgresql.conf`

6. Reload the configuration, options:
    * Portal: Click on the button `Service` next to the cluster and choose "Reload" from the dropdown menu
    * `psql`: `SELECT pg_reload_conf();`

7. (optional) Configure a superuser to be able to use OmniDB <https://your-server/omnidb> or other management tools
    * Create password for user postgres: `\password`
    * Create personalized superusers: `CREATE USER "sosna" SUPERUSER;`, `\password "sosna"`

