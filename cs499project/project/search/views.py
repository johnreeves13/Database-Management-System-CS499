#Filename: views.py
#Author: John Reeves
#Contributors: Derek King, Robert Watts
#Completion Date: 4/10/16
#Description: This file is the heart and soul of the program. Everything comes and goes through this file. This file runs based on POST and GET requests and does search and update queries, error checking, table/database calculations and going to certain html pages.

from django.shortcuts import render
from search.models import client, ppo, invoice, claim
from django.db import connection
from .forms import SearchForm
from datetime import *
import datetime
import json

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

#Commented out because it is an example
#def search_home(request):
    #    if request.user.is_authenticated():
    #    context = {
    #        "title": "Page"
    #}
    #else:
    #    context = {
    #        "title": "Wrong page"
    #}
    #return render(request, "index.html", {})#context)

#Name: query()
#Preconditions: A string containing a query statement to be executed.
#PostConditions: A list of lists containing the information for the database.
#Description: This function executes a query statement in the database and returns a nested list with all data from the database.
def query(query_string):
    with connection.cursor() as c:
        c.execute(query_string)
        row_list = c.fetchall()
    return row_list

#Name: update_database()
#Preconditions: A string containing a query statement to be executed.
#PostConditions: None
#Description: This function executes an UPDATE query statement which will update the basebase.
def update_database(query_string):
    with connection.cursor() as c:
        c.execute(query_string)

#Name: does_search_exist()
#Preconditions: A list of lists of the table, which table, data_point1(actual data from user input or None), data_point1_exist(0 for does not exist or 1 for does exist), data_point2(actual data from user input or None), data_point2_exist(0 for does not exist or 1 for does exist), data_point3(actual data from user input or None), data_point3_exist(0 for does not exist or 1 for does exist).
#PostConditions: Returns result which can be either 0 or 1.
#Description: This function checks to see if what the user inputted was in the database or not.
def does_search_exist(query_list, table, data_point1, data_point1_exist, data_point2, data_point2_exist, data_point3, data_point3_exist):
    result = 0
    for i in range(len(query_list)):
        #If table is 1, then we are checking a Client search
        if table == 1:
            #Checks if both Group Number and Location Number have inputs
            if data_point1_exist == 1 and data_point2_exist == 1:
                #Checks if the inputs matches up with what is in the database
                if str(query_list[i][0]) == str(data_point1) and str(query_list[i][2]) == str(data_point2):
                    #If true then result gets changed to 1
                    result = 1
            #Checks if Group Number has an input
            elif data_point1_exist == 1:
                #Checks if the input matches up with what is in the database
                if str(query_list[i][0]) == str(data_point1):
                    #If true then result gets changed to 1
                    result = 1
            #Checks if Location Number has an input
            elif data_point2_exist == 1:
                #Checks if the input matches up with what is in the database
                if str(query_list[i][2]) == str(data_point2):
                    #If true then result gets changed to 1
                    result = 1

        #If table is 2, then we are checking a PPO search
        elif table == 2:
            #Checks if the input matches up with what is in the database
            if str(query_list[i][0]) == str(data_point1):
                #If true then result gets changed to 1
                result = 1

        else:
            #We are checking either a Claims or Invoices search sinces both have three search boxes
            if data_point1_exist == 1 and data_point2_exist == 1 and data_point3_exist == 1:
                #Checks if the inputs matches up with what is in the database
                if str(query_list[i][0]) == str(data_point1) and str(query_list[i][1]) == str(data_point2) and str(query_list[i][2]) == str(data_point3):
                    #If true then result gets changed to 1
                    result = 1
            elif data_point2_exist == 1 and data_point3_exist == 1:
                #Checks if the inputs matches up with what is in the database
                if str(query_list[i][1]) == str(data_point2) and str(query_list[i][2]) == str(data_point3):
                    #If true then result gets changed to 1
                    result = 1
            elif data_point1_exist == 1 and data_point3_exist == 1:
                #Checks if the inputs matches up with what is in the database
                if str(query_list[i][0]) == str(data_point1) and str(query_list[i][2]) == str(data_point3):
                    #If true then result gets changed to 1
                    result = 1
            elif data_point1_exist == 1 and data_point2_exist == 1:
                #Checks if the inputs matches up with what is in the database
                if str(query_list[i][0]) == str(data_point1) and str(query_list[i][1]) == str(data_point2):
                    #If true then result gets changed to 1
                    result = 1
            elif data_point3_exist == 1:
                #Checks if the input matches up with what is in the database
                if str(query_list[i][2]) == str(data_point3):
                    #If true then result gets changed to 1
                    result = 1
            elif data_point2_exist == 1:
                #Checks if the input matches up with what is in the database
                if str(query_list[i][1]) == str(data_point2):
                    #If true then result gets changed to 1
                    result = 1
            elif data_point1_exist == 1:
                #Checks if the input matches up with what is in the database
                if str(query_list[i][0]) == str(data_point1):
                    #If true then result gets changed to 1
                    result = 1

    #Returns result to get_results()
    return result


#Name: is_only_one_being_searched()
#Preconditions: client_list, ppo_list, claims_list, invoices_list, total_list (where all the lists contain a list of 1's or None)
#PostConditions: Returns 0, 1 or 2
#Description: The purpose of this function is to see if the user is only trying to search in one table
def is_only_one_being_searched(client_list, ppo_list, claims_list, invoices_list, total_list):
    #find the length of each list
    client_list_length = len(client_list)
    ppo_list_length = len(ppo_list)
    invoices_list_length = len(invoices_list)
    claims_list_length = len(claims_list)
    total_list_length = len(total_list)
    
    #each variable finds the sum of the length of all but one list. Should be equal to 0 or a number higher than 0
    check1 = ppo_list_length + claims_list_length + invoices_list_length + total_list_length
    check2 = client_list_length + claims_list_length + invoices_list_length + total_list_length
    check3 = client_list_length + ppo_list_length + invoices_list_length + total_list_length
    check4 = client_list_length + ppo_list_length + claims_list_length + total_list_length
    check5 = client_list_length + ppo_list_length + claims_list_length + invoices_list_length
    
    #The first five checks see if only Client, PPO, Claims, Invoices or Find Total have an input(s) and if so only_one_searched = 0
    if int(client_list_length) > 0 and int(check1) == 0:
        only_one_searched = 0
    elif int(ppo_list_length) > 0 and int(check2) == 0:
        only_one_searched = 0
    elif int(claims_list_length) > 0 and int(check3) == 0:
        only_one_searched = 0
    elif int(invoices_list_length) > 0 and int(check4) == 0:
        only_one_searched = 0
    elif int(total_list_length) > 0 and int(check5) == 0:
        only_one_searched = 0
    #If none have any inputs then only_one_searched = 1
    elif int(client_list_length) == 0 and int(check1) == 0:
        only_one_searched = 2
    else:
        #More than one has been searched
        only_one_searched = 1

    return only_one_searched

#Name: duplicate_in_column()
#Preconditions: table, column, countThis, num_of_rows
#PostConditions: Returns 0 or 1 (false or true)
#Description: The purpose of this function is to see if there are duplicates in the column.
def duplicate_in_column(table, column, countThis, num_of_rows):
    duplicate = 0
    arr = []
    for i in table:
        if int(i[column]) == int(countThis):
            arr.append(int(i[column]))
    if arr.count(int(countThis)) == num_of_rows:
        duplicate = 1
    return duplicate

#Name: check_input_length_client()
#Preconditions: groupname, locname, addr_1, addr_2, city, state, zip_code, contact, phone, email, claim_charge
#PostConditions: Returns an error message
#Description: This function checks if the entries in each of the columns are under the maximum ammount of characters allows in the client table.
def check_input_length_client(groupname, locname, addr_1, addr_2, city, state, zip_code, contact, phone, email, claim_charge):
    status = ""
    if len(groupname) > 40:
        status = "Please enter a valid groupname (shorter than 40 characters)"
    elif len(locname) > 40:
        status = "Please enter a valid locname (shorter than 40 characters)"
    elif len(addr_1) > 40:
        status = "Please enter a valid addr_1 (shorter than 40 characters)"
    elif len(addr_2) > 40:
        status = "Please enter a valid addr_2 (shorter than 40 characters)"
    elif len(city) > 40:
        status = "Please enter a valid city (shorter than 40 characters)"
    elif len(state) > 2:
        status = "Please enter a valid state (shorter than 2 characters)"
    elif len(zip_code) > 10:
        status = "Please enter a valid zip_code (shorter than 10 characters)"
    elif len(contact) > 40:
        status = "Please enter a valid contact (shorter than 40 characters)"
    elif len(phone) > 20:
        status = "Please enter a valid phone number (shorter than 40 characters)"
    elif len(email) > 40:
        status = "Please enter a valid email (shorter than 40 characters)"
    elif len(claim_charge) > 15:
        status = "Please enter a valid claim_charge (shorter than 14 digits)"
    return status

#Name: check_input_length_ppo()
#Preconditions: active, ppo_name, ppo_method, ppo_cost
#PostConditions: Returns an error message
#Description: This function checks if the entries in each of the columns are under the maximum ammount of characters allows in the PPO table.
def check_input_length_ppo(active, ppo_name, ppo_method, ppo_cost):
    status = ""
    if active != "True":
        if active != "False":
            status = "Please enter a valid active (True or False)"
    elif len(ppo_name) > 40:
        status = "Please enter a valid ppo_name (shorter than 40 characters)"
    elif ppo_method != "":
        if ppo_method != "C":
            if ppo_method != "S":
                status = "Please enter a valid ppo_method (C or S)"
    elif len(ppo_cost) > 14:
        status = "Please enter a valid ppo_cost (shorter than 14 characters)"
    return status

#Name: check_input_length_invoices()
#Preconditions: invoice_method, ppo_charge
#PostConditions: Returns an error message
#Description: This function checks if the entries in each of the columns are under the maximum ammount of characters allows in the invoices table.
def check_input_length_invoices(invoice_method, ppo_charge):
    status = ""
    if invoice_method != "":
        if invoice_method != "C":
            if invoice_method != "S":
                status = "Please enter a valid ppo_method (C or S)"
    elif len(ppo_charge) > 14:
        status = "Please enter a valid ppo_charge (shorter than 14 characters)"
    return status


#Name: get_results()
#Preconditions: POST or GET request
#PostConditions: Returns a render to a html page
#Description: This is the "main" function of the program that tells the program what it needs to do and where it should go.
def get_results(request):
    #Status holds a string for an error message
    status = ""
    #If the Go Back button was clicked, go to the Search screen
    if request.POST.get('goBack'):
        form = SearchForm
        request.method = 'GET'
        return render(request, 'index.html', {'form': form, 'error': status})
    
    #If the Update button was clicked on the client results html page
    elif request.POST.get('update_client'):
        #Gets values from the table on the html page via javascript
        keys = list(request.POST.values())
        table_data = json.loads(keys[1])
        #Loop through each row and update database
        for i in table_data:
            for j in i:
                status = check_input_length_client(i[1], i[3], i[4], i[5], str(i[6]), i[7], i[8], i[9], i[10], i[11], i[12])
                if status != "":
                    return render(request, "client_result.html", {'error': status, 'table_data': table_data})
                else:
                    update_database("UPDATE client SET groupname='" + i[1] + "', locname='" + i[3] + "', addr_1='" + i[4] + "', addr_2='" + i[5] + "', city='" + i[6].title() + "', state='" + i[7].upper() + "', zip_code=" + i[8] + ", contact='" + i[9] + "', phone='" + i[10] + "', email='" + i[11] + "', claim_charge=" + i[12] + " WHERE grpno=" + i[0] + " AND locno=" + i[2])
        search1 = 0
        search2 = 0
        #Find if there are duplicate entries in a column, based on the results, figures out of the user searched for the data
        if duplicate_in_column(table_data, 2, table_data[0][2], len(table_data)) == 1:
            search2 = 1
        if duplicate_in_column(table_data, 0, table_data[0][0], len(table_data)) == 1:
            search1 = 1
        if search1 == 1 and search2 == 1:
            new_table = query("SELECT * FROM client WHERE grpno=" + table_data[0][0] + " AND locno=" + table_data[0][2] + "ORDER BY grpno")
        elif search2 == 1:
            new_table = query("SELECT * FROM client WHERE locno=" + table_data[0][2] + " ORDER BY grpno")
        elif search1 == 1:
            new_table = query("SELECT * FROM client WHERE grpno=" + table_data[0][0] + " ORDER BY grpno")
        #commented out just in case locno is unique to grpno
        #if len(table_data) > 1:
            #new_table = query("SELECT * FROM client ORDER BY grpno")
        #else:
            #new_table = query("SELECT * FROM client WHERE grpno=" + table_data[0][0])
        request.method = 'GET'
        #return to client results html page with updated table
        return render(request, "client_result.html", {'table_data': new_table})



    #If the Update button was clicked on the PPO results html page
    elif request.POST.get('update_ppo'):
        #Gets values from the table on the html page via javascript
        keys = list(request.POST.values())
        table_data = json.loads(keys[1])
        #Loop through and check each row for proper inputs and update database
        for i in table_data:
            for j in i:
                status = check_input_length_ppo(str(i[1].title()), str(i[2]), str(i[3].title()), str(i[4]))
                if status != "":
                    return render(request, "ppo_result.html", {'error': status, 'table_data': table_data})
                else:
                    update_database("UPDATE ppo SET active=" + i[1] + ", ppo_name='" + i[2] + "', ppo_method='" + i[3].title() + "', ppo_cost=" + i[4] + " WHERE ppono=" + i[0])
        #If the table has more than one row
        if len(table_data) > 1:
            new_table = query("SELECT * FROM ppo ORDER BY ppono")
        #Else the table has only one row
        else:
            new_table = query("SELECT * FROM ppo WHERE ppono=" + table_data[0][0])
        request.method = 'GET'
        #logger.error(new_table) #this is for error checking
        return render(request, "ppo_result.html", {'table_data': new_table})




    #If the Update button was clicked on the invoice results html page
    elif request.POST.get('update_invoices'):
        #Gets values from the table on the html page via javascript
        keys = list(request.POST.values())
        table_data = json.loads(keys[1])
        #Loop through each row and update database
        for i in table_data:
            for j in i:
                i[3] = i[3].title()
                status = check_input_length_invoices(i[3], i[4])
                if status != "":
                    return render(request, "invoices_result.html", {'error': status, 'table_data': table_data})
                else:
                    update_database("UPDATE invoice SET ppo_method='" + i[3] + "', ppo_charge='" + i[4] + "' WHERE grpno=" + i[0] + " AND locno=" + i[1] + " AND ppono=" + i[2])
        search1 = 0
        search2 = 0
        search3 = 0
        #Find if there are duplicate entries in a column, based on the results, figures out of the user searched for the data
        if duplicate_in_column(table_data, 2, table_data[0][2], len(table_data)) == 1:
            search3 = 1
        if duplicate_in_column(table_data, 1, table_data[0][1], len(table_data)) == 1:
            search2 = 1
        if duplicate_in_column(table_data, 0, table_data[0][0], len(table_data)) == 1:
            search1 = 1
        if search1 == 1 and search2 == 1 and search3 == 1:
            new_table = query("SELECT * FROM invoice WHERE grpno=" + table_data[0][0] + " AND locno=" + table_data[0][1] + " AND ppono=" + table_data[0][2] + "ORDER BY grpno, ppono")
        elif search2 == 1 and search3 == 1:
            new_table = query("SELECT * FROM invoice WHERE locno=" + table_data[0][1] + " AND ppono=" + table_data[0][2] + " ORDER BY grpno, ppono")
        elif search1 == 1 and search3 == 1:
            new_table = query("SELECT * FROM invoice WHERE grpno=" + table_data[0][0] + " AND ppono=" + table_data[0][2] + " ORDER BY grpno, ppono")
        elif search1 == 1 and search2 == 1:
            new_table = query("SELECT * FROM invoice WHERE grpno=" + table_data[0][0] + " AND locno=" + table_data[0][1] + " ORDER BY grpno, ppono")
        elif search3 == 1:
            new_table = query("SELECT * FROM invoice WHERE ppono=" + table_data[0][2] + " ORDER BY grpno, ppono")
        elif search2 == 1:
            new_table = query("SELECT * FROM invoice WHERE locno=" + table_data[0][1] + " ORDER BY grpno, ppono")
        elif search1 == 1:
            new_table = query("SELECT * FROM invoice WHERE grpno=" + table_data[0][0] + " ORDER BY grpno, ppono")
        request.method = 'GET'
        #logger.error(new_table) #for debugging
        return render(request, "invoices_result.html", {'table_data': new_table})

    #If the Calculate button was clicked on the claims html page
    elif request.POST.get('calculate'):
        #Gets values from the table on the html page via javascript
        keys = list(request.POST.values())
        table_data = json.loads(keys[1])
        #Get rows in claims where claim_charge is NULL/None
        
        #strVar = "SELECT clmpre, clmno, clmsuf, client.claim_charge FROM client, claim WHERE client.grpno=claim.grpno AND claim.claim_charge IS NULL AND (clmno = " + table_data[0][1]        
        #for i in range(len(table_data)):
            #strVar1 = " OR clmno = " + table_data[i][1]
            #strVar = strVar + strVar1
        #strVar = strVar + ")"
        #logger.error(strVar)
        #other_table_data = query(strVar)#
        
        other_table_data = query("SELECT clmpre, clmno, clmsuf, client.claim_charge FROM client, claim WHERE client.grpno=claim.grpno AND claim.claim_charge IS NULL")
        for i in range(len(other_table_data)):
            prefix = str(other_table_data[i][0])
            number = str(other_table_data[i][1])
            suffix = str(other_table_data[i][2])
            ccc = str(other_table_data[i][3])
            update_database("UPDATE claim SET claim_charge=" + ccc + "WHERE clmpre=" + prefix + " AND clmno=" + number + " AND clmsuf=" + suffix)
        #Get rows in claims where ppo_charge is NULL/None
        other_table_data = query("SELECT clmpre, clmno, clmsuf, invoice.ppo_method, invoice.ppo_charge, discamt FROM invoice, claim WHERE invoice.ppono=claim.ppono AND invoice.grpno=claim.grpno AND claim.ppo_charge IS NULL")
        #Calculates ppo_charge for claims table
        for i in range(len(other_table_data)):
            method = other_table_data[i][3]
            prefix = str(other_table_data[i][0])
            number = str(other_table_data[i][1])
            suffix = str(other_table_data[i][2])
            if method == "C":
                cpc = str(other_table_data[i][4])
            else:
                if other_table_data[i][5] is not None:
                    cpc = str(other_table_data[i][4] * other_table_data[i][5])
            update_database("UPDATE claim SET ppo_charge=" + cpc + "WHERE clmpre=" + prefix + " AND clmno=" + number + " AND clmsuf=" + suffix)
        #Get today's date
        time = str(date.today())
        todays_date = datetime.datetime.strptime(time, '%Y-%m-%d').strftime('%m/%d/%y')
        update_invoice_id_table = query("SELECT clmpre, clmno, clmsuf, grpno, ppono FROM claim WHERE invoice_id IS NULL ORDER BY grpno, ppono")
        #Finds last invoice_id used
        last_id_list = query("SELECT invoice_id FROM claim WHERE invoice_id IS NOT NULL ORDER BY invoice_id DESC LIMIT 1")
        if len(last_id_list) == 0:
            last_id = 0
        else:
            last_id = last_id_list[0][0]
        if len(update_invoice_id_table) > 0:
            update_database("UPDATE claim SET invoice_id=" + str(last_id) + ", invoice_date='" + todays_date + "' WHERE clmpre=" + str(update_invoice_id_table[0][0]) + " AND clmno=" + str(update_invoice_id_table[0][1]) + " AND clmsuf=" + str(update_invoice_id_table[0][2]))

        i = 1
        #Loop through each row and update table row
        for i in range(len(update_invoice_id_table)):
            if (update_invoice_id_table[i][3] != update_invoice_id_table[i-1][3]) or (update_invoice_id_table[i][4] != update_invoice_id_table[i-1][4]):
                last_id = last_id + 1
            update_database("UPDATE claim SET invoice_id=" + str(last_id) + ", invoice_date='" + todays_date + "' WHERE clmpre=" + str(update_invoice_id_table[i][0]) + " AND clmno=" + str(update_invoice_id_table[i][1]) + " AND clmsuf=" + str(update_invoice_id_table[i][2]))

        search1 = 0
        search2 = 0
        search3 = 0
        #Find if there are duplicate entries in a column, based on the results, figures out of the user searched for the data
        if duplicate_in_column(table_data, 2, table_data[0][2], len(table_data)) == 1:
            search3 = 1
        if duplicate_in_column(table_data, 1, table_data[0][1], len(table_data)) == 1:
            search2 = 1
        if duplicate_in_column(table_data, 0, table_data[0][0], len(table_data)) == 1:
            search1 = 1
        if search1 == 1 and search2 == 1 and search3 == 1:
            new_table = query("SELECT * FROM claim WHERE clmpre=" + table_data[0][0] + " AND clmno=" + table_data[0][1] + " AND clmsuf=" + table_data[0][2] + "ORDER BY invoice_id, clmpre, clmno")
        elif search2 == 1 and search3 == 1:
            new_table = query("SELECT * FROM claim WHERE clmno=" + table_data[0][1] + " AND clmsuf=" + table_data[0][2] + " ORDER BY invoice_id, clmpre, clmno")
        elif search1 == 1 and search3 == 1:
            new_table = query("SELECT * FROM claim WHERE clmpre=" + table_data[0][0] + " AND clmsuf=" + table_data[0][2] + " ORDER BY invoice_id, clmpre, clmno")
        elif search1 == 1 and search2 == 1:
            new_table = query("SELECT * FROM claim WHERE clmpre=" + table_data[0][0] + " AND clmno=" + table_data[0][1] + " ORDER BY invoice_id, clmpre, clmno")
        elif search3 == 1:
            new_table = query("SELECT * FROM claim WHERE clmsuf=" + table_data[0][2] + " ORDER BY invoice_id, clmpre, clmno")
        elif search2 == 1:
            new_table = query("SELECT * FROM claim WHERE clmno=" + table_data[0][1] + " ORDER BY invoice_id, clmpre, clmno")
        elif search1 == 1:
            new_table = query("SELECT * FROM claim WHERE clmpre=" + table_data[0][0] + " ORDER BY invoice_id, clmpre, clmno")
        request.method = 'GET'
        #logger.error(new_table) #for debugging
        return render(request, "claims_result.html", {'table_data': new_table})

    #If the Submit button on the Search screen is clicked
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            
            client_list = []
            ppo_list = []
            invoices_list = []
            claims_list =[]
            total_list = []
            #Whether there is an input or not, the data is cleaned so django can use it. If there is an input, then 1 is added to the appropriate list
            client_group_number = form.cleaned_data['client_group_number']
            if client_group_number != "":
                client_list.append(1)
            
            client_location_number = form.cleaned_data['client_location_number']
            if client_location_number != "":
                client_list.append(1)
            
            ppo_ppo_number = form.cleaned_data['ppo_ppo_number']
            if ppo_ppo_number != "":
                ppo_list.append(1)
            
            invoice_group_number = form.cleaned_data['invoice_group_number']
            if invoice_group_number != "":
                invoices_list.append(1)
            
            invoice_location_number = form.cleaned_data['invoice_location_number']
            if invoice_location_number != "":
                invoices_list.append(1)
            
            invoice_ppo_number = form.cleaned_data['invoice_ppo_number']
            if invoice_ppo_number != "":
                invoices_list.append(1)
            
            claim_prefix = form.cleaned_data['claim_prefix']
            if claim_prefix != "":
                claims_list.append(1)
            
            claim_number = form.cleaned_data['claim_number']
            if claim_number != "":
                claims_list.append(1)
            
            claim_suffix = form.cleaned_data['claim_suffix']
            if claim_suffix != "":
                claims_list.append(1)
            
            total_invoice_id = form.cleaned_data['total_invoice_id']
            if total_invoice_id != "":
                total_list.append(1)

            #Checks if multiple search are being made at once
            multiple_search = is_only_one_being_searched(client_list, ppo_list, claims_list, invoices_list, total_list)
            #If yes, then goes back to the Search screen with an error message popping up saying to only put in one search
            if multiple_search == 1:
                form = SearchForm
                request.method = 'GET'
                status = "Please input only for Client, PPO, Claims, Invoices or Total"
                return render(request, 'index.html', {'form': form, 'error': status})
            #If nothing is put in, then goes back to the Search screen with an error message popping up saying to put in an input
            elif multiple_search == 2:
                form = SearchForm
                request.method = 'GET'
                status = "Please put in an input"
                return render(request, 'index.html', {'form': form, 'error': status})

            #Else a valid search was made and now for the queries
            #If * is an input for Client
            if client_group_number == "*" or client_location_number == "*":
                #Make a query
                table_data = query("SELECT * FROM client ORDER BY grpno")
                #Goes to client results page with data
                return render(request, "client_result.html", {'table_data': table_data})
            #If Group Number and Location Number both have inputs in Client
            elif client_group_number != "" and client_location_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM client WHERE grpno=" + client_group_number + " AND locno=" + client_location_number)
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 1, client_group_number, 1, client_location_number, 1, None, 0)
                #If inputs do not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Client"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to client results page with data
                else:
                    return render(request, "client_result.html", {'table_data': table_data})
            #If only Group Number has an input only in Client
            elif client_group_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM client WHERE grpno=" + client_group_number)
                #Check if input is in database
                number_check = does_search_exist(table_data, 1, client_group_number, 1, None, 0, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Client"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to client results page with data
                else:
                    return render(request, "client_result.html", {'table_data': table_data})
            #If only Location Number has an input only in Client
            elif client_location_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM client WHERE locno=" + client_location_number)
                #Check if input is in database
                number_check = does_search_exist(table_data, 1, None, 0, client_location_number, 1, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Client"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to client results page with data
                else:
                    return render(request, "client_result.html", {'table_data': table_data})


            #If * is an input for PPO
            elif ppo_ppo_number == "*":
                #Make a query
                table_data = query("SELECT * FROM ppo ORDER BY ppono")
                #Goes to ppo results page with data
                return render(request, "ppo_result.html", {'table_data': table_data})
            #If PPO Number has an input in PPO
            elif ppo_ppo_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM ppo WHERE ppono=" + ppo_ppo_number)
                #Check if input is in database
                number_check = does_search_exist(table_data, 2, ppo_ppo_number, 1, None, 0, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for PPO"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to ppo results page with data
                else:
                    return render(request, "ppo_result.html", {'table_data': table_data})


            #If * is an input for Claims
            elif claim_prefix == "*" or claim_number == "*" or claim_suffix == "*":
                #Make a query
                table_data = query("SELECT * FROM claim ORDER BY invoice_id, clmpre, clmno")
                #Goes to claims results page with data
                return render(request, "claims_result.html", {'table_data': table_data})
            #If Prefix Number, Claim Number and Suffix Number have an input in Claims
            elif claim_prefix != "" and claim_number != "" and claim_suffix != "":
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmpre=" + claim_prefix + " AND clmno=" + claim_number + " AND clmsuf=" + claim_suffix + " ORDER BY invoice_id, clmpre, clmno")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 3, claim_prefix, 1, claim_number, 1, claim_suffix, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})
            #If Claim Number and Suffix Number have an input only in Claims
            elif claim_number != "" and claim_suffix != "":
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmno=" + claim_number + " AND clmsuf=" + claim_suffix + " ORDER BY invoice_id, clmpre, clmno")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 3, None, 0, claim_number, 1, claim_suffix, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})
            #If Prefix Number and Suffix Number have an input only in Claims
            elif claim_prefix != "" and claim_suffix != "":
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmpre=" + claim_prefix + " AND clmsuf=" + claim_suffix + " ORDER BY invoice_id, clmpre, clmno")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 3, claim_prefix, 1, None, 0, claim_suffix, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})
            #If Prefix Number and Claim Number have an input only in Claims
            elif claim_prefix != "" and claim_number != "":
                logger.error("Got here")
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmpre=" + claim_prefix + " AND clmno=" + claim_number + " ORDER BY invoice_id, clmpre, clmno")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 3, claim_prefix, 1, claim_number, 1, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})
            #If Prefix Number has an input only in Claims
            elif claim_prefix != "":
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmpre=" + claim_prefix + " ORDER BY invoice_id, clmpre, clmno")
                #Check if input is in database
                number_check = does_search_exist(table_data, 3, claim_prefix, 1, None, 0, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})
            #If Claim Number has an input only in Claims
            elif claim_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmno=" + claim_number + " ORDER BY invoice_id, clmpre, clmno")
                #Check if input is in database
                number_check = does_search_exist(table_data, 3, None, 0, claim_number, 1, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})
            #If Suffix Number has an input only in Claims
            elif claim_suffix != "":
                #Make a query based on input
                table_data = query("SELECT * FROM claim WHERE clmsuf=" + claim_suffix + " ORDER BY invoice_id, clmpre, clmno")
                #Check if input is in database
                number_check = does_search_exist(table_data, 3, None, 0, None, 0, claim_suffix, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Claims"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "claims_result.html", {'table_data': table_data})


            #If * is an input for Invoices
            elif invoice_group_number == "*" or invoice_location_number == "*" or invoice_ppo_number == "*":
                #Make a query
                table_data = query("SELECT * FROM invoice ORDER BY grpno, ppono")
                #Goes to invoices results page with data
                return render(request, "invoices_result.html", {'table_data': table_data})
            #If Group Number, Location Number and PPO Number have an input in Invoices
            elif invoice_group_number != "" and invoice_location_number != "" and invoice_ppo_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE grpno=" + invoice_group_number + " AND locno=" + invoice_location_number + " AND ppono=" + invoice_ppo_number + " ORDER BY grpno, ppono")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 4, invoice_group_number, 1, invoice_location_number, 1, invoice_ppo_number, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})
            #If Location Number and PPO Number have an input only in Invoices
            elif invoice_location_number != "" and invoice_ppo_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE locno=" + invoice_location_number + " AND ppono=" + invoice_ppo_number + " ORDER BY grpno, ppono")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 4, None, 0, invoice_location_number, 1, invoice_ppo_number, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})
            #If Group Number and PPO Number have an input only in Invoices
            elif invoice_group_number != "" and invoice_ppo_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE grpno=" + invoice_group_number + " AND ppono=" + invoice_ppo_number + " ORDER BY grpno, ppono")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 4, invoice_group_number, 1, None, 0, invoice_ppo_number, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})
            #If Group Number and Location Number have an input only in Invoices
            elif invoice_group_number != "" and invoice_location_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE grpno=" + invoice_group_number + " AND locno=" + invoice_location_number + " ORDER BY grpno, ppono")
                #Check if inputs are in database
                number_check = does_search_exist(table_data, 4, invoice_group_number, 1, invoice_location_number, 1, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})
            #If Group Number has an input only in Invoices
            elif invoice_group_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE grpno=" + invoice_group_number + " ORDER BY grpno, ppono")
                #Check if input is in database
                number_check = does_search_exist(table_data, 4, invoice_group_number, 1, None, 0, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})
            #If Location Number has an input only in Invoices
            elif invoice_location_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE locno=" + invoice_location_number + " ORDER BY grpno, ppono")
                #Check if input is in database
                number_check = does_search_exist(table_data, 4, None, 0, invoice_location_number, 1, None, 0)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})
            #If PPO Number has an input only in Invoices
            elif invoice_ppo_number != "":
                #Make a query based on input
                table_data = query("SELECT * FROM invoice WHERE ppono=" + invoice_ppo_number + " ORDER BY grpno, ppono")
                #Check if input is in database
                number_check = does_search_exist(table_data, 4, None, 0, None, 0, invoice_ppo_number, 1)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if number_check == 0:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input valid numbers for Invoices"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to invoices results page with data
                else:
                    return render(request, "invoices_result.html", {'table_data': table_data})


            #For Find Total
            elif total_invoice_id != "":
                table_data = query("SELECT sum(claim_charge), sum(ppo_charge) FROM claim WHERE invoice_id=" + total_invoice_id)
                #If input does not exist, then goes back to Search screen with error message popping up saying to put in a valid number
                if table_data[0][0] is None and table_data[0][1] is None:
                    form = SearchForm
                    request.method = 'GET'
                    status = "Please input a valid Invoice ID for Find Total"
                    return render(request, 'index.html', {'form': form, 'error': status})
                #Else input exists and goes to claims results page with data
                else:
                    return render(request, "total_cost_result.html", {'table_data': table_data, 'invoice_id': total_invoice_id})
            
        else:
            status = "Only enter in valid numbers or *"
    
    #request = GET and goes to Search screen with no error message
    else:
        form = SearchForm()

    return render(request, 'index.html', {'form': form, 'error': status})
