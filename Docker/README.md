Sravz Training Docker Image

# Commands
```bash
# To build the docker image
docker build -t sravz .

# To run the container
docker run -v /Users/fd98279/workspace/training/:/training -v /Users/fd98279/workspace/sravznew:/sravznew -v /Users/fd98279/workspace/secrets:/sravz-secrets  -it --cpuset-cpus="0-3" sravz

Sampats-MBP-2:Vagrant fd98279$ docker commit 4276f2092995  sravz/training:v1

docker attach

apt-add-repository ppa://ansible/ansible
apt-get update
apt-get install -y ansible

ansible localhost -m ping

cd /training/Ansible
ansible-playbook -v playbooks/sravz-node.yml
cd /training/notebooks
pip3 install pipenv

cd /training/Ansible
apt-get install systemctl sudo
sudo apt-get install systemd
ansible-playbook -v playbooks/mongodb.yml
```