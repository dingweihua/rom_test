# -*- coding: utf-8 -*-

import os
import datetime

import redis
import rom

# All models to be handled by rom must derived from rom.Model
class User(rom.Model):
    email = rom.String(required=True, unique=True, suffix=True, keygen=rom.SIMPLE)
    salt = rom.String()
    hash = rom.String()
    created_at = rom.DateTime()

    def gen_hash(self, password, salt=None):
        from hashlib import sha256

        PASSES = 32768
        salt = salt or os.urandom(16)
        comp = salt + password
        out = sha256(comp).digest()
        for i in xrange(PASSES-1):
            out = sha256(out + comp).digest()
        return salt, out

if __name__ == '__main__':
    # connect redis
    rom.util.set_connection_settings(host='localhost', port=6379, db=7)
    # save user
    user = User(email='user@gmail.com', created_at=datetime.datetime.now())
    password = 'sugarlady'
    user.salt, user.hash = user.gen_hash(password)
    user.save()
    # query user
    user = User.get_by(email='user@gmail.com')
    if user:
        print user.created_at
    at_gmail = User.query.endswith(email='@gmail.com').all()
    print at_gmail
    # delete user
    user.delete()
    user = User.get_by(email='user@gmail.com')
    print user
