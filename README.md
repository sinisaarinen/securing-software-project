# PROJECT REPORT

Purpose of the project: to create a web application containing at least five out of the 10 security flaws from the OWASP TOP 10 list.

## Installation instructions:

You are expected to have Python3 with pip installed to use the application. If you do not yet have these, follow instructions to install on this page: https://cybersecuritybase.mooc.fi/installation-guide

Dependencies required: in addition, some dependencies need to be installed. These dependencies are django, the widget tweaks django library and sqlite3. Django and the widget tweaks library can be installed using the following command:
python3 -m pip install django django-widget-tweaks

Sqlite3 should be already included in the standard library.


## Security flaws implemented

### FLAW 1: Broken Access Control. 

Broken access control has to do with the ways users can act outside of their intended permissions. It means that restrictions on what authenticated users are allowed to do are not implemented properly. It can open a way for attackers to access unauthorized functionality/data (for example access or modify others’ accounts or data).

There are multiple open endpoints in the project that should require authorization and therefore cause broken access control. For example, in views.py file there is a method (postMessage(request)) that allows users to post messages without authorization.

How to fix it? Restrictions need to be implemented to restrict users from accessing unintended accounts or data. This can be fixed by adding login required annotations to methods that only logged in users are allowed to use and by adding ownership checks that make sure the sensitive information belongs to the user who is trying to use the method. If not, the user should be restricted from using the method.

### FLAW 2: SQL injection.

SQL injection belongs to one of the most common hacking techniques and is a code injection technique (other code injection techniques include NoSQL, OS and LDAP injection, for example). SQL injection works as follows: malicious code is placed in SQL statements, via web page input, and is then sent to an interpreter. This can lead to the interpreter executing unintended commands or accessing data without proper authorization. SQL injection might lead to the destruction of the database.

There is possibility for SQL injection in the project. The flaw can be found in the file views.py in method findById(request). The parametres give to the endpoint findById are unsafely inserted to the SQL query. This allows the user to for example fetch the admin password.

How to fix it? There are many ways to fix this problem. I would suggest either 1) using Django’s own ORM instead of executing SQL statements directly or 2) sanitizing the input.

### FLAW 3: Insufficient Logging & Monitoring. 

Insufficient logging and monitoring can lead to attacks that system maintainers are not able to quickly react to. Insufficient logging and monitoring can mean that auditable events (logins, failed logins, etc.) are not logged, warnings and errors are not logged, logs are only stored locally etc. All of this can offer attackers more time to attack systems, destroy data etc. without being noticed.

There is no persistent logging and monitoring in the application.

How to fix it? By implementing proper monitoring. There are a few different ways to do this, including the use of middleware (for example logging middleware) and using LogEntry in Django Admin to monitor user actions.

### FLAW 4: Cross-Site Scripting (XSS). 

Cross-Site Scripting (XSS) is a security flaw that is common in web applications. It allows users to execute scripts in other peoples’ browsers – there scripts may be used in a malicious way in order to hijack user sessions, deface web sites or redirect the users to undesired sites. These security flaws are especially dangerous in web applications dealing with sensitive data (personal data, social security numbers, identities), money transactions etc.

It is possible to send scripts with messages that are then executed by everyone seeing the message. There is a text field in the HTML file that allows the user to enter scripts. These scripts are also saved to the database (see method postMessage(request) in file views.py).

How to fix it? As Django protects from XSS flaws, for my project it would be enough the remove the part |safe from the index.html file. The |safe part prevents Django from escaping the message and therefore allows cross-site scripting.

### FLAW 5: Security Misconfiguration. 

Security misconfiguration is the most common one of the security flaws. It is normally caused by insecure default configurations, incomplete or ad hoc configurations, open cloud storage, misconfigured HTTP headers and verbose error messages containing sensitive information. It is important not only to make sure everything is correctly and securely configured, but also that all configurations are up to date.

The project contains two security misconfiguration problems. First of all, sessions last for 1000 hours. The other problem is that user passwords and usernames are logged to the console.

How to fix it? By removing the SESSION_COOKIE_AGE = 1000 * 60 part of the settings.py file returns the session time to the Django default time. The other problem can be fixed by removing the following lines from the views.py file:
print("username: " + request.POST.get('username'))
print("password: " + request.POST.get('password'))
