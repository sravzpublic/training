# Provisioner runs as sudo so no sudo required
# Install ansible
apt-add-repository ppa://ansible/ansible
apt-get update
apt-get install -y ansible

# Set hostname
echo "# Required for mongodb sharding to work" >> /etc/hosts
echo "127.0.0.1 vagrant" >> /etc/hosts
# Create default ssh-Keys
rm /home/vagrant/.ssh/id_rsa*
cd /home/vagrant/.ssh
ssh-keygen -f id_rsa -t rsa -N ''
cat /home/vagrant/.ssh/id_rsa.pub >> /home/vagrant/.ssh/authorized_keys
chown vagrant.vagrant /home/vagrant/.ssh/*
