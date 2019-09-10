---
layout: default
title: Mongod DB
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
vagrant@vagrant:~/training/Ansible$ ansible-playbook -v playbooks/mongodb.yml
```

## Verify Mongodb Shard Status

```bash
vagrant@vagrant:~$ mongo admin  --port 26000 -u admin -p "changeme" --authenticationDatabase admin --eval "sh.status()"
MongoDB shell version v4.0.10
connecting to: mongodb://127.0.0.1:26000/admin?authSource=admin&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("1c5bfb7b-f4d2-4915-b942-4e031f9136fc") }
MongoDB server version: 4.0.10
--- Sharding Status ---
  sharding version: {
  	"_id" : 1,
  	"minCompatibleVersion" : 5,
  	"currentVersion" : 6,
  	"clusterId" : ObjectId("5d3063119bd26c21ba39080c")
  }
  shards:
        {  "_id" : "replica_set1",  "host" : "replica_set1/vagrant:27000,vagrant:27001,vagrant:27002",  "state" : 1 }
        {  "_id" : "replica_set2",  "host" : "replica_set2/vagrant:27005,vagrant:27006,vagrant:27007",  "state" : 1 }
  active mongoses:
        "4.0.10" : 3
  autosplit:
        Currently enabled: yes
  balancer:
        Currently enabled:  yes
        Currently running:  no
        Failed balancer rounds in last 5 attempts:  0
        Migration Results for the last 24 hours:
                No recent migrations
  databases:
        {  "_id" : "config",  "primary" : "config",  "partitioned" : true }
                config.system.sessions
                        shard key: { "_id" : 1 }
                        unique: false
                        balancing: true
                        chunks:
                                replica_set1	1
                        { "_id" : { "$minKey" : 1 } } -->> { "_id" : { "$maxKey" : 1 } } on : replica_set1 Timestamp(1, 0)
        {  "_id" : "sravz",  "primary" : "replica_set2",  "partitioned" : true,  "version" : {  "uuid" : UUID("cf10bbb1-f809-4f68-9632-e7f9c0604354"),  "lastMod" : 1 } }
        {  "_id" : "sravz_historical",  "primary" : "replica_set2",  "partitioned" : true,  "version" : {  "uuid" : UUID("4353a2d6-14d3-4c89-bea9-fd021c1f6f44"),  "lastMod" : 1 } }
```

## Connect to Mongodb

```bash
vagrant@vagrant:~$ mongo -u admin -p changeme 127.0.0.1:26000/admin
MongoDB shell version v4.0.10
connecting to: mongodb://127.0.0.1:26000/admin?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("53e5130a-95b8-49bc-be52-b2ac51f87eb6") }
MongoDB server version: 4.0.10
Server has startup warnings:
2019-07-18T12:27:19.688+0000 I CONTROL  [main]
2019-07-18T12:27:19.688+0000 I CONTROL  [main] ** WARNING: This server is bound to localhost.
2019-07-18T12:27:19.688+0000 I CONTROL  [main] **          Remote systems will be unable to connect to this server.
2019-07-18T12:27:19.688+0000 I CONTROL  [main] **          Start the server with --bind_ip <address> to specify which IP
2019-07-18T12:27:19.688+0000 I CONTROL  [main] **          addresses it should serve responses from, or with --bind_ip_all to
2019-07-18T12:27:19.688+0000 I CONTROL  [main] **          bind to all interfaces. If this behavior is desired, start the
2019-07-18T12:27:19.688+0000 I CONTROL  [main] **          server with --bind_ip 127.0.0.1 to disable this warning.
2019-07-18T12:27:19.688+0000 I CONTROL  [main]
mongos>
```