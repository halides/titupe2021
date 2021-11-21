# titupe2021

## 0. Environment

This project is a copy of part3-18.csrf-exercise, with a bunch of additional (bad) features just to create a bunch of problems in the codebase. I was planning to do both injection and XSS but in the 2021-OWASP they're under the same "topic" so I only did the injection part. However, I figured I could use these CSRF exempts as an example of securit misconfigurationy.

If you have the environment set up for the Cyber Security Base 2021, you should be able to just clone this repo and `python3 manage.py runserver` in the root directory. Details for setting up the environment in https://cybersecuritybase.mooc.fi/installation-guide

You probably need to run migrations before your first run: `python3 manage.py migrate`, but the runserver should complain about it if you do need to run it.

## 1. SQL injection (A03:2021-Injection)

https://github.com/halides/titupe2021/blob/a47b63d38dee6cae4651faaa6c28945c4debdc73/src/pages/views.py#L35

If you send a message with f.ex. the following payload:

'; delete from pages_account where user_id=5;--

you'll bypass many layers of injection protection and will delete the user with user_id of 5 from pages_account. To mitigate this you have many options:
1. As this is an SQLite database, just using .execute() instead of .executescript() will not run multiple statements from one query. This is however not a proper way to mitigate, as other SQL-engines could have different semantics for .execute().
2. Instead of using the ("string '%s'" % message) syntax, you could use ("string '%s'", [message]) which seems to make sure the message is escaped correctly and no injection should happen.
3. Instead of writing raw SQL like I do here, use the ORM-engine of Django, where you could just say something much simpler like "to.account.message = message", like is being done in the transfewVies method above.

## 2. Handling and storing secret data improperly (A02:2021 – Cryptographic Failures)

We promise to the user that we'll handle secret data properly. This data could be your credit-card number, your  We break this promise at least in two places, first in the frontend:

https://github.com/halides/titupe2021/blob/7cd15bb828382de098db3c5415a6165e31731539/src/pages/templates/pages/index.html#L62

and then in the backend:

https://github.com/halides/titupe2021/blob/7cd15bb828382de098db3c5415a6165e31731539/src/pages/views.py#L49

The front-end is not a secured site (HTTPS), thus this secret data is moved through a network unencrypted, and thus this data could be stolen by any listener between the client and server. In the back-end the data is stored in plaintext, which is not a good idea for sensitive data. Anyone having direct read-access to the database could steal this information, even though the front-end and the back-end might be secure.

To fix this, use HTTPS (or roll your own crypto (no don't roll your own crypto I'm just kidding)) for the front-end connection and crypt sensitive data that is going to be stored persistently. 

## 3. Logging secret data (A09:2021-Security Logging and Monitoring Failures)

https://github.com/halides/titupe2021/blob/7cd15bb828382de098db3c5415a6165e31731539/src/pages/views.py#L51

In addition to not handling the secret data properly, here we also log it improperly. Even though we could handle the front-end properly (use a secure connection over the network) and crypt the data when we store it to the database, logging like this can still expose sensitive data in places where it should not be exposed. Logging like this could be used for example in debugging, and when doing work like that it is important to remove logging like this.

This is something that I think there are no automatic tools that really can handle this, as I think we don't have a systemic way of tagging data as "sensitive" in a way that would automatically warn the developer that you're doing something stupid (like logging) with a piece of data that you should be super careful with. This is a similar (or even the same) problem that was discussed in the Threat Analysis portion regards "Data Lifetime is a System Problem". I discuss a mitigation for this in 5., below.

## 4. Liberal use of csrf-exempt (A05:2021 – Security Misconfiguration)

https://github.com/halides/titupe2021/blob/7cd15bb828382de098db3c5415a6165e31731539/src/pages/views.py#L14

I feel like this is a pretty contrived example, but I actually had a hard time in doing the part3.18-csrf-exercise as I didn't notice the @csrf_exempt decorator at first and had problems getting the exercise done properly for a while :-)

Django has automatic middleware for protecting again CSRF, and you can disable with the mentioned exempt-decorator. The exemption could once again be used for example when debugging the system ("this isn't working, is it because of csrf?" -> disable), and it might be easy to forget to turn it back on.

To fix this problem, just remove all the @csrf_exempts and add {% csrf_token %} to the forms in the index-template like so:

https://github.com/halides/titupe2021/blob/f1a45f1b0562ddde18999532da614c0546960c13/src/pages/templates/pages/index.html#L22

## 5. Not using common industry standard best practices (A04:2021 – Insecure Design)

This is not a problem I can give a line-reference to, as it is a systematic issue which is not handled properly in this example.

The two previous examples mentioned debugging and forgetting to turn security features back on. Any kind of a complex system that is connected to the public Internet is going to have some security flaws, and it is going to need updates and debugging which can cause additional security flaws if not handled properly. Another issue that can give rise to security issues is new functionality. 

The major contemporary mitigation in my opinion for these kinds of problems is a proper CI/CD-pipeline with a robust test suite. As discussed in 3., there seems to be no current systemic method to mark some data as "sensitive" and get warnings or errors when handling that data incorrectly. One way of getting this kind of functionality is through analysis of the codebase with automated tools. Data could be earmarked as something that we want to keep a keen eye on and thus be more confident that this data is handled properly. Another simple example for this kind of testing would be simply the grep the codebase for any kind of @csrf_exempts and give out errors and warnings if any are found.

This codebase has no testing whatsoever, and that fact is the most worrying for me. Any kind of "properly done" codebase can quickly slip into an "improperly done" codebase with just one update. Testing and CI/CD-pipelines do help if done properly (with a definition of "proper" that fits the budget of the project), but these are additional work and need intelligent, continuous reviews by experienced, multi-diciplinary developers.

To fix this problem, do proper testing and plausible delivery pipelines. If delivery is not automated, human error might happen at any update.
