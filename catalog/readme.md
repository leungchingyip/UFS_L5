######This is Udacity Full Stack Nano Degree project 3.It is a web app for displaying items. It base on Flask and Bootstrap.

----------------

**What's included?**  


	.
	|-- catalog.py
	|-- FacebookSignUp.py
	|-- file.db
	|-- login.py
	|-- model.py
	|-- pip_setup.txt
	|-- readme.md
	|-- static
	|   |-- dist
	|   |   |-- css
	|   |   |   |-- blog.css
	|   |   |   |-- bootstrap.css
	|   |   |   |-- bootstrap.css.map
	|   |   |   |-- bootstrap.min.css
	|   |   |   |-- bootstrap-theme.css
	|   |   |   |-- bootstrap-theme.css.map
	|   |   |   `-- bootstrap-theme.min.css
	|   |   |-- fonts
	|   |   |   |-- glyphicons-halflings-regular.eot
	|   |   |   |-- glyphicons-halflings-regular.svg
	|   |   |   |-- glyphicons-halflings-regular.ttf
	|   |   |    -- glyphicons-halflings-regular.woff
	|   |    -- js
	|   |       |-- bootstrap.js
	|   |       |-- bootstrap.min.js
	|   |        -- npm.js
	|    -- image
	|-- templates
	|   |-- add.html
	|   |-- base.html
	|   |-- csrf.html
	|   |-- delete.html
	|   |-- edit.html
	|   |-- home.html
	|   |-- item.html
	|    -- newcategory.html
	|-- upload_image.py
	 -- Vagrantfile  



**How to use?**

If do not use vagrant, please skip steps 1 and 2.

1. Install [VagrantBox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads)

2. At the catalog.py exists directory: `vagrant up`, then: `vagrant ssh`

3. Install the necessary module:  <code>pip install -r pip_setup.txt<code>

3. Set your ‘client_id’ and ‘client_secret' in FacebookSignUp.py.

4. Set your configuration of your database in create_engine line. Include which kind of database, database's user name, and adress.

5. Run the app on localhost: `python catalog.py`


