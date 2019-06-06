# Filename: forms.py
#
# Author: John Reeves
# Contributor: Derek King
#
# Completion Date: 4/10/16
#
# Description: This file defines the search form found in index.html. By declaring the form as a class
# consisting of the fields shown below, Django can easily access it and enforce the contraints we place 
# on it. 
#

from django import forms # allows us to create a form
from django.core.validators import RegexValidator # allows us to use regular expressions to limit user input

# create a class called SearchForm to hold our index.html form
class SearchForm(forms.Form):
	
	# all of the following fields follow the same format as this first example. The only difference lie in their label names, placeholder text, and max lengths. I have explained the first field and all others follow the same exact pattern.
	# i have also grouped them based on how they appear within the index.html page
	# assigns the client_group_number to a character field with the label group number, a max length of 5, alowwing it to be blank, making sure its only a 0-9 digit, and adding 'Group Number' as placeholder text
    client_group_number=forms.CharField(label='Group Number', max_length=5, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Group Number'}))
	# assigns the client_location_number....
    client_location_number=forms.CharField(label='Location Number', max_length=5, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Location Number'}))
    
	# assigns the ppo_ppo_number...
    ppo_ppo_number=forms.CharField(label='PPO Number', max_length=5, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'PPO Number'}))
    
	# assigns the invoice_group_number...
    invoice_group_number=forms.CharField(label='Invoice Group Number', max_length=5, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Group Number'}))
	# assigns the client_location_number...
    invoice_location_number=forms.CharField(label='Invoice Location Number', max_length=5, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Location Number'}))
    # assigns the client_ppo_number...
    invoice_ppo_number=forms.CharField(label='Invoice PPO Number', max_length=5, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'PPO Number'}))
    
	# assigns the claim_prefix...
    claim_prefix=forms.CharField(label='Prefix', max_length=4, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Prefix Number'}))
	# assigns the claim_number...
    claim_number=forms.CharField(label='Number', max_length=9, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Claim Number'}))
	# assigns the claim_suffix...
    claim_suffix=forms.CharField(label='Suffix', max_length=4, required=False, validators=[RegexValidator(regex='^[*0-9]*$', message='', code='invalid_input')], widget=forms.TextInput(attrs={'placeholder': 'Suffix Number'}))
    
	# assigns the total_invoice_id...
    total_invoice_id=forms.CharField(label='Invoice ID', max_length=10, validators=[RegexValidator(regex='^[0-9]*$', message='', code='invalid_input')], required=False, widget=forms.TextInput(attrs={'placeholder': 'Invoice ID'}))
	