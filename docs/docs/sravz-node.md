---
layout: default
title: Sravz Node
nav_order: 2
comments: true
---

# Configuration
{: .no_toc }

Sravz Node is an Ubuntu based virtual machine which can be used to contribute to Sravz Analytics Algorithms.
{: .fs-6 .fw-300 }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Verify Virtualbox and Vagrant are installed

```bash
# If Vagrant and Virtualbox are not installed, please install them.
$ vagrant --version
Vagrant 2.1.1
$ vboxmanage --version
5.2.12r122591
```

## Git clone Sravz training repo

```bash
# Clone Sravz training repo
$ git clone git@github.com:sravzpublic/training.git
```

## Create Vagrant VM

```bash
# Change directory to training/Vagrant directory
$ cd training/Vagrant
# Create vagrant + virtualbox based Ubuntu machine
$ vagrant up
# SSH into the VM
$ vagrant ssh
```

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
# Run sravz-node playbook, the playbook will set up python virtual environment
vagrant@vagrant:~/training/Ansible$ ansible-playbook -v playbooks/sravz-node.yml
```

## Verify python virtual environment installation

```bash
# Verify virtualenv and python3.6 installed
vagrant@vagrant:~$ source ~/.profile
vagrant@vagrant:~$ workon python3.6
# Python version should show in the prompt
(python3.6) vagrant@vagrant:~$ python --version
Python 3.6.8
```

<div id="disqus_thread"></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
/*
var disqus_config = function () {
this.page.url = 'https://sravzpublic.github.io/training/';  // Replace PAGE_URL with your page's canonical URL variable
this.page.identifier = '/training'; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
};
*/
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = 'https://sravzpublic-github-io.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>

