# Users

The web interface is password protected (HTTP basic authentication) and uses the system
users via PAM. When deployed via Ansible, the initial user is **admin** with
password **admin**. This user works for web access as well as for SSH and
PostgreSQL.

To create new users, use `adduser`, and add the user to the **elephant-shed** group.

```
adduser myon
adduser myon elephant-shed
```

On RedHat/CentOS, use `vigr` to add users to the **elephant-shed** group.
