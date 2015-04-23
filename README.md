######This is Udacity Full Stack Nano Degree project 5. It is a web app for displaying items, deploy on linux server with Apache2 and mod-wsgi. It bases on Flask and Bootstrap. 

---------------

**How to use?**

1. Update and install pip.

		sudo apt-get update
			
		sudo apt-get install python-pip

1. Install and activate virtualenv.

		sudo pip install virtualenv
	
		source catalog/bin/activate
	
1. Change the SSH Port:

		sudo nano /etc/ssh/sshd_config

	Then, chang 'port 22' to 'port 2200'

1. Install postgreSQL:

		sudo apt-get install postgresql postgresql-contrib 
		sudo apt-get build-dep python-psycopg2

1. Create new user and database in postgreSQL, and configurate catalog.py with username, password and database:

		engine = create_engine('postgres://<username>:<password>@localhost/<database>')

1. Set available port with iptables:

		iptables -A INPUT -p tcp -m tcp --dport 2200 -j ACCEPT
	
		iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
	
		iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
	
		iptables -A INPUT -p tcp -m tcp --dport 123 -j ACCEPT

		iptables -A INPUT -P tcp -m tcp --dport 5432 -j ACCEPT
	
		iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
	
		iptables -P OUTPUT ACCEPT
	
		iptables -P INPUT DROP


	Then save the configuration:

		iptables-save | sudo tee /etc/sysconfig/iptables
		service iptables restart
 
1. Protect SSH with fail2ban:

		sudo apt-get install fail2ban

	Edit the configure file as need:

		sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
	
		sudo nano /etc/fail2ban/jail.local

	Restart to activate the change:

		sudo service fail2ban restart

1. Install and configure Apache2:

		sudo apt-get install apache2

	Configure Apache2:

		sudo nano /etc/apache2/sites-available/catalog.conf

	Change the configuration as below:

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
	        ErrorLog ${APACHE_LOG_DIR}/error.log
	        LogLevel warn
	        CustomLog ${APACHE_LOG_DIR}/access.log combined
		</VirtualHost>


	Activate the host:

		sudo a2ensite catalog
	
		sudo service apache2 restart

1. Install and execute mod-wsgi:

		sudo apt-get install libapache2-mod-wsgi python-dev
		sudo a2enmod wsgi

1. Setup automatic update with cron:

		cd /PathToCatalog
	
		crontab crontab.txt
