Councilmatic!
=============
Philly City Council Legislative Subscription Service.

Contact Us
----------
- Join the mailing list at https://groups.google.com/group/councilmatic/
- Find us on irc.freenode.net in the #councilmatic room

Getting Started
---------------
First check out the project code.

    $ git clone git://github.com/codeforamerica/councilmatic.git

To work on your own instance of Councilmatic, you should first get Python
installed. Follow the instructions for doing so on your platform.

In addition, we recommend setting up a virtual environment for working with any
project, so that you can manage your project-specific dependencies.

    $ virtualenv councilmatic_env --no-site-packages
    $ source councilmatic_env/bin/activate
    
Next, install the requirements for Councilmatic (we recommend working in a
virtual environment, but it's not strictly necessary).

    $ pip install -r requirements.txt

Non-Python requirements include:

* pdftotext and pdftohtml (use ``apt-get install poppler-utils`` on Ubuntu)

Set up the project database and populate it with city council data (when the
syncdb command prompts you to create an administrative user, go ahead and do
so). There is a lot of data to be loaded, so downloading it all may take a
while.

    $ cd councilmatic
    $ python manage.py syncdb # Create admin account when prompted.
    $ python manage.py migrate
    $ python manage.py loadlegfiles
    $ python manage.py rebuild_index # For searches. Say yes when prompted.

Finally, to run the server:

    $ python manage.py runserver

Now, check that everything is working by browsing to http://localhost:8000/. Now
browse to http://localhost:8000/admin and enter the admin username and password
you supplied and you should have access to all of the legislative files!


Copyright
---------
Copyright (c) 2010 Code for America Laboratories
See [LICENSE](https://github.com/cfalabs/open311/blob/master/LICENSE.mkd) for details.

[![Code for America Tracker](http://stats.codeforamerica.org/codeforamerica/philly_legislative.png)](http://stats.codeforamerica.org/projects/philly_legislative)
