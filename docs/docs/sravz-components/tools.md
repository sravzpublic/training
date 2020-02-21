---
layout: default
title: Kafka
parent: Sravz Components
nav_order: 7
comments: true
---

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Sravz Node

Ensure [Sravz Node]({{ site.baseurl }}{% link docs/sravz-node.md %}#Development Environment) works

## Other Ansible Playbooks

```bash
# Commands to run other playbooks
vagrant@vagrant:~$ cd ~/training/Ansible
# Install NSQ
vagrant@vagrant:~$ ansible-playbook playbooks/nsq.yml
# Install NodeJS
vagrant@vagrant:~$ ansible-playbook -v playbooks/nodejs.yml
# Install Hugo Server
vagrant@vagrant:~$ ansible-playbook -v playbooks/hugo.yml
```

