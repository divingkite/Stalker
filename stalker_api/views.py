from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from stalker_api.helper_functions import *
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializer import *
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from stalker_api.permissions import IsOwner

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

"""@csrf_exempt
def register(request):
    '''
    To register a user, input is via RegistrationForm.
    '''
    if request.method == 'POST':
    	data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print serializer.data
            user = authenticate( username = serializer.validated_data['username'], password = serializer.validated_data['password'] )
            auth_login( request,user )
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)
     
"""
@csrf_exempt
def logout_page(request):
    if request.method == "GET":
        logout(request)
        return JSONResponse({"result":"logout"},status=200)

@csrf_exempt
def login(request):
    '''
    Upon login redirects to the friend_list page.
    '''
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer( data = data )
        
        if serializer.is_valid():
            print serializer.data["username"],serializer.validated_data['username']
            user = authenticate( username = serializer.validated_data['username'], password = serializer.validated_data['password'] )
            print user
            if user is not None:
                auth_login( request,user )
                return JSONResponse({},status=200)
            return JSONResponse({},status=400)

@api_view(['GET'])
#@permission_classes((IsOwner, ))
def home(request):
    return JSONResponse({"user":"csdsd"},status=200)
            #return JSONResponse({"fail":"csdsd"},status=200)

    #else:
     #   return HttpResponse({})

#@permission_classes((IsAuthenticated, ))
def update_info(request):
    '''
    For the refresh button, which updates all information about all contacts.
    '''
    if request.method == "GET":
        current = HelperFunctions(request)
        current.FetchContent()
        objs = Person.objects.filter()
        serializer = PersonSerializer( objs, many=True)
        return JSONResponse(serializer.data,status=200)

#@permission_classes((IsAuthenticated, ))
def list_( request ):
    #if request.user.is_authenticated():
    if request.method == "GET":
        objs = Person.objects.filter()
        serializer = PersonSerializer(objs,many = True )
        return JSONResponse(serializer.data,status=200)

#@permission_classes((IsAuthenticated, ))
@csrf_exempt
def expand_list( request ):
    if request.method == "POST":
    	data = JSONParser().parse(request)
        serializer = PersonSerializer(data = data)    
        if serializer.is_valid():
        	serializer.save()
        	return JSONResponse(serializer.data,status=200)
        return JSONResponse(serializer.errors,status=400)

#@permission_classes((IsAuthenticated, ))
def delete_contact( request,person_id ):
	#if request.method == "DELETE":
	p_object = Person.objects.get( pk = person_id )
	if p_object is not None:
		p_object.delete()
		return HttpResponse(status=204)
	else:
		return HttpResponse(status=404)
        

#@permission_classes((IsAuthenticated, ))
def profile( request,person_id ):
    if request.method == "GET":
        person = Person.objects.get(pk=person_id)
        cf_contest = Contest.objects.filter( site ='CF' )
        cf_obj=[]                                        # a list containing [[contest name,[questions]],[]] 
        
        for contest in cf_contest:                        # fetching all contest problems
            ques = Question.objects.filter( contest = contest,person=person )
            if len(ques) != 0:
                serializer = QuestionSerializer(ques,many=True)
            	cf_obj.append( [contest.name,serializer.data ] )
        
        cc_contest = Contest.objects.filter( site='CC' )
        
        cc_obj=[]
        for contest in cc_contest:
            ques = Question.objects.filter( contest = contest, person = person )
            if len(ques) != 0:
            	serializer = QuestionSerializer(ques,many=True)
                cc_obj.append( [contest.name,serializer.data ] )
            
        #cf_prac = PracticeProb.objects.filter( person = person,site='CF' )     #fetching all practice problems.
        #cc_prac = PracticeProb.objects.filter( person = person,site='CC' )
        
        return JSONResponse( { 'cf_data_chal' : cf_obj ,
                               'cc_data_chal' : cc_obj ,
                               #'cc_data_prac' : cc_prac ,
                               #'cf_data_prac' : cf_prac 
                               } )

#@permission_classes((IsAuthenticated, ))
def search_contestwise( request,site ):
    '''
    Gives list of all contest when site ( CC,CF ) is provided
    '''
    #if request.user.is_authenticated():
    if request.method == "GET":
        cons = Contest.objects.filter( site=site )
        serializer = ContestSerializer(cons,many=True)
        return JSONResponse(serializer.data,status=200)
    #else :
     #   return HttpResponseRedirect( reverse( 'stalkerNew:login' ))

#@permission_classes((IsAuthenticated, ))
def SearchForThisContest(request,site,contest):
    '''
    Fetches all the questions of all contacts when a contest in selected in contest.html page.
    '''
    if request.method == "GET" :
        questions_done_by_all_person = []
        if site == "CF":
            contest = Contest.objects.get(contestId = contest)
        else:
            contest = Contest.objects.get(name=contest)
        #persons = Person.objects.filter( user = request.user )
        persons = Person.objects.filter()
        for person in persons:
            ques = Question.objects.filter( person = person, contest = contest )
            qserializer = QuestionSerializer(ques,many=True)
            pserializer = PersonSerializer(person)
            questions_done_by_all_person.append( [pserializer.data,qserializer.data] )
        
        return JSONResponse( questions_done_by_all_person ,status=200)

#@permission_classes((IsAuthenticated, ))
@csrf_exempt
def update_a_person_info(request,person_id):
    '''
    Updates information about a particular contact.
    '''
    if request.method == "GET":
        current = HelperFunctions(request,person_id)
        current.FetchContentForAPerson()
        objs = Person.objects.filter()
        serializer = PersonSerializer(objs,many-True)
    return JSONResponse(serializer.data,status=200)


