# Reset the Django superuser password

source: https://djangowaves.com/tips-tricks/how-to-reset-the-django-admin-password/

If you forgot your Django admin/superuser password, there are multiple ways to reset it. We will go over them. If you lost your username, then we will find that back again as well.



## Find your username

If you already have your username, then [skip to this part](#reset-your-django-admin-password). On your server or localhost, start Django shell:

```shell
python manage.py shell
```

Up next, we can find out what usernames are used for admins with this:

```python
from django.contrib.auth import get_user_model
list(get_user_model().objects.filter(is_superuser=True).values_list('username', flat=True))
```

If you have changed the `username` field, then please change it above as well to whatever default username field is. You will now get a result similar to this:

```
['admin@djangowaves.com']
```

If you get multiple results, you have multiple superusers. Pick the one that you want to change the password from.



## Reset your Django admin password

Open up Django shell if you haven't yet (`python manage.py shell`). Then copy/paste this:

```python
from django.contrib.auth import get_user_model
def reset_password(u, password):
    try:
        user = get_user_model().objects.get(username=u)
    except:
        return "User could not be found"
    user.set_password(password)
    user.save()
    return "Password has been changed successfully"
```

That's the function we will use to change the password of a user. Up next, you can simply do:

```python
reset_password(username, password)
# example: reset_password('admin', 'averysecretpassword')
```

Obviously, change the username with the username of your superuser account and change the password with something you want to use as a password.

Please note that if you do not have the `username` field as the username, then change it in the function above. Specifically, change this:

```
user = get_user_model().objects.get(username=u)
```

To this (if you use email as the username):

```
user = get_user_model().objects.get(email=u)
```



## The End
