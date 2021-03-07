pip3 install xlsxwriter
pip3 install pyyaml

# install pattern library
sudo chown -R $(whoami) /usr/local/var/log
chmod u+w /usr/local/var/log
brew install mysql-connector-c
echo 'export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.bash_profile
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
pip3 install pattern
