######This is Udacity Full Stack Nano Degree project 5. It is a web app for displaying items, deploy on linux server by Apache2 and wsgi. It bases on Flask and Bootstrap. server

---------------

**How to use?**

1. `sudo apt-get update`

1. `sudo apt-get install python-pip`

1. install and activate virtualenv:

`sudo pip install virtualenv`

`source catalog/bin/activate`

1. install and execute mod-wsgi

<code>
sudo apt-get install libapache2-mod-wsgi python-dev

sudo a2enmod wsgi
</code>

1. change the SSH Port:

<code> nano /etc/ssh/sshd_config</code>

chang `port 22` to `port 2200`

1. install postgreSQL:

<code> sudo apt-get install postgresql postgresql-contrib </code>

1. create new user and database in postgreSQL, and configurate catalog.py with username, password and database:

<code> engine = create_engine('postgres://<username>:<password>@localhost/<database>')

1. 

<code>
iptables -A INPUT -p tcp -m tcp --dport 2200 -j ACCEPT

iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT

iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT

iptables -A INPUT -p tcp -m tcp --dport 123 -j ACCEPT

iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -P OUTPUT ACCEPT

iptables -P INPUT DROP
</code>

then save the configuration:

<code>
iptables-svae | sudo tee /etc/sysconfig/iptables
service iptables restart
</code> 

1. protect SSH with fail2ban:

`sudo apt-get install fail2ban`

Edit the configure file:

<code>
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

sudo nano /etc/fail2ban/jail.local
</code>

1. Install and configure Apache2:

`sudo apt-get install apache2`

Configure Apache2:

`sudo nano /etc/apache2/sites-available/catalog`

Change the configuration as below:

<code>
	<VirtualHost *:80>
                ServerName <your server ip or domain name>

                WSGIScriptAlias / /<path to catalog>/catalog/catalog.wsgi
                WSGIDaemonProcess catalog user=<username> threads=5
                <Directory /catalog/catalog/>
                        WSGIProcessGroup catalog
                        WSGIApplicationGroup %{GLOBAL}
                        WSGIScriptReloading On
                        Order allow,deny
                        Allow from all
                        Require all granted

                </Directory>
                Alias /static /<path to catalog>/catalog/static
                <Directory /catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Allow from all
                        Require all granted

                </Directory>
                Alias /static /<path to catalog>/catalog/static
                <Directory /catalog/catalog/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
	</VirtualHost>
</code>

Activate hte host:

`sudo a2ensite catalog`

`sudo service apache2 restart'

1. Setup automatic update with cron:

<code>
cd /PathToCatalog

crontab crontab.txt
</code>



