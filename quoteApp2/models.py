from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def registration_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        registerWithEmail = User.objects.filter(email= postData['email'])
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "Name should be at least 2 characters"
        if len(postData['email']) < 1:
            errors["emailBlank"] = "Email is required"
        if len(registerWithEmail) > 0:
            errors['emailTaken'] = "Email is taken already!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailPattern'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors["passwordLength"] = "Password must be at least 8 characters"
        if postData['confirmPassword'] != postData['password']:
            errors['passwordMatch'] = "Password and Confirm Password must match"
        print(errors)
        return errors

    def login_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+.[a-zA-Z]+$')
        loginWithEmail = User.objects.filter(email= postData['email'])
        print("printing usersWithEmail below:")
        print(loginWithEmail)
        print("printing a user")
        errors = {}
        if len(postData['email']) < 1:
            errors["emailBlank"] = "Email is required"
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailPattern'] = ("Invalid email address!")
        if len(postData['password']) < 8:
            errors["passwordLength"] = "Password must be at least 8 characters"
        if len(loginWithEmail) < 1:
            errors['EmailNotFound'] = "Email not found!"
        else:
            user = loginWithEmail[0]
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['passwordInvalid'] = "The password is incorrect"
        print(errors)
        return errors
    def quote_validator(self,postData):
        errors = {}
        if len(postData['quoter']) < 2:
            errors['quoterLength'] = "Quoted by must be at least 2 characters"
        if len(postData['message']) < 10:
            errors['messageLength'] = "Message must be at least 10 characters"
        print(errors)
        return errors
    def edit_quote_validator(self,postData):
        errors = {}
        if len(postData['quoter']) < 2:
            errors['quoterLength'] = "Quoted by must be at least 2 characters"
        if len(postData['message']) < 10:
            errors['messageLength'] = "Message must be at least 10 characters"
        print(errors)
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    poster = models.ForeignKey(User, related_name="quotes_created", on_delete=models.CASCADE, null="None")
    quoter = models.CharField(max_length=255)
    message = models.TextField()
    favorite = models.ManyToManyField(User, related_name="favorite_quote")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
