from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.desk.reportview import get_match_cond, get_filters_cond
from frappe.utils import nowdate
from collections import defaultdict
from frappe.utils import cstr, cint, flt, getdate, rounded
from datetime import datetime,timedelta

@frappe.whitelist()
def get_timedtls_dtls(warehouse):
    company = frappe.db.sql("select parent,warehouse,ending_time from `tabWarehouse Time Dtls` WHERE warehouse = %(string1)s",{'string1': warehouse},as_dict=1)
    return company

@frappe.whitelist()
def get_datedtls_possce(location):
    currentTimeDate = datetime.now() - timedelta(days=1)
    last_date =  currentTimeDate.strftime("%Y-%m-%d")
    
    frappe.log_error(message=last_date,title='last_date')
    
    ctime = frappe.db.get_all('Warehouse Time Dtls', filters={ 'warehouse': location }, fields=['ending_time'])
    
    from frappe.utils import now
    currentdate = frappe.utils.get_datetime(now())
    
    if len(ctime) > 0:
        datetime_str = str(frappe.utils.getdate())+" "+str(ctime[0]["ending_time"] )
        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d  %H:%M:%S')

        if datetime_object <= currentdate:

            #Date
            currentTimeDate = datetime.now() - timedelta(days=0)
            currentdate = currentTimeDate.strftime('%Y-%m-%d  %H:%M:%S')
            currentdate2 = currentTimeDate.strftime('%Y-%m-%d')
           # frappe.msgprint( msg= "Current " + currentdate +" "+ time_string, title='Date & Time')
        else :
        
            #Date
            currentTimeDate = datetime.now() - timedelta(days=1)
            currentdate = currentTimeDate.strftime('%Y-%m-%d  %H:%M:%S')
            currentdate2 = currentTimeDate.strftime('%Y-%m-%d')
            #frappe.msgprint( msg= "Old " + currentdate +" "+ time_string, title='Date & Time')
    else :

        #Date
        currentTimeDate = datetime.now() - timedelta(days=0)
        currentdate = currentTimeDate.strftime('%Y-%m-%d  %H:%M:%S')
        currentdate2 = currentTimeDate.strftime('%Y-%m-%d')
        #frappe.msgprint( msg= "Old " + currentdate +" "+ time_string, title='Date & Time')
        datetime_str = ""
        datetime_object = datetime.now()
        
    curTimDat = datetime.now() - timedelta(days=0)
    currdatevl = curTimDat.strftime('%Y-%m-%d')
    #--------------------------------------------------------
    values = {'warehouse': location }
    datedtls = frappe.db.sql("""
        SELECT
            date,time,user,location
        from `tabPOS Shift Clossing Entry`
        WHERE location = %(warehouse)s order by date desc limit 1
    """, values=values, as_dict=1)
    if datedtls:
        #datetime_str = str(datedtls[0].date)+" "+str(datedtls[1].time)
        #datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d  %H:%M:%S')
    
        currentTimeDate = datedtls[0].date - timedelta(days=-1)
        post_dates = currentTimeDate
    else:
        post_dates = currdatevl
    
    
    
    date = frappe.db.sql("select date,user,location from `tabPOS Shift Clossing Entry` WHERE location=%(string1)s and date=%(dt)s order by date desc limit 1 ",{'string1': location,'dt':post_dates},as_dict=1)
    return date

@frappe.whitelist()
def get_lastclos_date(location):
    warehouse = frappe.db.sql("select date,user,location from `tabPOS Shift Clossing Entry` WHERE location=%(string1)s order by date desc limit 1 ",{'string1': location},as_dict=1)
    return warehouse