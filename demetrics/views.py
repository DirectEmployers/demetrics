import datetime
import httplib2
import json
import locale
import time
from apiclient.discovery import build
from demetrics.queries import redirects as redirects_queries
from django.conf import settings
from django.db import connection, connections, transaction
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from oauth2client.client import * 
from oauth2client.file import Storage  
from oauth2client.tools import run_flow,run 
from operator import itemgetter

# global OAuth objects and variables
flow = OAuth2WebServerFlow(
    client_id=settings.GA_CLIENT_ID,
    client_secret=settings.GA_CLIENT_SECRET,
    scope='https://www.googleapis.com/auth/analytics',
    redirect_uri='http://demetrics.com:8000/auth_return')   
TOKEN_FILE_NAME = 'analytics.dat'
VIEW_ID = settings.GA_VIEW_ID

locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def read_my_jobs(request):
    """
    View object for the DE Metrics homepage. Handles calls to the my.jobs
    database and setups the ajax forms for google analytics api calls.
    
    """
    cursor = connections['myjobs'].cursor()

    # Accounts created by week
    cursor.execute(redirects_queries["accounts-by-week"])
    new_accounts = cursor.fetchall()
    new_accounts = sorted(new_accounts)
    del new_accounts[-1]
    
    # saved searches by group by week
    cursor.execute(redirects_queries["saved-searches-by-group"])
    saved_schs = cursor.fetchall()
    saved_schs = sorted(saved_schs)
    ss = __consolidate_rows(saved_schs)
    del ss[-1] # The last entry is for the current week and always incomplete

    # Binary Resume Completion
    cursor.execute(redirects_queries["binary-resumes"])
    binary_resumes = sorted(cursor.fetchall())
    binary_resumes_percentage = []
    for week in binary_resumes:
        total = float(week[1])+float(week[2])
        resume_percentage = int(float(week[1])/total*100)
        tup = (week[0], resume_percentage, 100-resume_percentage)
        binary_resumes_percentage.append(tup)
    del binary_resumes_percentage[-1]


    # Resume Completion by Week Joined
    cursor.execute(redirects_queries['resumes-by-week-joined'])
    resumes_by_week = cursor.fetchall()
    rbw = __consolidate_rows(resumes_by_week)
    del rbw[-1]

    # Google API Section
    try: # We only want to run this if there is a valid OAuth object
        ga = GoogleAnalytics()
        serv = ga.initialize_service()
        accounts = ga.get_microsite_accounts(serv)
    except: # There are a number of possible exceptions, hence the catch-all
        accounts = False
    
    # Build the data dictionary and render the page
    data_dict = {
        'new_accounts': new_accounts,
        'saved_schs': ss,
        'binary_resumes': binary_resumes_percentage,
        'rbw': rbw, 
        'accounts': accounts,
        }

    return render_to_response('table.html', data_dict, RequestContext(request))


def ga_ajax(request):
    """
    Performs a query of the Google Analytics API and returns the results as a
    JSON object. 
    
    Inputs (via GET):
    :accounts:  comma delimited list of google account numbers
    :metric:    the specific metric type being requested
    :start_date:the start date (future functionality)
    :end_date:  tne end date (future functionality)
    
    Returns:
    JSON results
    
    """
    try:
        ga = GoogleAnalytics()
        serv = ga.initialize_service()
    except:
        return HttpResponse(json.dumps({'error':'expired or bad token'}),
            content_type="application/json")
        
    accounts = request.GET.get('accounts').split(",")
    try:
        metric = request.GET.get('metric')
    except KeyError:
        metric = 'sessions'
    
    try:
        start = request.GET.get('start_date')
    except KeyError:
        start=False
    try:
        end = request.GET.get('end_date')
    except KeyError:
        end=False

    try:
        props = ga.get_microsite_profiles(serv, accounts)
    except:
        return HttpResponse(json.dumps({'error':'expired or bad token'}),
            content_type="application/json")
    ga_data=[]
    
    for prop in props:
        prop_sessions = ga.get_ga_metric(
            serv,prop['id'],metric,start,end)        
        try:
            if prop_sessions:
                for row in prop_sessions.get('rows'):
                    #cell_data = []
                    for cell in row:
                        #cell_data.append(cell)
                        cell_data = int(cell)
                    cell_data_formated = locale.format("%d", 
                        cell_data, grouping=True)
                    node = {
                        'name': prop['name'],
                        'url': prop['websiteUrl'],
                        metric: cell_data_formated, 
                        'raw_metric': cell_data, 
                        'start': ga.get_default_date(start,"start"),
                        'end': ga.get_default_date(end,"end"),
                        }
                    ga_data.append(node)
        except:
            pass # error handling would be good, but not a priority yet
        time.sleep(.25)

    if len(ga_data)==0:
        ga_data = "{'name':'error','Metric':'There was an error',}"

    try: # sort the results by descending metric count
        ga_data = sorted(ga_data, key=itemgetter('raw_metric'))
        ga_data.reverse() 
    except: # skip if there is a key error, type error, or some other mismatch
        pass

    data_dict = {
        'ga_data': ga_data,
        }
        
    return HttpResponse(json.dumps(ga_data), content_type="application/json")


def GAAuth(request):
    """
    Iniates the Google OAuth handshake.
    
    """
    auth_url = flow.step1_get_authorize_url()
    return redirect(auth_url)


def auth_return(request):
    """
    Handles the Oauth return from google and stores the resulting token for
    later use by the API.
    
    """
    token_code = request.GET['code']
    credentials = flow.step2_exchange(token_code)
    http = httplib2.Http()
    http = credentials.authorize(http)
    storage = Storage(TOKEN_FILE_NAME)
    if credentials is None or credentials.invalid:
        pass
    else:
        storage.put(credentials)
        
    data_dict = {'ga_data':token_code,}
    
    return HttpResponseRedirect("/")


def __consolidate_rows(db_list):
    """
    placeholder list and tuple for re-grouping data. The data comes in as multi
    rows per date and needs to be combined into one row per date.
    
    Inputs:
        :db_list:  database result set

    Returns:
        :cons_list: db_list consolidated to have all daata points for a given 
                    date in a single row.

    """ 
    cons_list = []
    tup = ()
    date = ""
    for row in db_list:
        if row[0] == date:
            tup += (str(row[2]),)
        else:
            cons_list.append(tup)
            date = row[0]
            tup = ('%s' % date, str(row[2]),)

    cons_list.append(tup)

    return cons_list


class GoogleAnalytics(object):
    """
    Global class for interacting with the Google Analytics API. It is dependent
    on a successful OAuth session, and will return false if one is not present.
    
    Most of this is taken from the Hello Analytics tutorial, but it is heavily
    modified since the original tutorial is broken.
    
    """    
    
    def __init__(self):  
        self.service = None
    
    def _authenticate(self):  
        # Retrieve existing credendials
        storage = Storage(TOKEN_FILE_NAME)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run(flow, storage, self.GAFlags())                        

        return credentials

    def _create_service(self):  
        # 1. Create an http object
        http = httplib2.Http()
        
        # 2. Authorize the http object
        credentials = self._authenticate()
        http = credentials.authorize(http) 
        
        # 3. Build the Analytics Service Object with the authorized http object
        return build('analytics', 'v3', http=http)

    def start_service(self):  
        """
        :return: ``this`` Google analytics object with the service set
        
        start the service which may be used to query the google analytics api
        """
        if not self.service:
            self.service = self._create_service()
        return self
        
    def prepare_credentials(self):
        storage = Storage(TOKEN_FILE_NAME)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
          credentials = False
        return credentials

    def initialize_service(self):        
      http = httplib2.Http()

      #Get stored credentials or run the Auth Flow if none are found
      credentials = self.prepare_credentials()

      if credentials:
          http = credentials.authorize(http)
          #Construct and return the authorized Analytics Service Object
          return build('analytics', 'v3', http=http)
      else:
          return False

    def get_ga_metric(self, service, profile_id,metric='sessions', 
        start=False, end=False):
        """
        Use the Analytics Service Object to query the Core Reporting API
        
        Inputs:
        :service:       OAuth service object
        :profile_id:    Profile ID to look up numbers for
        :metric:        The metric desired, less "ga:" (check the API docs)
        :start:         Start date
        :end:           End Date
        
        Returns:
        :metric_data:   JSON object with metrics for the requested profile_id
        
        """        
        if not start:
            start = self.get_default_date(False,"start")
          
        if not end:
            end = self.get_default_date(False,"end")
                
        ga_metric = "ga:"+metric
        metric_data = service.data().ga().get(
            ids='ga:' + profile_id, 
            start_date=start,
            end_date=end,
            metrics=ga_metric).execute()
          
        return metric_data

    def get_microsite_accounts(self, service):
        """
        Returns the acounts associated with an OAuth user.
        
        Inputs:
        :service:   OAuth service object
        
        Returns:
        :accounts:  JSON object with account information
        
        """
        ga_accounts = service.management().accounts().list().execute()
        accounts = []
        for ai in ga_accounts.get('items'):
            a = {'id':ai['id'],'name':ai['name']}
            accounts.append(a)
        return accounts
    
    def get_microsite_profiles(self, service, accounts):
        """
        Given an analytics account, retrieve all the profiles associated with it
        
        Inputs:
        :service:   The OAuth service object
        :accounts:  list of accounts from which to retrieve profiles
        
        Returns:
        :properties:list of profile JSON objects
        
        """
        properties = []
        for account in accounts:
            props = service.management().webproperties().list(
                accountId=account
                ).execute()            
            items = props['items']
            i=items[0]
            i_id = i['id'].split('-')[1]
            profiles = service.management().profiles().list(
               accountId=i_id,
               webPropertyId='~all'
               ).execute()
            for p in profiles['items']:
                properties.append(p)
                
        return properties
    
    def get_default_date(self,date,datetype):
        if datetype == 'start':
            date_delta=8 # set default start to sunday of previous week
        else:
            date_delta=2 # set default end to saturday of previous week            
        if not date:
            today = datetime.date.today()
            date = today - datetime.timedelta(days=today.weekday()+date_delta)
            date = date.strftime('%Y-%m-%d')    
        return date
        
                
    class GAFlags():  
        """
        total hack. If you want to see why, examine apiclient.sample_tools. 
        The python bindings as well as the documentation kind've forgot to 
        mention this...which is a big deal..but actually though.

        """
        noauth_local_webserver = True
        logging_level = "DEBUG"    
