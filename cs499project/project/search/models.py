# models.py
# Authors: John Reeves
# Completion Date: 4/10/16
# Description: 
#	This file describes the fields listed in the PostgreSQL database such that the other Django files can interface with the database.
#	It provides functionality for error prevention/ error checking by defining the data types. 


# This code imports neccessary functions and was written automatically upon project creation.

from __future__ import unicode_literals

from django.db import models

# Create your models here.


# Search example()
#
# Preconditions: This code is an example of the following functions and is not used.
# Postconditions: This code is an example of the following functions and is not used.
#
# Description: This code is an example of the following functions and is not used.

#class Search(models.Model):
    #title = models.CharField(max_length=120)
    #content = models.TextField()
    #updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    #timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    #def __unicode__(self):
        #return self.title



# client()
#
# Preconditions: NONE
# Postconditions: The database fields for the table "client" are defined.
#
# Description: The thirteen fields of the table "client are defined by thier datatypes. Django must understand many of these fields as character fields so that the user can 
#	input text for updates. Error type-checking may also occur elsewhere.

class client(models.Model):
    grpno = models.CharField(max_length=5, primary_key=True)			# Character field grpno of max length five characters is a primary key.
    groupname = models.CharField(max_length=40)							# Character field groupname of max length fourty characters.
    locno = models.CharField(max_length=5, primary_key=True)			# Character field locno of max length five characters is a primary key.
    locname = models.CharField(max_length=40)							# Character field locname of max length fourty characters.
    addr_1 = models.CharField(max_length=40)							# Character field address_1 of max length fourty characters. 
    addr_2 = models.CharField(max_length=40)							# Character field address_2 of max length fourty characters.
    city = models.CharField(max_length=40)								# Character field city of max length fourty characters.
    state = models.CharField(max_length=2)								# Character field state of max length two characters.
    zip_code = models.CharField(max_length=10)							# Character field zip_code of max length ten characters.
    contact = models.CharField(max_length=40)							# Character field contact of max length fourty characters.
    phone = models.CharField(max_length=20)								# Character field phone of max length twenty characters.
    email = models.CharField(max_length=40)								# Character field email of max length fourty characters.
    claim_charge = models.CharField(max_length=14)						# Character field claim_charge of max length fourteen characters.

    class Meta:															# Descriptor for client table.
        db_table = 'client'

    def __unicode__(self):												# Define text as unicode.
        return unicode(self.client)



# ppo()
#
# Preconditions: NONE
# Postconditions: The database fields for the table ppo are defined.
#
# Description:  The five fields of the table "ppo" are defined by thier datatypes. Django must understand many of these fields as character fields so that the user can 
#	input text for updates. Error type-checking may also occur elsewhere.

class ppo(models.Model):
    ppono = models.CharField(max_length=5, primary_key=True)			# Character field ppono of max length five characters is a primary key.
    active = models.BooleanField()										# Boolean field active.
    ppo_name = models.CharField(max_length=40)							# Character field ppo_name of max length fourty characters.
    ppo_method = models.CharField(max_length=1)							# Character field ppo_method of max length one character.
    ppo_cost = models.CharField(max_length=14)							# Character field ppo_cost of max length fourteen characters.
    
    class Meta:															# Descriptor for ppo table.
        db_table = 'ppo'
    
    def __unicode__(self):												# Define text as unicode.
        return unicode(self.ppono)



# client()
#
# Preconditions: NONE
# Postconditions: The database fields for the table invioce are defined.
#
# Description:  The five fields of the table "invoice" are defined by thier datatypes. Django must understand many of these fields as character fields so that the user can 
#	input text for updates. Error type-checking may also occur elsewhere.

class invoice(models.Model):
    grpno = models.CharField(max_length=5, primary_key=True)			# Character field grpno of max length five characters is a primary key.
    locno = models.CharField(max_length=5, primary_key=True)			# Character field locno of max length five characters is a primary key.
    ppono = models.CharField(max_length=5, primary_key=True)			# Character field ppono of max length five characters is a primary key.
    ppo_method = models.CharField(max_length=1)							# Character field ppo_method of max length one character.
    ppo_charge = models.CharField(max_length=14)						# Character field ppo_charge of max length fourteen characters.

    class Meta:															# Descriptor for ppo table.
        db_table = 'invoice'
                             
    def __unicode__(self):												# Define text as unicode.
        return unicode(self.invoice)




# client()
#
# Preconditions: NONE
# Postconditions: The database fields for the table claim are defined.
#
# Description:  The twenty-one fields of the table "claim" are defined by thier datatypes. Django must understand many, but not all of these fields as character fields so that the user can 
#	input text for updates. Error type-checking may also occur elsewhere.

class claim(models.Model):
    clmpre = models.CharField(max_length=4, primary_key=True)			# Character field clmpre of max length four characters is a primary key.
    clmno = models.CharField(max_length=9, primary_key=True)			# Character field clmmno of max length nine characters is a primary key.
    clmsuf = models.CharField(max_length=4, primary_key=True)			# Character field clmsuf of max length four characters is a primary key.
    grpno = models.CharField(max_length=5)								# Character field grpno of max length five characters.
    locno = models.CharField(max_length=5)								# Character field locno of max length five characters.
    totchg = models.CharField(max_length=14)							# Character field totchg of max length fourteen characters.
    discamt = models.CharField(max_length=14)							# Character field discamt of max length fourteen characters.
    prvpmt = models.CharField(max_length=14)							# Character field prvpmt of max length fourteen characters.
    lockno = models.CharField(max_length=10)							# Character field lockno of max length ten characters.
    fromdt = models.DateField()											# Date field fromdt.
    thrudt = models.DateField()											# Date field thrudt.
    pddt = models.DateField()											# Date field pddt.
    locname = models.CharField(max_length=40)							# Character field locname of max length fourty characters.
    ppono = models.CharField(max_length=5)								# Character field ppono of max length five characters.
    invoice_id = models.CharField(max_length=10)						# Character field invoice_id of max length ten characters.
    invoice_date = models.DateField()									# Date field invoice_date.
    claim_charge = models.CharField(max_length=14)						# Character field claim_charge of max length fourteen characters.
    ppo_charge = models.CharField(max_length=14)						# Character field ppo_charge of max length fourteen characters.
    ppo_pddt = models.DateField()										# Date field ppo_pddt.
    ppo_invoice = models.CharField(max_length=20)						# Character field ppo_invoice of max length twenty characters.
    ppo_pd_amt = models.CharField(max_length=14)						# Character field ppo_pd_amt of max length fourteen characters.

    class Meta:															# Descriptor for ppo table.
        db_table = 'claim'
                             
    def __unicode__(self):												# Define text as unicode.
        return unicode(self.claim)