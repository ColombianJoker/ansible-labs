Ansible labs from the book Red Hat Certified Engineer (RHCE) Ansible Automation Study Guide by Alex Soto Bueno & Andrew Block.

![Red Hat Certified Engineer (RHCE) Ansible Automation Study Guide](readme-1.jpg)

I used two versions, that's why the sequence of page numbers are not continuous.

# Files


## Página 90


### File listing

```
╭ 2026/06/30 15:30:16  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p90 
╰→ ls -l
.rw-r--r--@   37 e 30 Jun 15:29 -N 󱁻 ansible.cfg
.rw-r--r--@   63 e 30 Jun 15:27 -N 󰡯 inventory
.rw-r--r--@ 1.6k e 30 Jun 15:20 -N ⍱ Vagrantfile
╭ 2026/06/30 15:30:28  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p90 
╰→
```

Ansible local configuration (`ansible.cfg`)

```
[defaults]
host_key_checking = false
```

Ansible local inventory (`inventory`)

```
[node1]
192.168.25.147 ansible_user=alex ansible_ssh_pass=alex
```

`Vagrantfile`

```
Vagrant.configure("2") do |config|
  
  config.vm.define "staging" do |staging|
    # staging.vm.box = "fedora/37-cloud-base"
    staging.vm.box = "bento/almalinux-9"
    # staging.vm.box_version = "37.20221105.0"
    staging.vm.box_version = "202511.24.0"
    staging.ssh.password = "vagrant"
    staging.vm.network "public_network", use_dhcp_assigned_default_route: true
    staging.ssh.forward_agent = true
    staging.vm.provision "shell", inline: "ip -4 -o a"
  end
  
  config.vm.define "prod" do |prod|
    # staging.vm.box = "fedora/37-cloud-base"
    prod.vm.box = "bento/almalinux-9"
    # prod.vm.box_version = "37.20221105.0"
    prod.vm.box_version = "202511.24.0"
    prod.ssh.password = "vagrant"
    prod.vm.network "public_network", use_dhcp_assigned_default_route: true
    prod.ssh.forward_agent = true
    prod.vm.provision "shell", inline: "ip -4 -o a"
  end
  
  config.vm.define "node1" do |node1|
    node1.vm.box = "bento/almalinux-9"
    node1.vm.box_version = "202511.24.0"
    # This sets the SSH connection to expect the new user credentials
    node1.ssh.username = "vagrant"
    node1.ssh.password = "vagrant"
  
    node1.vm.network "public_network", use_dhcp_assigned_default_route: true
    node1.ssh.forward_agent = true
  
    # Provisioning: Create user, set password, and add to sudoers
    node1.vm.provision "shell", inline: <<-SHELL
      useradd -m alex
      echo "alex:alex" | chpasswd
      usermod -aG wheel alex
    SHELL
  end
  
  config.vm.provider "vmware_desktop" do |vmw|
    vmw.memory = "2048"
  end
end
```

Gather facts by playbook (`playbook-facts.yaml`)

```
- name: Gather Ansible facts
  hosts: all
  become: true
  
  tasks:
  - name: Print all available facts
    ansible.builtin.debug:
      var: ansible_facts
```

Output vars (`playbook-vars.yaml`)

```
- name: Echoing Vars
  hosts: all
  vars:
    msg_name: Alexandra
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Hello World {{msg_name}}"
      register: response
    - name: Print result
      ansible.builtin.debug:
        var: response
```

External vars (`external_vars.yaml`)

```
msg_name: Anna
```

Output vars #2 (`playbook-vars-2.yaml`)

```
- name: Echoing Vars
  hosts: all
  vars_files:
    - external_vars.yaml
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Hello World {{msg_name}}"
      register: response
    - name: Print result
      ansible.builtin.debug:
        var: response
```

## Página 99


### Inventory

```
[therock] ;
db ansible_host=192.168.0.17 ;
web ansible_hosts=192.168.0.18 ansible_user=alex ansible_ssh_pass=alex

[barcelona] '
db2 ansible_host=192.168.0.19 ansible_user=alex ansible_ssh_pass=alex
web2 ansible_host=192.168.0.20 ansible_user=alex ansible_ssh_pass=alex
```

### host_vars #1

`host_vars/db.yaml`
 
```
ansible_user: alex
ansible_ssh_pass: alex
msg_name: Anna
```

### group_vars #1

`group_vars/therock.yaml` 

```
ansible_user: alex
ansible_ssh_pass: alex
msg_name: Natale
```

### playbook-vars-3.yaml

`playbook-vars-3.yaml`

```
- name: Echoing Vars
  hosts: all
  vars_prompt:
    - name: msg_name
      prompt: What's the name?
      private: false
      default: Ada
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Hello World {{msg_name}}"
      register: response
    - name: Print result
      ansible.builtin.debug:
        var: response
```

### playbook-vars-4.yaml

`playbook-vars-4.yaml: Encrypt password`

```
- name: Echoing Vars
  hosts: all
  vars_prompt:
    - name: password
      prompt: Enter the password
      private: true
      encrypt: sha512_crypt
      confirm: true
      salt_size: 7
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Password '{{password}}'"
      register: response
    - name: Print result
      ansible.builtin.debug:
        var: response
```

### Encrypted playbook-env.yaml

`playbook-enc.yaml`

```
- name: Echoing vars
  hosts: all
  tasks:
    - name: Echo var
      ansible.builtin.command: >
         /bin/echo "The username is {{username}}
         and the password {{password}}"
      register: response
    - name: Print result
      ansible.builtin.debug:
        var: response
```

## Página 118

### Echo vars in loops

`loops-echo.yaml`
```
- name: Echoing in loops
  hosts: all
  gather_facts: false
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Hello World {{item}}"
      loop: [ "Ada", "Alexa" ]
      register: resp
    - name: Print result
      debug:
        var: resp
```

### Echo var in loops with pause

`loop-pause-echo.yaml`

```
- name: Echoing in loops
  hosts: all
  gather_facts: false
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Hello World {{item}}"
      loop: [ "Ada", "Alexa" ]
      loop_control:
        pause: 5
      register: resp
    - name: Print result
      debug:
        var: resp
```

### Echo var in indexed loops with pause

`loop-pause-echo-index.yaml`

```
- name: Echoing in loops
  hosts: all
  gather_facts: false
  tasks:
    - name: Echo var
      ansible.builtin.command: /bin/echo "Hello World {{item}} ({{idx}})"
      loop: [ "Ada", "Alexa" ]
      loop_control:
        pause: 5
        index_var: idx
      register: resp
    - name: Print result
      debug:
        var: resp
```

## Página 134
### Handlers

`playbook-handler.yaml`
```
- name: Update page
  hosts: all
  become: true
  tasks:
    - name: copy index.html
      ansible.builtin.copy:
        src: index.html
        dest: /usr/share/nginx/html/index.html
        mode: 0644
      notify:
        - Restart nginx
  handlers:
    - name: Restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

### External Variables

`play-ext-vars.yaml`
```
- name: Echoing Vars
  hosts: all
  gather_facts: false
  vars:
    una_variable: 'Un valor'
  vars_files:
    - external-vars.yaml
    
  tasks:
    - name: Echo var
      ansible.builtin.debug:
        msg: >
          una_variable: '{{una_variable}}', 
          segunda_variable: '{{segunda_variable}}',
          tercera_variable: '{{tercera_variable}}',
```

`external-vars.yaml`
```
segunda_variable: 'segundo valor'
tercera_variable: 'tercer valor'
```

## Página 123

### Loop extended control

`loop-ext-control.yaml`

```
- name: Loop extended control
  hosts: all
  gather_facts: false
  tasks:
    - name: Show all data
      ansible.builtin.debug:
        msg: >
          Indexes:
          - Index0 {{ ansible_loop.index0 }}
          - Index1 {{ ansible_loop.index }}
      loop: "{{ query('inventory_hostnames', 'all') }}"
      loop_control:
        extended: true
```

## Página 126

`builtin-dir-stat.yaml`
```
- name: Directory exists
  hosts: all
  gather_facts: false
  vars:
    systemddir: "/etc/systemd"

  tasks:
    - name: Do exists SystemD directory?
      ansible.builtin.stat:
        path: "{{systemddir}}"
      register: sysd
    - name: Show if SystemD directory exits
      ansible.builtin.debug:
        msg: "Directory {{systemddir}} exists!"
      when: sysd.stat.isdir is defined and sysd.stat.isdir
    - name: Shof if SystemD directory does not exists
      ansible.builtin.debug:
        msg: "Directory {{systemddir}} DOES NOT exists!"
      when: sysd.stat.isdir is not defined or not sysd.stat.isdir
```

## Página 147
### Block Rescue Always

`block-rescue-always.yaml`
```
- name: Block example
  hosts: all
  become: true
  tasks:
    - name: Attempt to install a package
      block:
        - name: install an invalid package
          ansible.builtin.dnf:
            name: kjdkdjkjfd
      rescue:
        - ansible.builtin.debug:
            msg: "Oh! there is an error"
      always:
        - ansible.builtin.debug:
            msg: "This always executes"
```

`block-rescue-always-with-name.yaml`
```
- name: Block example
  hosts: all
  become: true
  tasks:
    - name: Attempt to install a package
      block:
        - name: install an invalid package
          ansible.builtin.dnf:
            name: kjdkdjkjfd
      rescue:
        - name: Print custom error message
          ansible.builtin.debug:
            msg: "Oh! there is an error"
      always:
        - name: Print always-run message
          ansible.builtin.debug:
            msg: "This always executes"
```

### Inventory

`inventory.yaml` (created with `Vagrant2Inventory`)
```
all:
  children:
    vagrant_vms:
      hosts:
        staging:
          ansible_host: 127.0.0.1
          ansible_port: 2200
          ansible_user: vagrant
          ansible_ssh_private_key_file: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147/.vagrant/machines/staging/vmware_desktop/private_key
        prod:
          ansible_host: 127.0.0.1
          ansible_port: 2201
          ansible_user: vagrant
          ansible_ssh_private_key_file: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147/.vagrant/machines/prod/vmware_desktop/private_key
        node1:
          ansible_host: 127.0.0.1
          ansible_port: 2202
          ansible_user: vagrant
          ansible_ssh_private_key_file: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147/.vagrant/machines/node1/vmware_desktop/private_key
```

## Página 127
### Line/Block Infile Module

`line-block-infile.yaml`
```
- name: Line/Block Infile Module
  hosts: all
  gather_facts: false
  become: true
  tasks:
    - name: Insert line
      ansible.builtin.lineinfile:
        line: Hello Alexandra
        path: /home/alex/welcome.txt
        create: true
    - name: Remove line
      ansible.builtin.lineinfile:
        line: Hello World
        path: /home/alex/welcome.txt
        state: absent
```

## Página 131
### Jinja2 templates

`conf.properties.j2`
```
# File created at {{ansible_date_time.iso8601}}

hostname={{ ansible_hostname }}

{% if ansible_memtotal_mb > 500 %}
connection_pool=30
{% else %}
connection_pool=10
{% endif %}

db_username={{ username }}
db_password={{ password }}
```

`jinja2-playbook.yaml`
```
---
- name: configuration template
  hosts: all
  vars:
    username: Alex
    password: Alex

  tasks:
    - name: Copy conf files
      ansible.builtin.template:
        src: "conf.properties.j2"
        dest: "/tmp/conf.properties"
    - name: Display conf.properties contents
      ansible.builtin.command:
        cmd: cat conf.properties
        chdir: /tmp
      register: command_output
    - name: Print to console
      ansible.builtin.debug:
        msg: "{{command_output.stdout.split('\n')}}"
```

## Página 135

`lookup-hosts.yaml`
```
- name: Read hosts
  hosts: all
  gather_facts: false
  vars:
    hosts_value: "{{ lookup('file', '/etc/hosts') }}"
  tasks:
    - debug:
        msg: "hosts value is {{ hosts_value }}"
```

## Página 124

`library/hello.py`
```
#!/usr/bin/python3
#

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: hello
short_description: A demo module that prints a greeting message
version_added: "2.20"
description:
    - "A module that says hello."
options:
    name:
        description:
            - Name of the person to salute. If no value is provided the default
              value will be used.
        required: false
        type: str
        default: John Doe
author:
    - The Ops Team
"""

EXAMPLES = """
# Pass in a custom name
- name: Say hello to Linus Torvalds
  hello:
    name: "Linus Torvalds"
"""

RETURN = """
fact:
    description: Hello string
    type: str
    sample: Hello John Doe!
"""

from ansible.module_utils.basic import AnsibleModule

FACTS = "Hello {name}!"


def run_module():
    module_args = dict(
        name=dict(type="str", default="John Doe"),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    result = dict(
        changed=False,
        fact="",
    )

    txt = FACTS.format(name=module.params["name"])
    print(txt)
    result["fact"] = txt
    if module.check_mode:
        return result
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
```
playbook-example-use.yaml 
```
---
- name: CustomModule
  hosts: all
  gather_facts: true

  tasks:
    - name: Executes custom module
      hello:
        name: "Alexandra"
      register: demo_greeting

    - name: dump_output
      ansible.builtin.debug:
        msg: "{{ demo_greeting }}\n"
```

## Página 150
### Using role in a playbook

`install-jdk` (using `geerlingguy.java`)
```
---
- name: Install OpenJK 1.8.0
  hosts: all
  become: true
  roles:
    - role: geerlingguy.java
      when: "ansible_os_family == 'RedHat'"
      vars:
        java_packages:
          - java-1.8.0-openjdk
```

## Página 154

`printfile/tasks/main.yaml`
```
#SPDX-License-Identifier: MIT-0
---
# tasks file for printfile
- name: Display file contents
  ansible.builtin.command: "cat {{show_file}}"
  register: command_output
- name: Print to console
  ansible.builtin.debug:
    msg: "{{command_output.stdout}}"
```

`printfile/vars/main.yaml`
```
#SPDX-License-Identifier: MIT-0
---
# vars file for printfile
show_file: /etc/hosts
```

`roles/requirements.yaml`
```
---
- name: printfile
  src: file:///Users/e/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile.tar.gz
```

`play-use-role.yaml`
```
---
- name: use role
  become: true
  hosts: all

  tasks:
    - name: Print Hosts
      ansible.builtin.include_role:
        name: printfile
```

`printfile/tasks/main.yaml` (with handler added)
```
#SPDX-License-Identifier: MIT-0
---
# tasks file for printfile
- name: Display file contents
  ansible.builtin.command: "cat {{show_file}}"
  register: command_output
  notify: Print to console
- name: Print to console
  ansible.builtin.debug:
    msg: "{{command_output.stdout}}"
```

`printfile/handlers/main.yaml` (handler added)
```
#SPDX-License-Identifier: MIT-0
---
# handlers file for printfile
- name: Print to console
  ansible.builtin.debug:
    msg: "{{command_output.stdout}}"
```


## Página 90
### Facts

`ansible all -i inventory -m ansible.builtin.setup`
```
192.168.25.147 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.209.177",
            "192.168.25.147"
        ],
        "ansible_all_ipv6_addresses": [
            "fe80::20c:29ff:fed7:8619",
            "fe80::20c:29ff:fed7:8623"
        ],
        "ansible_apparmor": {
            "status": "disabled"
        },
        "ansible_architecture": "aarch64",
        "ansible_bios_date": "07/21/2025",
        "ansible_bios_vendor": "VMware, Inc.",
        "ansible_bios_version": "VMW201.00V.24866131.BA64.2507211911",
        "ansible_board_asset_tag": "NA",
        "ansible_board_name": "VBSA",
        "ansible_board_serial": "NA",
        "ansible_board_vendor": "VMware, Inc.",
        "ansible_board_version": "1",
        "ansible_chassis_asset_tag": "NA",
        "ansible_chassis_serial": "NA",
        "ansible_chassis_vendor": "VMware, Inc.",
        "ansible_chassis_version": "VMware20,1",
        "ansible_cmdline": {
            "BOOT_IMAGE": "(hd0,gpt3)/boot/vmlinuz-5.14.0-611.5.1.el9_7.aarch64",
            "console": "ttyS0,115200n8",
            "no_timer_check": true,
            "ro": true,
            "root": "UUID=8cac1a76-12b8-48cb-9106-a56e21d96853"
        },
        "ansible_date_time": {
            "date": "2026-06-30",
            "day": "30",
            "epoch": "1782851588",
            "epoch_int": "1782851588",
            "hour": "20",
            "iso8601": "2026-06-30T20:33:08Z",
            "iso8601_basic": "20260630T203308271045",
            "iso8601_basic_short": "20260630T203308",
            "iso8601_micro": "2026-06-30T20:33:08.271045Z",
            "minute": "33",
            "month": "06",
            "second": "08",
            "time": "20:33:08",
            "tz": "UTC",
            "tz_dst": "UTC",
            "tz_offset": "+0000",
            "weekday": "Tuesday",
            "weekday_number": "2",
            "weeknumber": "26",
            "year": "2026"
        },
        "ansible_default_ipv4": {
            "address": "192.168.209.177",
            "alias": "enp2s0",
            "broadcast": "192.168.209.255",
            "gateway": "192.168.209.2",
            "interface": "enp2s0",
            "macaddress": "00:0c:29:d7:86:19",
            "mtu": 1500,
            "netmask": "255.255.255.0",
            "network": "192.168.209.0",
            "prefix": "24",
            "type": "ether"
        },
        "ansible_default_ipv6": {},
        "ansible_device_links": {
            "ids": {
                "nvme0n1": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77"
                ],
                "nvme0n1p1": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part1",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part1",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77-part1"
                ],
                "nvme0n1p2": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part2",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part2",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77-part2"
                ],
                "nvme0n1p3": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part3",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part3",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77-part3"
                ],
                "sr0": [
                    "ata-VMware_Virtual_SATA_CDRW_Drive_00000000000000000001"
                ]
            },
            "labels": {},
            "masters": {},
            "uuids": {
                "nvme0n1p1": [
                    "9175-A449"
                ],
                "nvme0n1p2": [
                    "6f1523db-76e5-4906-bf1f-135e1c5d7951"
                ],
                "nvme0n1p3": [
                    "8cac1a76-12b8-48cb-9106-a56e21d96853"
                ]
            }
        },
        "ansible_devices": {
            "nvme0n1": {
                "holders": [],
                "host": "Non-Volatile memory controller: VMware NVMe SSD Controller",
                "links": {
                    "ids": [
                        "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000",
                        "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1",
                        "nvme-eui.408173c8ad2775b9000c296a110fad77"
                    ],
                    "labels": [],
                    "masters": [],
                    "uuids": []
                },
                "model": "VMware Virtual NVMe Disk",
                "partitions": {
                    "nvme0n1p1": {
                        "holders": [],
                        "links": {
                            "ids": [
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part1",
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part1",
                                "nvme-eui.408173c8ad2775b9000c296a110fad77-part1"
                            ],
                            "labels": [],
                            "masters": [],
                            "uuids": [
                                "9175-A449"
                            ]
                        },
                        "sectors": 1228800,
                        "sectorsize": 512,
                        "size": "600.00 MB",
                        "start": "2048",
                        "uuid": "9175-A449"
                    },
                    "nvme0n1p2": {
                        "holders": [],
                        "links": {
                            "ids": [
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part2",
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part2",
                                "nvme-eui.408173c8ad2775b9000c296a110fad77-part2"
                            ],
                            "labels": [],
                            "masters": [],
                            "uuids": [
                                "6f1523db-76e5-4906-bf1f-135e1c5d7951"
                            ]
                        },
                        "sectors": 8255488,
                        "sectorsize": 512,
                        "size": "3.94 GB",
                        "start": "1230848",
                        "uuid": "6f1523db-76e5-4906-bf1f-135e1c5d7951"
                    },
                    "nvme0n1p3": {
                        "holders": [],
                        "links": {
                            "ids": [
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part3",
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part3",
                                "nvme-eui.408173c8ad2775b9000c296a110fad77-part3"
                            ],
                            "labels": [],
                            "masters": [],
                            "uuids": [
                                "8cac1a76-12b8-48cb-9106-a56e21d96853"
                            ]
                        },
                        "sectors": 124729344,
                        "sectorsize": 512,
                        "size": "59.48 GB",
                        "start": "9486336",
                        "uuid": "8cac1a76-12b8-48cb-9106-a56e21d96853"
                    }
                },
                "removable": "0",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "none",
                "sectors": 134217728,
                "sectorsize": "512",
                "size": "64.00 GB",
                "support_discard": "0",
                "vendor": null,
                "virtual": 1
            },
            "sr0": {
                "holders": [],
                "host": "SATA controller: VMware SATA AHCI controller",
                "links": {
                    "ids": [
                        "ata-VMware_Virtual_SATA_CDRW_Drive_00000000000000000001"
                    ],
                    "labels": [],
                    "masters": [],
                    "uuids": []
                },
                "model": "VMware SATA CD00",
                "partitions": {},
                "removable": "1",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "mq-deadline",
                "sectors": 2097151,
                "sectorsize": "512",
                "size": "1024.00 MB",
                "support_discard": "0",
                "vendor": "NECVMWar",
                "virtual": 1
            }
        },
        "ansible_distribution": "AlmaLinux",
        "ansible_distribution_file_parsed": true,
        "ansible_distribution_file_path": "/etc/redhat-release",
        "ansible_distribution_file_variety": "RedHat",
        "ansible_distribution_major_version": "9",
        "ansible_distribution_release": "Moss Jungle Cat",
        "ansible_distribution_version": "9.7",
        "ansible_dns": {
            "nameservers": [
                "192.168.209.2",
                "192.168.25.1"
            ],
            "search": [
                "localdomain",
                "lan"
            ]
        },
        "ansible_domain": "localdomain",
        "ansible_effective_group_id": 1001,
        "ansible_effective_user_id": 1001,
        "ansible_enp26s0": {
            "active": true,
            "device": "enp26s0",
            "features": {
                "esp_hw_offload": "off [fixed]",
                "esp_tx_csum_hw_offload": "off [fixed]",
                "generic_receive_offload": "on",
                "generic_segmentation_offload": "on",
                "highdma": "on [fixed]",
                "hsr_dup_offload": "off [fixed]",
                "hsr_fwd_offload": "off [fixed]",
                "hsr_tag_ins_offload": "off [fixed]",
                "hsr_tag_rm_offload": "off [fixed]",
                "hw_tc_offload": "off [fixed]",
                "l2_fwd_offload": "off [fixed]",
                "large_receive_offload": "off [fixed]",
                "loopback": "off [fixed]",
                "macsec_hw_offload": "off [fixed]",
                "ntuple_filters": "off [fixed]",
                "receive_hashing": "on",
                "rx_all": "off",
                "rx_checksumming": "on",
                "rx_fcs": "off",
                "rx_gro_hw": "off [fixed]",
                "rx_gro_list": "off",
                "rx_udp_gro_forwarding": "off",
                "rx_udp_tunnel_port_offload": "off [fixed]",
                "rx_vlan_filter": "on [fixed]",
                "rx_vlan_offload": "on",
                "rx_vlan_stag_filter": "off [fixed]",
                "rx_vlan_stag_hw_parse": "off [fixed]",
                "scatter_gather": "on",
                "tcp_segmentation_offload": "on",
                "tls_hw_record": "off [fixed]",
                "tls_hw_rx_offload": "off [fixed]",
                "tls_hw_tx_offload": "off [fixed]",
                "tx_checksum_fcoe_crc": "off [fixed]",
                "tx_checksum_ip_generic": "on",
                "tx_checksum_ipv4": "off [fixed]",
                "tx_checksum_ipv6": "off [fixed]",
                "tx_checksum_sctp": "off [fixed]",
                "tx_checksumming": "on",
                "tx_esp_segmentation": "off [fixed]",
                "tx_fcoe_segmentation": "off [fixed]",
                "tx_gre_csum_segmentation": "off [fixed]",
                "tx_gre_segmentation": "off [fixed]",
                "tx_gso_list": "off [fixed]",
                "tx_gso_partial": "off [fixed]",
                "tx_gso_robust": "off [fixed]",
                "tx_ipxip4_segmentation": "off [fixed]",
                "tx_ipxip6_segmentation": "off [fixed]",
                "tx_nocache_copy": "off",
                "tx_scatter_gather": "on",
                "tx_scatter_gather_fraglist": "off [fixed]",
                "tx_sctp_segmentation": "off [fixed]",
                "tx_tcp6_segmentation": "on",
                "tx_tcp_ecn_segmentation": "off [fixed]",
                "tx_tcp_mangleid_segmentation": "off",
                "tx_tcp_segmentation": "on",
                "tx_tunnel_remcsum_segmentation": "off [fixed]",
                "tx_udp_segmentation": "off [fixed]",
                "tx_udp_tnl_csum_segmentation": "off [fixed]",
                "tx_udp_tnl_segmentation": "off [fixed]",
                "tx_vlan_offload": "on",
                "tx_vlan_stag_hw_insert": "off [fixed]",
                "vlan_challenged": "off [fixed]"
            },
            "hw_timestamp_filters": [],
            "ipv4": {
                "address": "192.168.25.147",
                "broadcast": "192.168.25.255",
                "netmask": "255.255.255.0",
                "network": "192.168.25.0",
                "prefix": "24"
            },
            "ipv6": [
                {
                    "address": "fe80::20c:29ff:fed7:8623",
                    "prefix": "64",
                    "scope": "link"
                }
            ],
            "macaddress": "00:0c:29:d7:86:23",
            "module": "e1000e",
            "mtu": 1500,
            "pciid": "0000:1a:00.0",
            "promisc": false,
            "speed": 1000,
            "timestamping": [],
            "type": "ether"
        },
        "ansible_enp2s0": {
            "active": true,
            "device": "enp2s0",
            "features": {
                "esp_hw_offload": "off [fixed]",
                "esp_tx_csum_hw_offload": "off [fixed]",
                "generic_receive_offload": "on",
                "generic_segmentation_offload": "on",
                "highdma": "on [fixed]",
                "hsr_dup_offload": "off [fixed]",
                "hsr_fwd_offload": "off [fixed]",
                "hsr_tag_ins_offload": "off [fixed]",
                "hsr_tag_rm_offload": "off [fixed]",
                "hw_tc_offload": "off [fixed]",
                "l2_fwd_offload": "off [fixed]",
                "large_receive_offload": "off [fixed]",
                "loopback": "off [fixed]",
                "macsec_hw_offload": "off [fixed]",
                "ntuple_filters": "off [fixed]",
                "receive_hashing": "on",
                "rx_all": "off",
                "rx_checksumming": "on",
                "rx_fcs": "off",
                "rx_gro_hw": "off [fixed]",
                "rx_gro_list": "off",
                "rx_udp_gro_forwarding": "off",
                "rx_udp_tunnel_port_offload": "off [fixed]",
                "rx_vlan_filter": "on [fixed]",
                "rx_vlan_offload": "on",
                "rx_vlan_stag_filter": "off [fixed]",
                "rx_vlan_stag_hw_parse": "off [fixed]",
                "scatter_gather": "on",
                "tcp_segmentation_offload": "on",
                "tls_hw_record": "off [fixed]",
                "tls_hw_rx_offload": "off [fixed]",
                "tls_hw_tx_offload": "off [fixed]",
                "tx_checksum_fcoe_crc": "off [fixed]",
                "tx_checksum_ip_generic": "on",
                "tx_checksum_ipv4": "off [fixed]",
                "tx_checksum_ipv6": "off [fixed]",
                "tx_checksum_sctp": "off [fixed]",
                "tx_checksumming": "on",
                "tx_esp_segmentation": "off [fixed]",
                "tx_fcoe_segmentation": "off [fixed]",
                "tx_gre_csum_segmentation": "off [fixed]",
                "tx_gre_segmentation": "off [fixed]",
                "tx_gso_list": "off [fixed]",
                "tx_gso_partial": "off [fixed]",
                "tx_gso_robust": "off [fixed]",
                "tx_ipxip4_segmentation": "off [fixed]",
                "tx_ipxip6_segmentation": "off [fixed]",
                "tx_nocache_copy": "off",
                "tx_scatter_gather": "on",
                "tx_scatter_gather_fraglist": "off [fixed]",
                "tx_sctp_segmentation": "off [fixed]",
                "tx_tcp6_segmentation": "on",
                "tx_tcp_ecn_segmentation": "off [fixed]",
                "tx_tcp_mangleid_segmentation": "off",
                "tx_tcp_segmentation": "on",
                "tx_tunnel_remcsum_segmentation": "off [fixed]",
                "tx_udp_segmentation": "off [fixed]",
                "tx_udp_tnl_csum_segmentation": "off [fixed]",
                "tx_udp_tnl_segmentation": "off [fixed]",
                "tx_vlan_offload": "on",
                "tx_vlan_stag_hw_insert": "off [fixed]",
                "vlan_challenged": "off [fixed]"
            },
            "hw_timestamp_filters": [],
            "ipv4": {
                "address": "192.168.209.177",
                "broadcast": "192.168.209.255",
                "netmask": "255.255.255.0",
                "network": "192.168.209.0",
                "prefix": "24"
            },
            "ipv6": [
                {
                    "address": "fe80::20c:29ff:fed7:8619",
                    "prefix": "64",
                    "scope": "link"
                }
            ],
            "macaddress": "00:0c:29:d7:86:19",
            "module": "e1000e",
            "mtu": 1500,
            "pciid": "0000:02:00.0",
            "promisc": false,
            "speed": 1000,
            "timestamping": [],
            "type": "ether"
        },
        "ansible_env": {
            "BASH_FUNC_which%%": "() {  ( alias;\n eval ${which_declare} ) | /usr/bin/which --tty-only --read-alias --read-functions --show-tilde --show-dot $@\n}",
            "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1001/bus",
            "DEBUGINFOD_IMA_CERT_PATH": "/etc/keys/ima:",
            "HOME": "/home/alex",
            "LANG": "en_US.UTF-8",
            "LESSOPEN": "||/usr/bin/lesspipe.sh %s",
            "LOGNAME": "alex",
            "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.m4a=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.oga=01;36:*.opus=01;36:*.spx=01;36:*.xspf=01;36:",
            "MOTD_SHOWN": "pam",
            "PATH": "/home/alex/.local/bin:/home/alex/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin",
            "PWD": "/home/alex",
            "SELINUX_LEVEL_REQUESTED": "",
            "SELINUX_ROLE_REQUESTED": "",
            "SELINUX_USE_CURRENT_RANGE": "",
            "SHELL": "/bin/bash",
            "SHLVL": "1",
            "SSH_CLIENT": "192.168.25.8 59607 22",
            "SSH_CONNECTION": "192.168.25.8 59607 192.168.25.147 22",
            "SSH_TTY": "/dev/pts/0",
            "TERM": "xterm-256color",
            "USER": "alex",
            "XDG_RUNTIME_DIR": "/run/user/1001",
            "XDG_SESSION_CLASS": "user",
            "XDG_SESSION_ID": "7",
            "XDG_SESSION_TYPE": "tty",
            "_": "/usr/bin/python3.9",
            "which_declare": "declare -f"
        },
        "ansible_fibre_channel_wwn": [],
        "ansible_fips": false,
        "ansible_form_factor": "Other",
        "ansible_fqdn": "localhost.localdomain",
        "ansible_hostname": "localhost",
        "ansible_hostnqn": "nqn.2014-08.org.nvmexpress:uuid:20aa4d56-a6e3-e861-befd-ddcb7a5bce85",
        "ansible_interfaces": [
            "enp26s0",
            "lo",
            "enp2s0"
        ],
        "ansible_is_chroot": false,
        "ansible_iscsi_iqn": "",
        "ansible_kernel": "5.14.0-611.5.1.el9_7.aarch64",
        "ansible_kernel_version": "#1 SMP PREEMPT_DYNAMIC Tue Nov 11 17:55:12 EST 2025",
        "ansible_lo": {
            "active": true,
            "device": "lo",
            "features": {
                "esp_hw_offload": "off [fixed]",
                "esp_tx_csum_hw_offload": "off [fixed]",
                "generic_receive_offload": "on",
                "generic_segmentation_offload": "on",
                "highdma": "on [fixed]",
                "hsr_dup_offload": "off [fixed]",
                "hsr_fwd_offload": "off [fixed]",
                "hsr_tag_ins_offload": "off [fixed]",
                "hsr_tag_rm_offload": "off [fixed]",
                "hw_tc_offload": "off [fixed]",
                "l2_fwd_offload": "off [fixed]",
                "large_receive_offload": "off [fixed]",
                "loopback": "on [fixed]",
                "macsec_hw_offload": "off [fixed]",
                "ntuple_filters": "off [fixed]",
                "receive_hashing": "off [fixed]",
                "rx_all": "off [fixed]",
                "rx_checksumming": "on [fixed]",
                "rx_fcs": "off [fixed]",
                "rx_gro_hw": "off [fixed]",
                "rx_gro_list": "off",
                "rx_udp_gro_forwarding": "off",
                "rx_udp_tunnel_port_offload": "off [fixed]",
                "rx_vlan_filter": "off [fixed]",
                "rx_vlan_offload": "off [fixed]",
                "rx_vlan_stag_filter": "off [fixed]",
                "rx_vlan_stag_hw_parse": "off [fixed]",
                "scatter_gather": "on",
                "tcp_segmentation_offload": "on",
                "tls_hw_record": "off [fixed]",
                "tls_hw_rx_offload": "off [fixed]",
                "tls_hw_tx_offload": "off [fixed]",
                "tx_checksum_fcoe_crc": "off [fixed]",
                "tx_checksum_ip_generic": "on [fixed]",
                "tx_checksum_ipv4": "off [fixed]",
                "tx_checksum_ipv6": "off [fixed]",
                "tx_checksum_sctp": "on [fixed]",
                "tx_checksumming": "on",
                "tx_esp_segmentation": "off [fixed]",
                "tx_fcoe_segmentation": "off [fixed]",
                "tx_gre_csum_segmentation": "off [fixed]",
                "tx_gre_segmentation": "off [fixed]",
                "tx_gso_list": "on",
                "tx_gso_partial": "off [fixed]",
                "tx_gso_robust": "off [fixed]",
                "tx_ipxip4_segmentation": "off [fixed]",
                "tx_ipxip6_segmentation": "off [fixed]",
                "tx_nocache_copy": "off [fixed]",
                "tx_scatter_gather": "on [fixed]",
                "tx_scatter_gather_fraglist": "on [fixed]",
                "tx_sctp_segmentation": "on",
                "tx_tcp6_segmentation": "on",
                "tx_tcp_ecn_segmentation": "on",
                "tx_tcp_mangleid_segmentation": "on",
                "tx_tcp_segmentation": "on",
                "tx_tunnel_remcsum_segmentation": "off [fixed]",
                "tx_udp_segmentation": "on",
                "tx_udp_tnl_csum_segmentation": "off [fixed]",
                "tx_udp_tnl_segmentation": "off [fixed]",
                "tx_vlan_offload": "off [fixed]",
                "tx_vlan_stag_hw_insert": "off [fixed]",
                "vlan_challenged": "on [fixed]"
            },
            "hw_timestamp_filters": [],
            "ipv4": {
                "address": "127.0.0.1",
                "broadcast": "",
                "netmask": "255.0.0.0",
                "network": "127.0.0.0",
                "prefix": "8"
            },
            "ipv6": [
                {
                    "address": "::1",
                    "prefix": "128",
                    "scope": "host"
                }
            ],
            "mtu": 65536,
            "promisc": false,
            "timestamping": [],
            "type": "loopback"
        },
        "ansible_loadavg": {
            "15m": 0.0,
            "1m": 0.0,
            "5m": 0.01
        },
        "ansible_local": {},
        "ansible_locally_reachable_ips": {
            "ipv4": [
                "127.0.0.0/8",
                "127.0.0.1",
                "192.168.25.147",
                "192.168.209.177"
            ],
            "ipv6": [
                "::1",
                "fe80::20c:29ff:fed7:8619",
                "fe80::20c:29ff:fed7:8623"
            ]
        },
        "ansible_lsb": {},
        "ansible_lvm": "N/A",
        "ansible_machine": "aarch64",
        "ansible_machine_id": "c273435379134e3f8b29c556d35b5308",
        "ansible_memfree_mb": 1517,
        "ansible_memory_mb": {
            "nocache": {
                "free": 1677,
                "used": 278
            },
            "real": {
                "free": 1517,
                "total": 1955,
                "used": 438
            },
            "swap": {
                "cached": 0,
                "free": 4030,
                "total": 4030,
                "used": 0
            }
        },
        "ansible_memtotal_mb": 1955,
        "ansible_mounts": [
            {
                "block_available": 15110852,
                "block_size": 4096,
                "block_total": 15574784,
                "block_used": 463932,
                "device": "/dev/nvme0n1p3",
                "dump": 0,
                "fstype": "xfs",
                "inode_available": 31146028,
                "inode_total": 31182336,
                "inode_used": 36308,
                "mount": "/",
                "options": "rw,seclabel,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota",
                "passno": 0,
                "size_available": 61894049792,
                "size_total": 63794315264,
                "uuid": "8cac1a76-12b8-48cb-9106-a56e21d96853"
            },
            {
                "block_available": 151415,
                "block_size": 4096,
                "block_total": 153296,
                "block_used": 1881,
                "device": "/dev/nvme0n1p1",
                "dump": 0,
                "fstype": "vfat",
                "inode_available": 0,
                "inode_total": 0,
                "inode_used": 0,
                "mount": "/boot/efi",
                "options": "rw,relatime,fmask=0077,dmask=0077,codepage=437,iocharset=ascii,shortname=winnt,errors=remount-ro",
                "passno": 0,
                "size_available": 620195840,
                "size_total": 627900416,
                "uuid": "9175-A449"
            }
        ],
        "ansible_nodename": "localhost.localdomain",
        "ansible_os_family": "RedHat",
        "ansible_pkg_mgr": "dnf",
        "ansible_proc_cmdline": {
            "BOOT_IMAGE": "(hd0,gpt3)/boot/vmlinuz-5.14.0-611.5.1.el9_7.aarch64",
            "console": [
                "tty0",
                "ttyS0,115200n8"
            ],
            "no_timer_check": true,
            "ro": true,
            "root": "UUID=8cac1a76-12b8-48cb-9106-a56e21d96853"
        },
        "ansible_processor": [
            "0",
            "1"
        ],
        "ansible_processor_cores": 1,
        "ansible_processor_count": 2,
        "ansible_processor_nproc": 2,
        "ansible_processor_threads_per_core": 1,
        "ansible_processor_vcpus": 2,
        "ansible_product_name": "VMware20,1",
        "ansible_product_serial": "NA",
        "ansible_product_uuid": "NA",
        "ansible_product_version": "1",
        "ansible_python": {
            "executable": "/usr/bin/python3.9",
            "has_sslcontext": true,
            "type": "cpython",
            "version": {
                "major": 3,
                "micro": 23,
                "minor": 9,
                "releaselevel": "final",
                "serial": 0
            },
            "version_info": [
                3,
                9,
                23,
                "final",
                0
            ]
        },
        "ansible_python_version": "3.9.23",
        "ansible_real_group_id": 1001,
        "ansible_real_user_id": 1001,
        "ansible_selinux": {
            "config_mode": "enforcing",
            "mode": "enforcing",
            "policyvers": 33,
            "status": "enabled",
            "type": "targeted"
        },
        "ansible_selinux_python_present": true,
        "ansible_service_mgr": "systemd",
        "ansible_ssh_host_key_ecdsa_public": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGGp6kHseSenOvU5sCCBFZzJvZtf6/Hhhrd5qQzJbSu5hS3s+6a8eTx3iDp5NNNR/QYVY2gCo84nAVPqxJFzJ2M=",
        "ansible_ssh_host_key_ecdsa_public_keytype": "ecdsa-sha2-nistp256",
        "ansible_ssh_host_key_ed25519_public": "AAAAC3NzaC1lZDI1NTE5AAAAIEAPnL4iz8MyzQufR4HqTF/DrqSqsLn2BkZJ+N0xXIpo",
        "ansible_ssh_host_key_ed25519_public_keytype": "ssh-ed25519",
        "ansible_ssh_host_key_rsa_public": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDRYbGsaJBeiJEF66hCk2UGzWcLU8AvXPFT8SucHGdwwaMI79wB4iBzPfbdQhHaVilC7v+Ke09N1tvngKIYkOeMmtaAVF0Wdn9gSXQQzgvpLAn6vuyKWuF1jXvnl2aLiRVEgTL9xXWTs0w6cexEN5ST1m+PUEc7VE8ecWUmvM5yCck+olxDE32PDzft2v6XMUnnAQOvfpmi8dUXr8hcWxQ6TeDD5vuXswFis/JomMrBK4chRvlirf+GqvHm5kobzZqtOUA1hOWR1hP4iAcw44xxAfrbRegfY3Y1cWPvikPWquI3fM88KdlAi8xVtKkPq+1QJ4lyNQBbubZb/AmLPgTSepZ1/TaStNbgQ9sS2DhbUjalyXC/u2f/GLM0rXqNwYw3OJkVRt4/99Pe4boWO3b11toF2xs4nNKFrwMGnI1LSyAj+qCx+af3B4UO7zyEy2WjZxRURKwA03LiF8L8IPl7lMQ5R0sPx08xZADUlcAF6SUqBEw4BIQbveJuviRk8ss=",
        "ansible_ssh_host_key_rsa_public_keytype": "ssh-rsa",
        "ansible_swapfree_mb": 4030,
        "ansible_swaptotal_mb": 4030,
        "ansible_system": "Linux",
        "ansible_system_capabilities": [
            ""
        ],
        "ansible_system_capabilities_enforced": "True",
        "ansible_system_vendor": "VMware, Inc.",
        "ansible_systemd": {
            "features": "+PAM +AUDIT +SELINUX -APPARMOR +IMA +SMACK +SECCOMP +GCRYPT +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN -IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 -PWQUALITY +P11KIT -QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD -BPF_FRAMEWORK +XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified",
            "version": 252
        },
        "ansible_uptime_seconds": 475,
        "ansible_user_dir": "/home/alex",
        "ansible_user_gecos": "",
        "ansible_user_gid": 1001,
        "ansible_user_id": "alex",
        "ansible_user_shell": "/bin/bash",
        "ansible_user_uid": 1001,
        "ansible_userspace_bits": "64",
        "ansible_virtualization_role": "guest",
        "ansible_virtualization_tech_guest": [
            "VMware"
        ],
        "ansible_virtualization_tech_host": [],
        "ansible_virtualization_type": "VMware",
        "discovered_interpreter_python": "/usr/bin/python3.9",
        "gather_subset": [
            "all"
        ],
        "module_setup": true
    },
    "changed": false
}
```

### Playbook Facts

`ansible-playbook -i inventory -K playbook-facts.yaml`
```
BECOME password: 

PLAY [Gather Ansible facts] ******************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.147' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.147]

TASK [Print all available facts] *************************************************************
ok: [192.168.25.147] => {
    "ansible_facts": {
        "all_ipv4_addresses": [
            "192.168.209.177",
            "192.168.25.147"
        ],
        "all_ipv6_addresses": [
            "fe80::20c:29ff:fed7:8619",
            "fe80::20c:29ff:fed7:8623"
        ],
        "ansible_local": {},
        "apparmor": {
            "status": "disabled"
        },
        "architecture": "aarch64",
        "bios_date": "07/21/2025",
        "bios_vendor": "VMware, Inc.",
        "bios_version": "VMW201.00V.24866131.BA64.2507211911",
        "board_asset_tag": "NA",
        "board_name": "VBSA",
        "board_serial": "ACAA6BE889B34D56",
        "board_vendor": "VMware, Inc.",
        "board_version": "1",
        "chassis_asset_tag": "NA",
        "chassis_serial": "ACAA6BE889B34D56",
        "chassis_vendor": "VMware, Inc.",
        "chassis_version": "VMware20,1",
        "cmdline": {
            "BOOT_IMAGE": "(hd0,gpt3)/boot/vmlinuz-5.14.0-611.5.1.el9_7.aarch64",
            "console": "ttyS0,115200n8",
            "no_timer_check": true,
            "ro": true,
            "root": "UUID=8cac1a76-12b8-48cb-9106-a56e21d96853"
        },
        "date_time": {
            "date": "2026-06-30",
            "day": "30",
            "epoch": "1782852114",
            "epoch_int": "1782852114",
            "hour": "20",
            "iso8601": "2026-06-30T20:41:54Z",
            "iso8601_basic": "20260630T204154885765",
            "iso8601_basic_short": "20260630T204154",
            "iso8601_micro": "2026-06-30T20:41:54.885765Z",
            "minute": "41",
            "month": "06",
            "second": "54",
            "time": "20:41:54",
            "tz": "UTC",
            "tz_dst": "UTC",
            "tz_offset": "+0000",
            "weekday": "Tuesday",
            "weekday_number": "2",
            "weeknumber": "26",
            "year": "2026"
        },
        "default_ipv4": {
            "address": "192.168.209.177",
            "alias": "enp2s0",
            "broadcast": "192.168.209.255",
            "gateway": "192.168.209.2",
            "interface": "enp2s0",
            "macaddress": "00:0c:29:d7:86:19",
            "mtu": 1500,
            "netmask": "255.255.255.0",
            "network": "192.168.209.0",
            "prefix": "24",
            "type": "ether"
        },
        "default_ipv6": {},
        "device_links": {
            "ids": {
                "nvme0n1": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77"
                ],
                "nvme0n1p1": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part1",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part1",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77-part1"
                ],
                "nvme0n1p2": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part2",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part2",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77-part2"
                ],
                "nvme0n1p3": [
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part3",
                    "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part3",
                    "nvme-eui.408173c8ad2775b9000c296a110fad77-part3"
                ],
                "sr0": [
                    "ata-VMware_Virtual_SATA_CDRW_Drive_00000000000000000001"
                ]
            },
            "labels": {},
            "masters": {},
            "uuids": {
                "nvme0n1p1": [
                    "9175-A449"
                ],
                "nvme0n1p2": [
                    "6f1523db-76e5-4906-bf1f-135e1c5d7951"
                ],
                "nvme0n1p3": [
                    "8cac1a76-12b8-48cb-9106-a56e21d96853"
                ]
            }
        },
        "devices": {
            "nvme0n1": {
                "holders": [],
                "host": "Non-Volatile memory controller: VMware NVMe SSD Controller",
                "links": {
                    "ids": [
                        "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000",
                        "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1",
                        "nvme-eui.408173c8ad2775b9000c296a110fad77"
                    ],
                    "labels": [],
                    "masters": [],
                    "uuids": []
                },
                "model": "VMware Virtual NVMe Disk",
                "partitions": {
                    "nvme0n1p1": {
                        "holders": [],
                        "links": {
                            "ids": [
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part1",
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part1",
                                "nvme-eui.408173c8ad2775b9000c296a110fad77-part1"
                            ],
                            "labels": [],
                            "masters": [],
                            "uuids": [
                                "9175-A449"
                            ]
                        },
                        "sectors": 1228800,
                        "sectorsize": 512,
                        "size": "600.00 MB",
                        "start": "2048",
                        "uuid": "9175-A449"
                    },
                    "nvme0n1p2": {
                        "holders": [],
                        "links": {
                            "ids": [
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part2",
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part2",
                                "nvme-eui.408173c8ad2775b9000c296a110fad77-part2"
                            ],
                            "labels": [],
                            "masters": [],
                            "uuids": [
                                "6f1523db-76e5-4906-bf1f-135e1c5d7951"
                            ]
                        },
                        "sectors": 8255488,
                        "sectorsize": 512,
                        "size": "3.94 GB",
                        "start": "1230848",
                        "uuid": "6f1523db-76e5-4906-bf1f-135e1c5d7951"
                    },
                    "nvme0n1p3": {
                        "holders": [],
                        "links": {
                            "ids": [
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000-part3",
                                "nvme-VMware_Virtual_NVMe_Disk_VMware_NVME_0000_1-part3",
                                "nvme-eui.408173c8ad2775b9000c296a110fad77-part3"
                            ],
                            "labels": [],
                            "masters": [],
                            "uuids": [
                                "8cac1a76-12b8-48cb-9106-a56e21d96853"
                            ]
                        },
                        "sectors": 124729344,
                        "sectorsize": 512,
                        "size": "59.48 GB",
                        "start": "9486336",
                        "uuid": "8cac1a76-12b8-48cb-9106-a56e21d96853"
                    }
                },
                "removable": "0",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "none",
                "sectors": 134217728,
                "sectorsize": "512",
                "serial": "VMware",
                "size": "64.00 GB",
                "support_discard": "0",
                "vendor": null,
                "virtual": 1
            },
            "sr0": {
                "holders": [],
                "host": "SATA controller: VMware SATA AHCI controller",
                "links": {
                    "ids": [
                        "ata-VMware_Virtual_SATA_CDRW_Drive_00000000000000000001"
                    ],
                    "labels": [],
                    "masters": [],
                    "uuids": []
                },
                "model": "VMware SATA CD00",
                "partitions": {},
                "removable": "1",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "mq-deadline",
                "sectors": 2097151,
                "sectorsize": "512",
                "size": "1024.00 MB",
                "support_discard": "0",
                "vendor": "NECVMWar",
                "virtual": 1
            }
        },
        "discovered_interpreter_python": "/usr/bin/python3.9",
        "distribution": "AlmaLinux",
        "distribution_file_parsed": true,
        "distribution_file_path": "/etc/redhat-release",
        "distribution_file_variety": "RedHat",
        "distribution_major_version": "9",
        "distribution_release": "Moss Jungle Cat",
        "distribution_version": "9.7",
        "dns": {
            "nameservers": [
                "192.168.209.2",
                "192.168.25.1"
            ],
            "search": [
                "localdomain",
                "lan"
            ]
        },
        "domain": "localdomain",
        "effective_group_id": 0,
        "effective_user_id": 0,
        "enp26s0": {
            "active": true,
            "device": "enp26s0",
            "features": {
                "esp_hw_offload": "off [fixed]",
                "esp_tx_csum_hw_offload": "off [fixed]",
                "generic_receive_offload": "on",
                "generic_segmentation_offload": "on",
                "highdma": "on [fixed]",
                "hsr_dup_offload": "off [fixed]",
                "hsr_fwd_offload": "off [fixed]",
                "hsr_tag_ins_offload": "off [fixed]",
                "hsr_tag_rm_offload": "off [fixed]",
                "hw_tc_offload": "off [fixed]",
                "l2_fwd_offload": "off [fixed]",
                "large_receive_offload": "off [fixed]",
                "loopback": "off [fixed]",
                "macsec_hw_offload": "off [fixed]",
                "ntuple_filters": "off [fixed]",
                "receive_hashing": "on",
                "rx_all": "off",
                "rx_checksumming": "on",
                "rx_fcs": "off",
                "rx_gro_hw": "off [fixed]",
                "rx_gro_list": "off",
                "rx_udp_gro_forwarding": "off",
                "rx_udp_tunnel_port_offload": "off [fixed]",
                "rx_vlan_filter": "on [fixed]",
                "rx_vlan_offload": "on",
                "rx_vlan_stag_filter": "off [fixed]",
                "rx_vlan_stag_hw_parse": "off [fixed]",
                "scatter_gather": "on",
                "tcp_segmentation_offload": "on",
                "tls_hw_record": "off [fixed]",
                "tls_hw_rx_offload": "off [fixed]",
                "tls_hw_tx_offload": "off [fixed]",
                "tx_checksum_fcoe_crc": "off [fixed]",
                "tx_checksum_ip_generic": "on",
                "tx_checksum_ipv4": "off [fixed]",
                "tx_checksum_ipv6": "off [fixed]",
                "tx_checksum_sctp": "off [fixed]",
                "tx_checksumming": "on",
                "tx_esp_segmentation": "off [fixed]",
                "tx_fcoe_segmentation": "off [fixed]",
                "tx_gre_csum_segmentation": "off [fixed]",
                "tx_gre_segmentation": "off [fixed]",
                "tx_gso_list": "off [fixed]",
                "tx_gso_partial": "off [fixed]",
                "tx_gso_robust": "off [fixed]",
                "tx_ipxip4_segmentation": "off [fixed]",
                "tx_ipxip6_segmentation": "off [fixed]",
                "tx_nocache_copy": "off",
                "tx_scatter_gather": "on",
                "tx_scatter_gather_fraglist": "off [fixed]",
                "tx_sctp_segmentation": "off [fixed]",
                "tx_tcp6_segmentation": "on",
                "tx_tcp_ecn_segmentation": "off [fixed]",
                "tx_tcp_mangleid_segmentation": "off",
                "tx_tcp_segmentation": "on",
                "tx_tunnel_remcsum_segmentation": "off [fixed]",
                "tx_udp_segmentation": "off [fixed]",
                "tx_udp_tnl_csum_segmentation": "off [fixed]",
                "tx_udp_tnl_segmentation": "off [fixed]",
                "tx_vlan_offload": "on",
                "tx_vlan_stag_hw_insert": "off [fixed]",
                "vlan_challenged": "off [fixed]"
            },
            "hw_timestamp_filters": [],
            "ipv4": {
                "address": "192.168.25.147",
                "broadcast": "192.168.25.255",
                "netmask": "255.255.255.0",
                "network": "192.168.25.0",
                "prefix": "24"
            },
            "ipv6": [
                {
                    "address": "fe80::20c:29ff:fed7:8623",
                    "prefix": "64",
                    "scope": "link"
                }
            ],
            "macaddress": "00:0c:29:d7:86:23",
            "module": "e1000e",
            "mtu": 1500,
            "pciid": "0000:1a:00.0",
            "promisc": false,
            "speed": 1000,
            "timestamping": [],
            "type": "ether"
        },
        "enp2s0": {
            "active": true,
            "device": "enp2s0",
            "features": {
                "esp_hw_offload": "off [fixed]",
                "esp_tx_csum_hw_offload": "off [fixed]",
                "generic_receive_offload": "on",
                "generic_segmentation_offload": "on",
                "highdma": "on [fixed]",
                "hsr_dup_offload": "off [fixed]",
                "hsr_fwd_offload": "off [fixed]",
                "hsr_tag_ins_offload": "off [fixed]",
                "hsr_tag_rm_offload": "off [fixed]",
                "hw_tc_offload": "off [fixed]",
                "l2_fwd_offload": "off [fixed]",
                "large_receive_offload": "off [fixed]",
                "loopback": "off [fixed]",
                "macsec_hw_offload": "off [fixed]",
                "ntuple_filters": "off [fixed]",
                "receive_hashing": "on",
                "rx_all": "off",
                "rx_checksumming": "on",
                "rx_fcs": "off",
                "rx_gro_hw": "off [fixed]",
                "rx_gro_list": "off",
                "rx_udp_gro_forwarding": "off",
                "rx_udp_tunnel_port_offload": "off [fixed]",
                "rx_vlan_filter": "on [fixed]",
                "rx_vlan_offload": "on",
                "rx_vlan_stag_filter": "off [fixed]",
                "rx_vlan_stag_hw_parse": "off [fixed]",
                "scatter_gather": "on",
                "tcp_segmentation_offload": "on",
                "tls_hw_record": "off [fixed]",
                "tls_hw_rx_offload": "off [fixed]",
                "tls_hw_tx_offload": "off [fixed]",
                "tx_checksum_fcoe_crc": "off [fixed]",
                "tx_checksum_ip_generic": "on",
                "tx_checksum_ipv4": "off [fixed]",
                "tx_checksum_ipv6": "off [fixed]",
                "tx_checksum_sctp": "off [fixed]",
                "tx_checksumming": "on",
                "tx_esp_segmentation": "off [fixed]",
                "tx_fcoe_segmentation": "off [fixed]",
                "tx_gre_csum_segmentation": "off [fixed]",
                "tx_gre_segmentation": "off [fixed]",
                "tx_gso_list": "off [fixed]",
                "tx_gso_partial": "off [fixed]",
                "tx_gso_robust": "off [fixed]",
                "tx_ipxip4_segmentation": "off [fixed]",
                "tx_ipxip6_segmentation": "off [fixed]",
                "tx_nocache_copy": "off",
                "tx_scatter_gather": "on",
                "tx_scatter_gather_fraglist": "off [fixed]",
                "tx_sctp_segmentation": "off [fixed]",
                "tx_tcp6_segmentation": "on",
                "tx_tcp_ecn_segmentation": "off [fixed]",
                "tx_tcp_mangleid_segmentation": "off",
                "tx_tcp_segmentation": "on",
                "tx_tunnel_remcsum_segmentation": "off [fixed]",
                "tx_udp_segmentation": "off [fixed]",
                "tx_udp_tnl_csum_segmentation": "off [fixed]",
                "tx_udp_tnl_segmentation": "off [fixed]",
                "tx_vlan_offload": "on",
                "tx_vlan_stag_hw_insert": "off [fixed]",
                "vlan_challenged": "off [fixed]"
            },
            "hw_timestamp_filters": [],
            "ipv4": {
                "address": "192.168.209.177",
                "broadcast": "192.168.209.255",
                "netmask": "255.255.255.0",
                "network": "192.168.209.0",
                "prefix": "24"
            },
            "ipv6": [
                {
                    "address": "fe80::20c:29ff:fed7:8619",
                    "prefix": "64",
                    "scope": "link"
                }
            ],
            "macaddress": "00:0c:29:d7:86:19",
            "module": "e1000e",
            "mtu": 1500,
            "pciid": "0000:02:00.0",
            "promisc": false,
            "speed": 1000,
            "timestamping": [],
            "type": "ether"
        },
        "env": {
            "HOME": "/root",
            "LANG": "en_US.UTF-8",
            "LOGNAME": "root",
            "LS_COLORS": "rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.m4a=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.oga=01;36:*.opus=01;36:*.spx=01;36:*.xspf=01;36:",
            "MAIL": "/var/mail/root",
            "PATH": "/sbin:/bin:/usr/sbin:/usr/bin",
            "PWD": "/home/alex",
            "SHELL": "/bin/bash",
            "SHLVL": "0",
            "SUDO_COMMAND": "/bin/sh -c echo BECOME-SUCCESS-xngdvgjengcntusgtwwcwtxuzrwaadfw ; /usr/bin/python3.9 /home/alex/.ansible/tmp/ansible-tmp-1782852113.625232-9083-165882968550796/AnsiballZ_setup.py",
            "SUDO_GID": "1001",
            "SUDO_UID": "1001",
            "SUDO_USER": "alex",
            "TERM": "xterm-256color",
            "USER": "root",
            "_": "/usr/bin/python3.9"
        },
        "fibre_channel_wwn": [],
        "fips": false,
        "form_factor": "Other",
        "fqdn": "localhost.localdomain",
        "gather_subset": [
            "all"
        ],
        "hostname": "localhost",
        "hostnqn": "nqn.2014-08.org.nvmexpress:uuid:20aa4d56-a6e3-e861-befd-ddcb7a5bce85",
        "interfaces": [
            "enp26s0",
            "enp2s0",
            "lo"
        ],
        "is_chroot": false,
        "iscsi_iqn": "",
        "kernel": "5.14.0-611.5.1.el9_7.aarch64",
        "kernel_version": "#1 SMP PREEMPT_DYNAMIC Tue Nov 11 17:55:12 EST 2025",
        "lo": {
            "active": true,
            "device": "lo",
            "features": {
                "esp_hw_offload": "off [fixed]",
                "esp_tx_csum_hw_offload": "off [fixed]",
                "generic_receive_offload": "on",
                "generic_segmentation_offload": "on",
                "highdma": "on [fixed]",
                "hsr_dup_offload": "off [fixed]",
                "hsr_fwd_offload": "off [fixed]",
                "hsr_tag_ins_offload": "off [fixed]",
                "hsr_tag_rm_offload": "off [fixed]",
                "hw_tc_offload": "off [fixed]",
                "l2_fwd_offload": "off [fixed]",
                "large_receive_offload": "off [fixed]",
                "loopback": "on [fixed]",
                "macsec_hw_offload": "off [fixed]",
                "ntuple_filters": "off [fixed]",
                "receive_hashing": "off [fixed]",
                "rx_all": "off [fixed]",
                "rx_checksumming": "on [fixed]",
                "rx_fcs": "off [fixed]",
                "rx_gro_hw": "off [fixed]",
                "rx_gro_list": "off",
                "rx_udp_gro_forwarding": "off",
                "rx_udp_tunnel_port_offload": "off [fixed]",
                "rx_vlan_filter": "off [fixed]",
                "rx_vlan_offload": "off [fixed]",
                "rx_vlan_stag_filter": "off [fixed]",
                "rx_vlan_stag_hw_parse": "off [fixed]",
                "scatter_gather": "on",
                "tcp_segmentation_offload": "on",
                "tls_hw_record": "off [fixed]",
                "tls_hw_rx_offload": "off [fixed]",
                "tls_hw_tx_offload": "off [fixed]",
                "tx_checksum_fcoe_crc": "off [fixed]",
                "tx_checksum_ip_generic": "on [fixed]",
                "tx_checksum_ipv4": "off [fixed]",
                "tx_checksum_ipv6": "off [fixed]",
                "tx_checksum_sctp": "on [fixed]",
                "tx_checksumming": "on",
                "tx_esp_segmentation": "off [fixed]",
                "tx_fcoe_segmentation": "off [fixed]",
                "tx_gre_csum_segmentation": "off [fixed]",
                "tx_gre_segmentation": "off [fixed]",
                "tx_gso_list": "on",
                "tx_gso_partial": "off [fixed]",
                "tx_gso_robust": "off [fixed]",
                "tx_ipxip4_segmentation": "off [fixed]",
                "tx_ipxip6_segmentation": "off [fixed]",
                "tx_nocache_copy": "off [fixed]",
                "tx_scatter_gather": "on [fixed]",
                "tx_scatter_gather_fraglist": "on [fixed]",
                "tx_sctp_segmentation": "on",
                "tx_tcp6_segmentation": "on",
                "tx_tcp_ecn_segmentation": "on",
                "tx_tcp_mangleid_segmentation": "on",
                "tx_tcp_segmentation": "on",
                "tx_tunnel_remcsum_segmentation": "off [fixed]",
                "tx_udp_segmentation": "on",
                "tx_udp_tnl_csum_segmentation": "off [fixed]",
                "tx_udp_tnl_segmentation": "off [fixed]",
                "tx_vlan_offload": "off [fixed]",
                "tx_vlan_stag_hw_insert": "off [fixed]",
                "vlan_challenged": "on [fixed]"
            },
            "hw_timestamp_filters": [],
            "ipv4": {
                "address": "127.0.0.1",
                "broadcast": "",
                "netmask": "255.0.0.0",
                "network": "127.0.0.0",
                "prefix": "8"
            },
            "ipv6": [
                {
                    "address": "::1",
                    "prefix": "128",
                    "scope": "host"
                }
            ],
            "mtu": 65536,
            "promisc": false,
            "timestamping": [],
            "type": "loopback"
        },
        "loadavg": {
            "15m": 0.01,
            "1m": 0.12,
            "5m": 0.04
        },
        "locally_reachable_ips": {
            "ipv4": [
                "127.0.0.0/8",
                "127.0.0.1",
                "192.168.25.147",
                "192.168.209.177"
            ],
            "ipv6": [
                "::1",
                "fe80::20c:29ff:fed7:8619",
                "fe80::20c:29ff:fed7:8623"
            ]
        },
        "lsb": {},
        "lvm": {
            "lvs": {},
            "pvs": {},
            "vgs": {}
        },
        "machine": "aarch64",
        "machine_id": "c273435379134e3f8b29c556d35b5308",
        "memfree_mb": 1476,
        "memory_mb": {
            "nocache": {
                "free": 1652,
                "used": 303
            },
            "real": {
                "free": 1476,
                "total": 1955,
                "used": 479
            },
            "swap": {
                "cached": 0,
                "free": 4030,
                "total": 4030,
                "used": 0
            }
        },
        "memtotal_mb": 1955,
        "module_setup": true,
        "mounts": [
            {
                "block_available": 15107970,
                "block_size": 4096,
                "block_total": 15574784,
                "block_used": 466814,
                "device": "/dev/nvme0n1p3",
                "dump": 0,
                "fstype": "xfs",
                "inode_available": 31146042,
                "inode_total": 31182336,
                "inode_used": 36294,
                "mount": "/",
                "options": "rw,seclabel,relatime,attr2,inode64,logbufs=8,logbsize=32k,noquota",
                "passno": 0,
                "size_available": 61882245120,
                "size_total": 63794315264,
                "uuid": "8cac1a76-12b8-48cb-9106-a56e21d96853"
            },
            {
                "block_available": 151415,
                "block_size": 4096,
                "block_total": 153296,
                "block_used": 1881,
                "device": "/dev/nvme0n1p1",
                "dump": 0,
                "fstype": "vfat",
                "inode_available": 0,
                "inode_total": 0,
                "inode_used": 0,
                "mount": "/boot/efi",
                "options": "rw,relatime,fmask=0077,dmask=0077,codepage=437,iocharset=ascii,shortname=winnt,errors=remount-ro",
                "passno": 0,
                "size_available": 620195840,
                "size_total": 627900416,
                "uuid": "9175-A449"
            }
        ],
        "nodename": "localhost.localdomain",
        "os_family": "RedHat",
        "pkg_mgr": "dnf",
        "proc_cmdline": {
            "BOOT_IMAGE": "(hd0,gpt3)/boot/vmlinuz-5.14.0-611.5.1.el9_7.aarch64",
            "console": [
                "tty0",
                "ttyS0,115200n8"
            ],
            "no_timer_check": true,
            "ro": true,
            "root": "UUID=8cac1a76-12b8-48cb-9106-a56e21d96853"
        },
        "processor": [
            "0",
            "1"
        ],
        "processor_cores": 1,
        "processor_count": 2,
        "processor_nproc": 2,
        "processor_threads_per_core": 1,
        "processor_vcpus": 2,
        "product_name": "VMware20,1",
        "product_serial": "VMware-56 4d b3 89 e8 6b aa ac-69 b0 02 3c 0d d7 86 19",
        "product_uuid": "89b34d56-6be8-acaa-69b0-023c0dd78619",
        "product_version": "1",
        "python": {
            "executable": "/usr/bin/python3.9",
            "has_sslcontext": true,
            "type": "cpython",
            "version": {
                "major": 3,
                "micro": 23,
                "minor": 9,
                "releaselevel": "final",
                "serial": 0
            },
            "version_info": [
                3,
                9,
                23,
                "final",
                0
            ]
        },
        "python_version": "3.9.23",
        "real_group_id": 0,
        "real_user_id": 0,
        "selinux": {
            "config_mode": "enforcing",
            "mode": "enforcing",
            "policyvers": 33,
            "status": "enabled",
            "type": "targeted"
        },
        "selinux_python_present": true,
        "service_mgr": "systemd",
        "ssh_host_key_ecdsa_public": "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGGp6kHseSenOvU5sCCBFZzJvZtf6/Hhhrd5qQzJbSu5hS3s+6a8eTx3iDp5NNNR/QYVY2gCo84nAVPqxJFzJ2M=",
        "ssh_host_key_ecdsa_public_keytype": "ecdsa-sha2-nistp256",
        "ssh_host_key_ed25519_public": "AAAAC3NzaC1lZDI1NTE5AAAAIEAPnL4iz8MyzQufR4HqTF/DrqSqsLn2BkZJ+N0xXIpo",
        "ssh_host_key_ed25519_public_keytype": "ssh-ed25519",
        "ssh_host_key_rsa_public": "AAAAB3NzaC1yc2EAAAADAQABAAABgQDRYbGsaJBeiJEF66hCk2UGzWcLU8AvXPFT8SucHGdwwaMI79wB4iBzPfbdQhHaVilC7v+Ke09N1tvngKIYkOeMmtaAVF0Wdn9gSXQQzgvpLAn6vuyKWuF1jXvnl2aLiRVEgTL9xXWTs0w6cexEN5ST1m+PUEc7VE8ecWUmvM5yCck+olxDE32PDzft2v6XMUnnAQOvfpmi8dUXr8hcWxQ6TeDD5vuXswFis/JomMrBK4chRvlirf+GqvHm5kobzZqtOUA1hOWR1hP4iAcw44xxAfrbRegfY3Y1cWPvikPWquI3fM88KdlAi8xVtKkPq+1QJ4lyNQBbubZb/AmLPgTSepZ1/TaStNbgQ9sS2DhbUjalyXC/u2f/GLM0rXqNwYw3OJkVRt4/99Pe4boWO3b11toF2xs4nNKFrwMGnI1LSyAj+qCx+af3B4UO7zyEy2WjZxRURKwA03LiF8L8IPl7lMQ5R0sPx08xZADUlcAF6SUqBEw4BIQbveJuviRk8ss=",
        "ssh_host_key_rsa_public_keytype": "ssh-rsa",
        "swapfree_mb": 4030,
        "swaptotal_mb": 4030,
        "system": "Linux",
        "system_capabilities": [],
        "system_capabilities_enforced": "False",
        "system_vendor": "VMware, Inc.",
        "systemd": {
            "features": "+PAM +AUDIT +SELINUX -APPARMOR +IMA +SMACK +SECCOMP +GCRYPT +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 -IDN -IPTC +KMOD +LIBCRYPTSETUP +LIBFDISK +PCRE2 -PWQUALITY +P11KIT -QRENCODE +TPM2 +BZIP2 +LZ4 +XZ +ZLIB +ZSTD -BPF_FRAMEWORK +XKBCOMMON +UTMP +SYSVINIT default-hierarchy=unified",
            "version": 252
        },
        "uptime_seconds": 1001,
        "user_dir": "/root",
        "user_gecos": "root",
        "user_gid": 0,
        "user_id": "root",
        "user_shell": "/bin/bash",
        "user_uid": 0,
        "userspace_bits": "64",
        "virtualization_role": "guest",
        "virtualization_tech_guest": [
            "VMware"
        ],
        "virtualization_tech_host": [],
        "virtualization_type": "VMware"
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.147             : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/06/30 15:41:54  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p90
╰→
```

### Playbook Vars

`ansible-playbook -i inventory playbook-vars.yaml`
```
╰→ ansible-playbook -i inventory playbook-vars.yaml 

PLAY [Echoing Vars] **************************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.147' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.147]

TASK [Echo var] ******************************************************************************
changed: [192.168.25.147]

TASK [Print result] **************************************************************************
ok: [192.168.25.147] => {
    "response": {
        "changed": true,
        "cmd": [
            "/bin/echo",
            "Hello World Alexandra"
        ],
        "delta": "0:00:00.002774",
        "end": "2026-06-30 20:57:13.421471",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2026-06-30 20:57:13.418697",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "Hello World Alexandra",
        "stdout_lines": [
            "Hello World Alexandra"
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.147             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/06/30 15:57:14  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p90
```

## Playbook External Vars

`ansible-playbook -i inventory playbook-vars-2.yaml`
```
╰→ ansible-playbook -i inventory playbook-vars-2.yaml 

PLAY [Echoing Vars] **************************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.147' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.147]

TASK [Echo var] ******************************************************************************
changed: [192.168.25.147]

TASK [Print result] **************************************************************************
ok: [192.168.25.147] => {
    "response": {
        "changed": true,
        "cmd": [
            "/bin/echo",
            "Hello World Anna"
        ],
        "delta": "0:00:00.001465",
        "end": "2026-06-30 21:00:51.325044",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2026-06-30 21:00:51.323579",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "Hello World Anna",
        "stdout_lines": [
            "Hello World Anna"
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.147             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/06/30 16:00:51  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p90 
╰→
```


Página 99


Playbook Vars (Prompt)

ansible-playbook -i inventory playbook-vars-3.yaml 
```
╰→ ansible-playbook -i inventory playbook-vars-3.yaml 
What's the name? [Ada]: Aixa

PLAY [Echoing Vars] **************************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.147' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.147]

TASK [Echo var] ******************************************************************************
changed: [192.168.25.147]

TASK [Print result] **************************************************************************
ok: [192.168.25.147] => {
    "response": {
        "changed": true,
        "cmd": [
            "/bin/echo",
            "Hello World Aixa"
        ],
        "delta": "0:00:00.001377",
        "end": "2026-06-30 21:15:11.408632",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2026-06-30 21:15:11.407255",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "Hello World Aixa",
        "stdout_lines": [
            "Hello World Aixa"
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.147             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/06/30 16:15:11  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p99
```


## Playbook External Vars with Crypto

`ansible-playbook -i inventory playbook-vars-4.yaml`
```
╰→ ansible-playbook -i inventory playbook-vars-4.yaml 
Enter the password: 
confirm Enter the password: 

PLAY [Echoing Vars] **************************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.147' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.147]

TASK [Echo var] ******************************************************************************
changed: [192.168.25.147]

TASK [Print result] **************************************************************************
ok: [192.168.25.147] => {
    "response": {
        "changed": true,
        "cmd": [
            "/bin/echo",
            "Password '$6$rounds=656000$eFuROOv$sVqv9IlDp8h6XcI0gNLwbCvlBdadt/R53GRX8iKmxGgsJ0ZWmgJpHadoBWlsaa//YAnZOdPnpQ4ZPugk2VNR00'"
        ],
        "delta": "0:00:00.001623",
        "end": "2026-06-30 21:24:14.034216",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2026-06-30 21:24:14.032593",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "Password '$6$rounds=656000$eFuROOv$sVqv9IlDp8h6XcI0gNLwbCvlBdadt/R53GRX8iKmxGgsJ0ZWmgJpHadoBWlsaa//YAnZOdPnpQ4ZPugk2VNR00'",
        "stdout_lines": [
            "Password '$6$rounds=656000$eFuROOv$sVqv9IlDp8h6XcI0gNLwbCvlBdadt/R53GRX8iKmxGgsJ0ZWmgJpHadoBWlsaa//YAnZOdPnpQ4ZPugk2VNR00'"
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.147             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/06/30 16:24:14  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p99 
╰→
```

## Ansible Vault

`ansible-vault create prod.yaml`
```
╭ 2026/06/30 16:26:23  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p99 
╰→ command cat prod.yaml 
$ANSIBLE_VAULT;1.1;AES256
35373138313235616664623935386265636564323965373163653535356463623038316437666137
3232393435303133396431663734346332343139303166330a656333323365356438383731393763
32643762633561343765666331376462616532623832633337616431613762353932326331356237
6665383535336538330a653536663564626435396165613336633465623432363531343064343764
64666465313038636233616337323531373932376134613635633335646235613231653564383162
3465376335643861636134376439666663346462633330646132
╭ 2026/06/30 16:26:34  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p99 
╰→
```

## Use Ansible Vault

`ansible-playbook -i inventory --extra-vars "@prod-yaml" --ask-vault-pass playbook-enc.yaml`
```
╰→ ansible-playbook -i inventory --extra-vars "@prod.yaml" --ask-vault-pass playbook-enc.yaml
Vault password: 

PLAY [Echoing vars] **************************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.147' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.147]

TASK [Echo var] ******************************************************************************
changed: [192.168.25.147]

TASK [Print result] **************************************************************************
ok: [192.168.25.147] => {
    "response": {
        "changed": true,
        "cmd": [
            "/bin/echo",
            "The username is Secret1 and the password Secret2"
        ],
        "delta": "0:00:00.001461",
        "end": "2026-06-30 21:33:50.510843",
        "failed": false,
        "msg": "",
        "rc": 0,
        "start": "2026-06-30 21:33:50.509382",
        "stderr": "",
        "stderr_lines": [],
        "stdout": "The username is Secret1 and the password Secret2",
        "stdout_lines": [
            "The username is Secret1 and the password Secret2"
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.147             : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/06/30 16:33:50  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p99 
╰→
```

## Página 118
### Echo in loops

`ansible-playbook -i inventory loops-echo.yaml`
```
╭ 2026/07/01 16:26:59  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p118 
╰→ ansible-playbook -i inventory loops-echo.yaml 

PLAY [Echoing in loops] **********************************************************************

TASK [Echo var] ******************************************************************************
[WARNING]: Host '192.168.25.167' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.167] => (item=Ada)
[WARNING]: Host '192.168.25.87' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.87] => (item=Ada)
[WARNING]: Host '192.168.25.97' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.97] => (item=Ada)
changed: [192.168.25.167] => (item=Alexa)
changed: [192.168.25.87] => (item=Alexa)
changed: [192.168.25.97] => (item=Alexa)

TASK [Print result] **************************************************************************
ok: [192.168.25.167] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada"
                ],
                "delta": "0:00:00.001749",
                "end": "2026-07-01 21:27:08.640298",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:27:08.638549",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada",
                "stdout_lines": [
                    "Hello World Ada"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa"
                ],
                "delta": "0:00:00.002047",
                "end": "2026-07-01 21:27:08.903825",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:27:08.901778",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa",
                "stdout_lines": [
                    "Hello World Alexa"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.167' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}
ok: [192.168.25.97] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada"
                ],
                "delta": "0:00:00.001807",
                "end": "2026-07-01 21:27:08.633987",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:27:08.632180",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada",
                "stdout_lines": [
                    "Hello World Ada"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa"
                ],
                "delta": "0:00:00.001968",
                "end": "2026-07-01 21:27:08.895522",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:27:08.893554",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa",
                "stdout_lines": [
                    "Hello World Alexa"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.97' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}
ok: [192.168.25.87] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada"
                ],
                "delta": "0:00:00.002045",
                "end": "2026-07-01 21:27:08.663161",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:27:08.661116",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada",
                "stdout_lines": [
                    "Hello World Ada"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa"
                ],
                "delta": "0:00:00.001422",
                "end": "2026-07-01 21:27:08.927354",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:27:08.925932",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa",
                "stdout_lines": [
                    "Hello World Alexa"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.87' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.167             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.25.87              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.25.97              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/07/01 16:27:09  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p118
```

## Echo in loops with pause

`ansible-playbook -i inventory loop-pause-echo.yaml`
```
╭ 2026/07/01 16:30:12  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p118 
╰→ ansible-playbook -i inventory loop-pause-echo.yaml 

PLAY [Echoing in loops] **********************************************************************

TASK [Echo var] ******************************************************************************
[WARNING]: Host '192.168.25.167' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.167] => (item=Ada)
[WARNING]: Host '192.168.25.97' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.97] => (item=Ada)
[WARNING]: Host '192.168.25.87' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.87] => (item=Ada)
changed: [192.168.25.97] => (item=Alexa)
changed: [192.168.25.167] => (item=Alexa)
changed: [192.168.25.87] => (item=Alexa)

TASK [Print result] **************************************************************************
ok: [192.168.25.167] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada"
                ],
                "delta": "0:00:00.001530",
                "end": "2026-07-01 21:30:47.641345",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:30:47.639815",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada",
                "stdout_lines": [
                    "Hello World Ada"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa"
                ],
                "delta": "0:00:00.001725",
                "end": "2026-07-01 21:30:52.919252",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:30:52.917527",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa",
                "stdout_lines": [
                    "Hello World Alexa"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.167' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}
ok: [192.168.25.97] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada"
                ],
                "delta": "0:00:00.001588",
                "end": "2026-07-01 21:30:47.658210",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:30:47.656622",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada",
                "stdout_lines": [
                    "Hello World Ada"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa"
                ],
                "delta": "0:00:00.001501",
                "end": "2026-07-01 21:30:52.932067",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:30:52.930566",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa",
                "stdout_lines": [
                    "Hello World Alexa"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.97' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}
ok: [192.168.25.87] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada"
                ],
                "delta": "0:00:00.001919",
                "end": "2026-07-01 21:30:47.603960",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:30:47.602041",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada",
                "stdout_lines": [
                    "Hello World Ada"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa"
                ],
                "delta": "0:00:00.001796",
                "end": "2026-07-01 21:30:52.880708",
                "failed": false,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:30:52.878912",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa",
                "stdout_lines": [
                    "Hello World Alexa"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.87' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.167             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.25.87              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.25.97              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/07/01 16:30:52  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p118
╰→ 
```

## Echo in indexed loops with pause
`ansible-playbook -i inventory loop-pause-echo-index.yaml`
```
╭ 2026/07/01 16:32:41  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p118 
╰→ ansible-playbook -i inventory loop-pause-echo-index.yaml 

PLAY [Echoing in loops] **********************************************************************

TASK [Echo var] ******************************************************************************
[WARNING]: Host '192.168.25.167' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.167] => (item=Ada)
[WARNING]: Host '192.168.25.87' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.87] => (item=Ada)
[WARNING]: Host '192.168.25.97' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [192.168.25.97] => (item=Ada)
changed: [192.168.25.167] => (item=Alexa)
changed: [192.168.25.97] => (item=Alexa)
changed: [192.168.25.87] => (item=Alexa)

TASK [Print result] **************************************************************************
ok: [192.168.25.167] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_index_var": "idx",
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada (0)"
                ],
                "delta": "0:00:00.001605",
                "end": "2026-07-01 21:33:11.431529",
                "failed": false,
                "idx": 0,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada (0)\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:33:11.429924",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada (0)",
                "stdout_lines": [
                    "Hello World Ada (0)"
                ]
            },
            {
                "ansible_index_var": "idx",
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa (1)"
                ],
                "delta": "0:00:00.001405",
                "end": "2026-07-01 21:33:16.718458",
                "failed": false,
                "idx": 1,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa (1)\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:33:16.717053",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa (1)",
                "stdout_lines": [
                    "Hello World Alexa (1)"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.167' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}
ok: [192.168.25.97] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_index_var": "idx",
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada (0)"
                ],
                "delta": "0:00:00.001760",
                "end": "2026-07-01 21:33:11.432007",
                "failed": false,
                "idx": 0,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada (0)\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:33:11.430247",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada (0)",
                "stdout_lines": [
                    "Hello World Ada (0)"
                ]
            },
            {
                "ansible_index_var": "idx",
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa (1)"
                ],
                "delta": "0:00:00.002125",
                "end": "2026-07-01 21:33:16.720938",
                "failed": false,
                "idx": 1,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa (1)\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:33:16.718813",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa (1)",
                "stdout_lines": [
                    "Hello World Alexa (1)"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.97' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}
ok: [192.168.25.87] => {
    "resp": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "ansible_facts": {
                    "discovered_interpreter_python": "/usr/bin/python3.9"
                },
                "ansible_index_var": "idx",
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Ada (0)"
                ],
                "delta": "0:00:00.001720",
                "end": "2026-07-01 21:33:11.419037",
                "failed": false,
                "idx": 0,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Ada (0)\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Ada",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:33:11.417317",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Ada (0)",
                "stdout_lines": [
                    "Hello World Ada (0)"
                ]
            },
            {
                "ansible_index_var": "idx",
                "ansible_loop_var": "item",
                "changed": true,
                "cmd": [
                    "/bin/echo",
                    "Hello World Alexa (1)"
                ],
                "delta": "0:00:00.001784",
                "end": "2026-07-01 21:33:16.708356",
                "failed": false,
                "idx": 1,
                "invocation": {
                    "module_args": {
                        "_raw_params": "/bin/echo \"Hello World Alexa (1)\"",
                        "_uses_shell": false,
                        "argv": null,
                        "chdir": null,
                        "cmd": null,
                        "creates": null,
                        "executable": null,
                        "expand_argument_vars": true,
                        "removes": null,
                        "stdin": null,
                        "stdin_add_newline": true,
                        "strip_empty_ends": true
                    }
                },
                "item": "Alexa",
                "msg": "",
                "rc": 0,
                "start": "2026-07-01 21:33:16.706572",
                "stderr": "",
                "stderr_lines": [],
                "stdout": "Hello World Alexa (1)",
                "stdout_lines": [
                    "Hello World Alexa (1)"
                ]
            }
        ],
        "skipped": false,
        "warnings": [
            "Host '192.168.25.87' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered."
        ]
    }
}

PLAY RECAP ***********************************************************************************
192.168.25.167             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.25.87              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.25.97              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/07/01 16:33:16  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p118
```

## Página 134
### Handlers

`ansible-playbook -i inventory -K playbook-handler.yaml`
```
╰→ ansible-playbook -i inventory -K playbook-handler.yaml 
BECOME password: 

PLAY [Update page] ***************************************************************************

TASK [Gathering Facts] ***********************************************************************
[WARNING]: Host '192.168.25.123' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.123]
[WARNING]: Host '192.168.25.181' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [192.168.25.181]
[WARNING]: Host '192.168.25.103' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
[ERROR]: Task failed: Incorrect sudo password
fatal: [192.168.25.103]: FAILED! => {"changed": false, "msg": "Task failed: Incorrect sudo password"}

TASK [copy index.html] ***********************************************************************
[ERROR]: Task failed: Module failed: Destination directory /usr/share/nginx/html does not exist
Origin: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p134/playbook-handler.yaml:5:7

3   become: true
4   tasks:
5     - name: copy index.html
        ^ column 7

fatal: [192.168.25.181]: FAILED! => {"changed": false, "checksum": "50dd1731e0733a9b2fff222c2ad44d269ad14f20", "msg": "Destination directory /usr/share/nginx/html does not exist"}
fatal: [192.168.25.123]: FAILED! => {"changed": false, "checksum": "50dd1731e0733a9b2fff222c2ad44d269ad14f20", "msg": "Destination directory /usr/share/nginx/html does not exist"}

PLAY RECAP ***********************************************************************************
192.168.25.103             : ok=0    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
192.168.25.123             : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   
192.168.25.181             : ok=1    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   

╭ 2026/07/02 11:45:03  2 eGunther ~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p134 
╰→
```

## External Variables

`ansible-playbook -i inventory -l node1 play-ext-vars.yaml`
```
╭ 2026/07/06 19:00:05  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p134 
╰→ ansible-playbook -i inventory -l node1 play-ext-vars.yaml

PLAY [Echoing Vars] **************************************************************************

TASK [Echo var] ******************************************************************************
ok: [192.168.25.103] => {
    "msg": "una_variable: 'Un valor',  segunda_variable: 'segundo valor', tercera_variable: 'tercer valor', "
}

PLAY RECAP ***********************************************************************************
192.168.25.103             : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

╭ 2026/07/06 19:00:13  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p134 
╰→
```

## Página 123
### Loop Extended Control

`ansible-playbook -i inventory loop-ext-control.yaml`
```
╭ 2026/07/16 16:35:11  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p123
╰→ ansible-playbook -i inventory loop-ext-control.yaml

PLAY [Loop extended control] ****************************************************************

TASK [Show all data] ************************************************************************
ok: [192.168.25.115] => (item=192.168.25.115) => {
    "msg": "Indexes: - Index0 0 - Index1 1\n"
}
ok: [192.168.25.157] => (item=192.168.25.115) => {
    "msg": "Indexes: - Index0 0 - Index1 1\n"
}
ok: [192.168.25.115] => (item=192.168.25.157) => {
    "msg": "Indexes: - Index0 1 - Index1 2\n"
}
ok: [192.168.25.115] => (item=192.168.25.143) => {
    "msg": "Indexes: - Index0 2 - Index1 3\n"
}
ok: [192.168.25.157] => (item=192.168.25.157) => {
    "msg": "Indexes: - Index0 1 - Index1 2\n"
}
ok: [192.168.25.143] => (item=192.168.25.115) => {
    "msg": "Indexes: - Index0 0 - Index1 1\n"
}
ok: [192.168.25.157] => (item=192.168.25.143) => {
    "msg": "Indexes: - Index0 2 - Index1 3\n"
}
ok: [192.168.25.143] => (item=192.168.25.157) => {
    "msg": "Indexes: - Index0 1 - Index1 2\n"
}
ok: [192.168.25.143] => (item=192.168.25.143) => {
    "msg": "Indexes: - Index0 2 - Index1 3\n"
}

PLAY RECAP **********************************************************************************
192.168.25.115             : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.25.143             : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
192.168.25.157             : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

╭ 2026/07/16 16:35:57  0 eGunther ~/Documents/Code/Ansible/RHCE/ansible-labs/p123
╰→
```

## Página 126
### Stat a dir

`ansible-playbook -i inventory.yaml builtin-dir-stat.yaml`
```
[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p126] ansible-playbook -i inventory.yaml builtin-dir-stat.yaml

PLAY [Directory exists] *******************************************************************

TASK [Do exists SystemD directory?] *******************************************************
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [node1]
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]

TASK [Show if SystemD directory exits] ****************************************************
ok: [staging] => {
    "msg": "Directory /etc/systemd exists!"
}
ok: [prod] => {
    "msg": "Directory /etc/systemd exists!"
}
ok: [node1] => {
    "msg": "Directory /etc/systemd exists!"
}

TASK [Shof if SystemD directory does not exists] ******************************************
skipping: [staging]
skipping: [prod]
skipping: [node1]

PLAY RECAP ********************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
prod                       : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
staging                    : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p126]
```

### Stat an unexistant dir
`ansible-playbook -i inventory.yaml builtin-dir-stat.yaml -e systemddir=/etc/systemctl.d`
```
[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p126] ansible-playbook -i inventory.yaml builtin-dir-stat.yaml -e systemddir=/etc/systemctl.d

PLAY [Directory exists] *******************************************************************

TASK [Do exists SystemD directory?] *******************************************************
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [node1]

TASK [Show if SystemD directory exits] ****************************************************
skipping: [staging]
skipping: [prod]
skipping: [node1]

TASK [Shof if SystemD directory does not exists] ******************************************
ok: [staging] => {
    "msg": "Directory /etc/systemctl.d DOES NOT exists!"
}
ok: [prod] => {
    "msg": "Directory /etc/systemctl.d DOES NOT exists!"
}
ok: [node1] => {
    "msg": "Directory /etc/systemctl.d DOES NOT exists!"
}

PLAY RECAP ********************************************************************************
node1                      : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
prod                       : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
staging                    : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p126]
```

## Página 147
### Block/Rescue/Always

`ansible-playbook -i inventory block-rescue-always.yaml`
```
[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147] ansible-playbook -i inventory.yaml block-rescue-always.yaml

PLAY [Block example] **********************************************************************

TASK [Gathering Facts] ********************************************************************
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [node1]

TASK [install an invalid package] *********************************************************
[ERROR]: Task failed: Module failed: Failed to install some of the specified packages
Origin: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147/block-rescue-always.yaml:7:11

5     - name: Attempt to install a package
6       block:
7         - name: install an invalid package
            ^ column 11

fatal: [prod]: FAILED! => {"changed": false, "failures": ["No package kjdkdjkjfd available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}
fatal: [node1]: FAILED! => {"changed": false, "failures": ["No package kjdkdjkjfd available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}
fatal: [staging]: FAILED! => {"changed": false, "failures": ["No package kjdkdjkjfd available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}

TASK [ansible.builtin.debug] **************************************************************
ok: [staging] => {
    "msg": "Oh! there is an error"
}
ok: [prod] => {
    "msg": "Oh! there is an error"
}
ok: [node1] => {
    "msg": "Oh! there is an error"
}

TASK [ansible.builtin.debug] **************************************************************
ok: [staging] => {
    "msg": "This always executes"
}
ok: [prod] => {
    "msg": "This always executes"
}
ok: [node1] => {
    "msg": "This always executes"
}

PLAY RECAP ********************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
prod                       : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
staging                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147]
```

### Block/Rescue/Always with names

`ansible-playbook -i inventory.yaml block-rescue-always-with-name.yaml`
```
[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147] ansible-playbook -i inventory.yaml block-rescue-always-with-name.yaml

PLAY [Block example] **********************************************************************

TASK [Gathering Facts] ********************************************************************
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [node1]
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]

TASK [install an invalid package] *********************************************************
[ERROR]: Task failed: Module failed: Failed to install some of the specified packages
Origin: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147/block-rescue-always-with-name.yaml:7:11

5     - name: Attempt to install a package
6       block:
7         - name: install an invalid package
            ^ column 11

fatal: [node1]: FAILED! => {"changed": false, "failures": ["No package kjdkdjkjfd available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}
fatal: [staging]: FAILED! => {"changed": false, "failures": ["No package kjdkdjkjfd available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}
fatal: [prod]: FAILED! => {"changed": false, "failures": ["No package kjdkdjkjfd available."], "msg": "Failed to install some of the specified packages", "rc": 1, "results": []}

TASK [Print custom error message] *********************************************************
ok: [staging] => {
    "msg": "Oh! there is an error"
}
ok: [prod] => {
    "msg": "Oh! there is an error"
}
ok: [node1] => {
    "msg": "Oh! there is an error"
}

TASK [Print always-run message] ***********************************************************
ok: [staging] => {
    "msg": "This always executes"
}
ok: [prod] => {
    "msg": "This always executes"
}
ok: [node1] => {
    "msg": "This always executes"
}

PLAY RECAP ********************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
prod                       : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
staging                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p147]
```

## Página 127
### Line/Block Infile Module

`ansible-playbook -i inventory.yaml line-block-infile.yaml`
```
[2 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p127] ansible-playbook -i inventory.yaml line-block-infile.yaml

PLAY [Line/Block Infile Module] ***********************************************************

TASK [Insert line] ************************************************************************
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [node1]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [prod]
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
changed: [staging]

TASK [Remove line] ************************************************************************
ok: [node1]
ok: [prod]
ok: [staging]

PLAY RECAP ********************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
prod                       : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
staging                    : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p127]
```

## Página 131
### Jinja2 Templates

`ansible-playbook -i inventory.yaml jinja2-playbook.yaml`
```
[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p131] ansible-playbook -i inventory.yaml jinja2-playbook.yaml

PLAY [configuration template] *************************************************************

TASK [Gathering Facts] ********************************************************************
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [node1]
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]

TASK [Copy conf files] ********************************************************************
[WARNING]: Deprecation warnings can be disabled by setting `deprecation_warnings=False` in ansible.cfg.
[DEPRECATION WARNING]: INJECT_FACTS_AS_VARS default to `True` is deprecated, top-level facts will not be auto injected after the change. This feature will be removed from ansible-core version 2.24.
Origin: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p131/templates/conf.properties.j2

Use `ansible_facts["fact_name"]` (no `ansible_` prefix) instead.

changed: [prod]
changed: [staging]
changed: [node1]

TASK [Display conf.properties contents] ***************************************************
changed: [prod]
changed: [staging]
changed: [node1]

TASK [Print to console] *******************************************************************
ok: [staging] => {
    "msg": [
        "# File created at 2026-07-22T23:42:02Z",
        "",
        "hostname=localhost",
        "",
        "connection_pool=30",
        "",
        "db_username=Alex",
        "db_password=Alex"
    ]
}
ok: [prod] => {
    "msg": [
        "# File created at 2026-07-22T23:42:02Z",
        "",
        "hostname=localhost",
        "",
        "connection_pool=30",
        "",
        "db_username=Alex",
        "db_password=Alex"
    ]
}
ok: [node1] => {
    "msg": [
        "# File created at 2026-07-22T23:42:02Z",
        "",
        "hostname=localhost",
        "",
        "connection_pool=30",
        "",
        "db_username=Alex",
        "db_password=Alex"
    ]
}

PLAY RECAP ********************************************************************************
node1                      : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
prod                       : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
staging                    : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p131]
```

## Página 135
### Lookup

`ansible-playbook -i inventory.yaml -l node1  lookup-hosts.yaml`
```
[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p131] ansible-playbook -i inventory.yaml -l node1  lookup-hosts.yaml

PLAY [Read hosts] *************************************************************************

TASK [debug] ******************************************************************************
ok: [node1] => {
    "msg": "hosts value is ##\n# Host Database\n#\n# localhost is used to configure the loopback interface\n# when the system is booting.  Do not change this entry.\n##\n127.0.0.1\tlocalhost\n255.255.255.255\tbroadcasthost\n::1             localhost\n\n192.168.25.254\tgw.lan \n192.168.25.254\tgateway.lan\n192.168.25.15\thermes.lan\n192.168.25.16\tbender.lan\n192.168.25.9\tleela.lan\n192.168.25.240\tvios.lan\n192.168.25.241\taix1.lan\n# Added by Docker Desktop\n# To allow the same kube context to work on the host and the container:\n127.0.0.1 kubernetes.docker.internal\n# End of section"
}

PLAY RECAP ********************************************************************************
node1                      : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[0 e@Gunther:~/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p131]
```

## Página 124
### Custom module

`ansible-playbook -i ../inventory.yaml playbook-example-use.yaml`
```
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p124/module_hello] ansible-playbook -i ../inventory.yaml playbook-example-use.yaml

PLAY [CustomModule] *************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'node1' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [node1]

TASK [Executes custom module] ***************************************************************************************
ok: [node1]
ok: [prod]
ok: [staging]

TASK [dump_output] **************************************************************************************************
ok: [staging] => {
    "msg": {
        "changed": false,
        "fact": "Hello Alexandra!",
        "failed": false
    }
}
ok: [prod] => {
    "msg": {
        "changed": false,
        "fact": "Hello Alexandra!",
        "failed": false
    }
}
ok: [node1] => {
    "msg": {
        "changed": false,
        "fact": "Hello Alexandra!",
        "failed": false
    }
}

PLAY RECAP **********************************************************************************************************
node1                      : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
prod                       : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
staging                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p124/module_hello]
```

## Página 150
### Install `geerlingguy.java` role

`ansible-galaxy install geerlingguy.java`
```
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p150] ansible-galaxy install geerlingguy.java
Starting galaxy role install process
- downloading role 'java', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-java/archive/2.6.1.tar.gz
- extracting geerlingguy.java to /Users/e/.ansible/roles/geerlingguy.java
- geerlingguy.java (2.6.1) was installed successfully
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p150]
```

### Install Java on nodes with `geerlingguy.java`

`ansible-playbook -i inventory.yaml install-jdk.yaml`
```
[1 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p150] ansible-playbook -i inventory.yaml install-jdk.yaml

PLAY [Install OpenJK 1.8.0] *****************************************************************************************

TASK [Gathering Facts] **********************************************************************************************
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]

TASK [geerlingguy.java : Include OS-specific variables for Fedora or FreeBSD.] **************************************
[WARNING]: Deprecation warnings can be disabled by setting `deprecation_warnings=False` in ansible.cfg.
[DEPRECATION WARNING]: INJECT_FACTS_AS_VARS default to `True` is deprecated, top-level facts will not be auto injected after the change. This feature will be removed from ansible-core version 2.24.
Origin: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p150/install-jdk.yaml:7:13

5   roles:
6     - role: geerlingguy.java
7       when: "ansible_os_family == 'RedHat'"
              ^ column 13

Use `ansible_facts["fact_name"]` (no `ansible_` prefix) instead.

skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Include OS-specific variables for Amazon.] *************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Include version-specific variables for CentOS/RHEL.] ***************************************
ok: [staging]
ok: [prod]

TASK [geerlingguy.java : Include version-specific variables for Ubuntu.] ********************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Include version-specific variables for Debian.] ********************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Define java_packages.] *********************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
included: /Users/e/.ansible/roles/geerlingguy.java/tasks/setup-RedHat.yml for staging, prod

TASK [geerlingguy.java : Ensure Java is installed.] *****************************************************************
changed: [staging]
changed: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Set JAVA_HOME if configured.] **************************************************************
skipping: [staging]
skipping: [prod]

PLAY RECAP **********************************************************************************************************
prod                       : ok=4    changed=1    unreachable=0    failed=0    skipped=9    rescued=0    ignored=0
staging                    : ok=4    changed=1    unreachable=0    failed=0    skipped=9    rescued=0    ignored=0

[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p150]
```

### Again

```
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p150] ansible-playbook -i inventory.yaml install-jdk.yaml

PLAY [Install OpenJK 1.8.0] *****************************************************************************************

TASK [Gathering Facts] **********************************************************************************************
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]

TASK [geerlingguy.java : Include OS-specific variables for Fedora or FreeBSD.] **************************************
[WARNING]: Deprecation warnings can be disabled by setting `deprecation_warnings=False` in ansible.cfg.
[DEPRECATION WARNING]: INJECT_FACTS_AS_VARS default to `True` is deprecated, top-level facts will not be auto injected after the change. This feature will be removed from ansible-core version 2.24.
Origin: /Users/e/Dropbox/Documents/Code/Ansible/RHCE/ansible-labs/p150/install-jdk.yaml:7:13

5   roles:
6     - role: geerlingguy.java
7       when: "ansible_os_family == 'RedHat'"
              ^ column 13

Use `ansible_facts["fact_name"]` (no `ansible_` prefix) instead.

skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Include OS-specific variables for Amazon.] *************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Include version-specific variables for CentOS/RHEL.] ***************************************
ok: [staging]
ok: [prod]

TASK [geerlingguy.java : Include version-specific variables for Ubuntu.] ********************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Include version-specific variables for Debian.] ********************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Define java_packages.] *********************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
included: /Users/e/.ansible/roles/geerlingguy.java/tasks/setup-RedHat.yml for staging, prod

TASK [geerlingguy.java : Ensure Java is installed.] *****************************************************************
ok: [staging]
ok: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : include_tasks] *****************************************************************************
skipping: [staging]
skipping: [prod]

TASK [geerlingguy.java : Set JAVA_HOME if configured.] **************************************************************
skipping: [staging]
skipping: [prod]

PLAY RECAP **********************************************************************************************************
prod                       : ok=4    changed=0    unreachable=0    failed=0    skipped=9    rescued=0    ignored=0
staging                    : ok=4    changed=0    unreachable=0    failed=0    skipped=9    rescued=0    ignored=0

[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p150]
```

## Página 154
### Create/develop new role

`ansible-galaxy role init printfile`, `ansible-galaxy role install -r roles/requirements.yaml` 
```
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] ansible-galaxy role init printfile
- Role printfile was created successfully
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] ls -l
.rw-r--r--@  37 e 23 Jul 10:42 -N 󱁻 ansible.cfg
drwxr-xr-x@   - e 23 Jul 10:46 -N  printfile
.rw-r--r--@ 964 e 23 Jul 10:42 -N ⍱ Vagrantfile
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] cd printfile/
/Users/e/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile] ls -l
drwxr-xr-x@    - e 23 Jul 10:46 -N  defaults
drwxr-xr-x@    - e 23 Jul 10:46 --  files
drwxr-xr-x@    - e 23 Jul 10:46 -N  handlers
drwxr-xr-x@    - e 23 Jul 10:46 -N  meta
.rw-r--r--@ 1.3k e 23 Jul 10:46 -N 󰂺 README.md
drwxr-xr-x@    - e 23 Jul 10:46 -N  tasks
drwxr-xr-x@    - e 23 Jul 10:46 --  templates
drwxr-xr-x@    - e 23 Jul 10:46 -N  tests
drwxr-xr-x@    - e 23 Jul 10:46 -N  vars
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile] zed tasks/main.yml
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile] zed vars/main.yml
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile] cd ..
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] tar -czvf printfile.tar.gz printfile/
a printfile
a printfile/vars
a printfile/tasks
a printfile/tests
a printfile/meta
a printfile/README.md
a printfile/defaults
a printfile/files
a printfile/templates
a printfile/handlers
a printfile/handlers/main.yml
a printfile/defaults/main.yml
a printfile/meta/main.yml
a printfile/tests/test.yml
a printfile/tests/inventory
a printfile/tasks/main.yml
a printfile/vars/main.yml
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] mkdir roles
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] zed roles/requirements.yaml
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] zed play-use-role.yaml
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] ansible-galaxy role install -r roles/requirements.yaml
Starting galaxy role install process
- downloading role from file:///Users/e/Documents/Code/Ansible/RHCE/ansible-labs/p154/printfile.tar.gz
- extracting printfile to /Users/e/.ansible/roles/printfile
- printfile was installed successfully
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154]
```

### Run Playbook using role

`ansible-playbook -i inventory.yaml play-use-role.yaml`
```
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] ansible-playbook -i inventory.yaml play-use-role.yaml

PLAY [use role] *****************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]

TASK [Print Hosts] **************************************************************************************************
included: printfile for staging, prod

TASK [printfile : Display file contents] ****************************************************************************
changed: [prod]
changed: [staging]

TASK [printfile : Print to console] *********************************************************************************
ok: [staging] => {
    "msg": "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6"
}
ok: [prod] => {
    "msg": "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6"
}

PLAY RECAP **********************************************************************************************************
prod                       : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
staging                    : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154]
```

### Run again, after a handler is defined

```
[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154] ansible-playbook -i inventory.yaml play-use-role.yaml

PLAY [use role] *****************************************************************************************************

TASK [Gathering Facts] **********************************************************************************************
[WARNING]: Host 'staging' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [staging]
[WARNING]: Host 'prod' is using the discovered Python interpreter at '/usr/bin/python3.9', but future installation of another Python interpreter could cause a different interpreter to be discovered. See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html for more information.
ok: [prod]

TASK [Print Hosts] **************************************************************************************************
included: printfile for staging, prod

TASK [printfile : Display file contents] ****************************************************************************
changed: [prod]
changed: [staging]

TASK [printfile : Print to console] *********************************************************************************
ok: [staging] => {
    "msg": "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6"
}
ok: [prod] => {
    "msg": "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4\n::1         localhost localhost.localdomain localhost6 localhost6.localdomain6"
}

PLAY RECAP **********************************************************************************************************
prod                       : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
staging                    : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[0 e@Gunther:~/Documents/Code/Ansible/RHCE/ansible-labs/p154]
```
