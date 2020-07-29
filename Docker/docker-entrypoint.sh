# Provisioner runs as sudo so no sudo required
# Install ansible
apt-add-repository ppa://ansible/ansible
apt-get update
apt-get install -y ansible

# Set hostname
echo "# Required for mongodb sharding to work" >> /etc/hosts
echo "127.0.0.1 ubuntu" >> /etc/hosts
echo "192.168.56.4 ubuntu.sravz.com" >> /etc/hosts
# Create default ssh-Keys
mkdir -p ~/.ssh
rm ~/.ssh/id_rsa*
cd ~/.ssh
ssh-keygen -f id_rsa -t rsa -N ''
cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
chmod 400 ~/.ssh/authorized_keys
