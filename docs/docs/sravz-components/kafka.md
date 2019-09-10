---
layout: default
title: Kafka
parent: Sravz Components
nav_order: 6
comments: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Sravz Node

Ensure [Sravz Node]({{ site.baseurl }}{% link docs/sravz-node.md %}#Development Environment) works

Ensure [Zookeeper]({{ site.baseurl }}{% link docs/sravz-components/zookeeper.md %}) installed and works

## Ansible playbook run

```bash
# In the Vagrant VM change directory to Ansible direcotry
vagrant@vagrant:~$ cd ~/training/Ansible
# Verify ansible works
vagrant@vagrant:~/training/Ansible$ ansible vagrant -m ping
vagrant | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
# Install ansible galaxy roles
vagrant@vagrant:~/training/Ansible$ ansible-galaxy install --roles-path ./roles/galaxy -r requirements.yml
# Run the playbook
vagrant@vagrant:~/training/Ansible$ ansible-playbook -v playbooks/kafka.yml
```

## Verify kafka status

```bash
vagrant@vagrant:~$ echo dump | nc localhost 2181 | grep brokers
	/brokers/ids/3
	/brokers/ids/1
	/brokers/ids/2
```
