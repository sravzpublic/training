---
layout: default
title: Zookeeper
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
vagrant@vagrant:~/training/Ansible$ ansible-playbook -v playbooks/zookeeper.yml
```

## Verify zookeeper status

```bash
vagrant@vagrant:~/training/Ansible$ /usr/share/zookeeper/bin/zkServer.sh status
ZooKeeper JMX enabled by default
Using config: /etc/zookeeper/conf/zoo.cfg
Mode: standalone

vagrant@vagrant:~/training/Ansible$ echo stat | nc localhost 2181
Zookeeper version: 3.4.10-3--1, built on Sat, 03 Feb 2018 14:58:02 -0800
Clients:
 /0:0:0:0:0:0:0:1:40928[0](queued=0,recved=1,sent=0)

Latency min/avg/max: 0/0/0
Received: 4
Sent: 3
Connections: 1
Outstanding: 0
Zxid: 0x0
Mode: standalone
Node count: 4

vagrant@vagrant:~/training/Ansible$ echo mntr | nc localhost 2181
zk_version	3.4.10-3--1, built on Sat, 03 Feb 2018 14:58:02 -0800
zk_avg_latency	0
zk_max_latency	0
zk_min_latency	0
zk_packets_received	5
zk_packets_sent	4
zk_num_alive_connections	1
zk_outstanding_requests	0
zk_server_state	standalone
zk_znode_count	4
zk_watch_count	0
zk_ephemerals_count	0
zk_approximate_data_size	27
zk_open_file_descriptor_count	45
zk_max_file_descriptor_count	4096
```
