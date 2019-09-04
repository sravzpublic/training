# Training
[Sravz](https://sravz.com) Training Material

Directories:<br/>
Vagrant: Contains Sravz Node Vagrant file<br/>
Ansible: Contains Sravz Node Ansible roles

Steps:
1) Spin up a vagrant based Ubuntu 18.04 machine for development<br/>
a. Ensure vagrant and virtualbox are installed<br/>
b. cd ../training/Vagrant directory<br/>
```
vagrant up
vagrant ssh
```
e. verify ansible works<br/>
```
    vagrant@vagrant:~/training/Ansible$ ansible vagrant -m ping
    vagrant | SUCCESS => {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
        },
        "changed": false,
        "ping": "pong"
    }
```
f. Install ansible galaxy roles<br/>
```
vagrant@vagrant:~/training/Ansible$ ansible-galaxy install --roles-path ./roles/galaxy -r requirements.yml
```

Test ansible playbooks:<br/>

Mongodb Sharded Cluster Installation<br/>
Mongodb playbook is based on: https://github.com/twoyao/ansible-mongodb-cluster<br/>
The playbook has been udpated to support Ubuntu 18.04 + Mongodb 4.0<br/>

Customization Steps:
1) Update Ansible/host_vars/vagrant/vars.yml

Installation Steps:<br/>
1) ssh into vagrant machine<br/>
```
   vagrant ssh
```
2) cd ~/training/Ansible directory
3) run mongodb playbook<br/>
```
   ansible-playbook -v playbooks/mongodb.yml
```

4) Verify shard status
```
$ mongo admin  --port 26000 -u admin -p "changeme" --authenticationDatabase admin --eval "sh.status()"
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
5) To connect to mongodb:
```
$ mongo -u admin -p changeme 127.0.0.1:26000/admin
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

Single Node ZooKeeper Installation<br/>
ZooKeeper playbook is based on: https://github.com/sansible/zookeeper<br/>
The playbook has been udpated to support Ubuntu 18.04<br/>

Customization Steps:
1) Update Ansible/host_vars/vagrant/vars.yml

Installation Steps:<br/>
1) ssh into vagrant machine<br/>
```
   vagrant ssh
```
2) cd ~/training/Ansible directory
3) run zookeeper playbook<br/>
```
   ansible-playbook -v playbooks/zookeeper.yml
```
4) Verify zookeeper is up
```
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
vagrant@vagrant:~/training/Ansible$
```

Single Node Kafka Installation<br/>
Kafka playbook is based on: https://github.com/sansible/kafka<br/>
The playbook has been udpated to support Ubuntu 18.04<br/>

1) ssh into vagrant machine<br/>
```
   vagrant ssh
```
2) cd ~/training/Ansible directory
3) run kafka playbook<br/>
```
   ansible-playbook -v playbooks/kafka.yml
```
4) Verify kakfa is up
```
vagrant@vagrant:~$ echo dump | nc localhost 2181 | grep brokers
	/brokers/ids/3
	/brokers/ids/1
	/brokers/ids/2
```

Sravz Development Environment: Sravz-Node setup:
```
vagrant@vagrant:~/training/Ansible$ ansible-playbook -v playbooks/sravz-node.yml
```

```
# Verify virtualenv and python3.6 installed
vagrant@vagrant:~$ source ~/.profile
vagrant@vagrant:~$ workon python3.6
(python3.6) vagrant@vagrant:~$
(python3.6) vagrant@vagrant:~$ python --version
Python 3.6.8
```
