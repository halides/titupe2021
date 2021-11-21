# titupe2021

## 0. Environment

This project is a copy of part3-18.csrf-exercise, with a bunch of additional (bad) features just to create a bunch of problems in the codebase. I was planning to do both injection and XSS but in the 2021-OWASP they're under the same "topic" so I only did the injection part. Which makes using the CSRF-exercise a bit moot.

If you have the environment set up for the Cyber Security Base 2021, you should be able to just clone this repo and `python3 manage.py runserver` in the root directory. Details for setting up the environment in https://cybersecuritybase.mooc.fi/installation-guide

You probably need to run migrations before your first run: `python3 manage.py migrate`, but the runserver should complain about it too.

## 1. SQL injection (A03:2021-Injection)

https://github.com/halides/titupe2021/blob/a47b63d38dee6cae4651faaa6c28945c4debdc73/src/pages/views.py#L35

If you send a message with f.ex. the following payload:

'; delete from pages_account where user_id=5;--

you'll bypass many layers of injection protection and will delete the user with user_id of 5 from pages_account. To mitigate this you have many options:
1. As this is an SQLite database, just using .execute() instead of .executescript() will not run multiple statements from one query. This is however not a proper way to mitigate, as other SQL-engines could have different semantics for .execute().
2. Instead of using the ("string '%s'" % message) syntax, you could use ("string '%s'", [message]) which seems to make sure the message is escaped correctly and no injection should happen.
3. Instead of writing raw SQL like I do here, use the ORM-engine of Django, where you could just say something much simpler like "to.account.message = message", like is being done in the transfewVies method above.
