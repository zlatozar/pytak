#!/bin/bash

# YUM install stuff

# Install development tools and some misc. necessary packages
yum -y groupinstall "Development tools"
yum -y install zlib-devel
yum -y install bzip2-devel openssl-devel ncurses-devel
yum -y install mysql-devel
yum -y install libxml2-devel libxslt-devel  # req'd by python package 'lxml'
yum -y install unixODBC-devel               # req'd by python package 'pyodbc'
yum -y install sqlite sqlite-devel
yum -y install python-setuptools

# Install Python 2.7.4 (do NOT remove 2.6, by the way)
wget --no-check-certificate http://www.python.org/ftp/python/2.7.4/Python-2.7.4.tar.bz2

tar xf Python-2.7.4.tar.bz2

cd Python-2.7.4
./configure --prefix=/usr/local
make && make altinstall
cd ..

# CentOS extention
rpm -Uvh epel-release-6*.rpm

# Clean up
rm -rf Python-2.7.4*

echo "Fix /etc/yum.repos.d/epel.repo and update repos"
sed -i 's/https/http/g' /etc/yum.repos.d/epel.repo

# Install pip and virtualenv stuff
echo | yum update --skip-broken
yum -y install python-pip python-virtualenv python-virtualenvwrapper

echo 'export WORKON_HOME=~/Envs' >> $HOME/.bashrc
source $HOME/.bashrc

mkdir -p ~/Envs
echo '. /usr/bin/virtualenvwrapper.sh' >> $HOME/.bashrc
source $HOME/.bashrc

echo "Done!"
echo "Now you can do in PyTak directory as regular user:"
echo
echo "mkvirtualenv pytak --python=python2.7"
echo "workon pytak"
echo "pip install -r requirements-dev.txt"
