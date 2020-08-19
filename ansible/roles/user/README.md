Role Name
=========

Installs corosync and pacemaker

Requirements
------------

Role Variables
--------------
````

  root_ssh_key: NAME_OF_SSH_KEY (in credentials)
  users:
          - login: root
            name: root
            password: "{{ lookup('password', 'credentials/{{ inventory_hostname }}.sha512')}}"
            group: admin
            group_id: 2000
            non_unique: yes
            uid: 0
            ssh_key: "credentials/linux_server.pub"
            update_password: always


````
Dependencies
------------

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: user }

License
-------

BSD

Author Information
------------------

Heiko Borchers
- h.borchers [at] reply.de
