from stalker_api.models import *
from django.http import HttpResponseRedirect, HttpResponse
from stalker_api.helper_functions import *
from django.contrib.auth.models import User
from stalker_api.serializer import *
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.views import APIView
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['POST'])
@permission_classes(())
def Registration(request):
    '''
    For registration of new users.
    '''
    data = JSONParser().parse(request)
    serializer = RegistrationSerializer(data=data) 
    if serializer.is_valid():                           #user can be created
        data = serializer.data
        user = User.objects.create(username=data['username'])
        user.set_password(data['password'])
        user.save() 
        return JSONResponse(serializer.data, status=201)
    return JSONResponse(serializer.errors, status=400)   # user not creatd


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, TokenHasReadWriteScope,))
def update_info(request):
    '''
    For the refresh url, which updates all information about all contacts.
    '''
    current = HelperFunctions(request=request)
    current.FetchContent()
    objs = Person.objects.filter(owner=request.user)
    serializer = PersonSerializer( objs, many=True)
    return JSONResponse(serializer.data,status=200)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def list_( request ):
    '''
    For url friend_list, provides a list of all contacts.
    '''
    objs = Person.objects.filter(owner=request.user)
    for o in objs:
        print o.name
    serializer = PersonSerializer(objs,many = True )
    data = { 'persons':serializer.data }
    return JSONResponse(data,status=200)


@api_view( ['POST'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
@csrf_exempt
def expand_list( request ):
    '''
    For url expand_list, used to add new contacts.
    '''
    data = JSONParser().parse(request)
    serializer = PersonSerializer(data=data)
    if serializer.is_valid():
        data = serializer.data
        cc_status = check_codechef_handle(data['codechef_handle'])      
        #True if correct handle name is provided in request, else false.

        cf_status = check_codeforces_handle(data['codeforces_handle'])
        #True if correct handle name is provided in request, else false.

        if cc_status and cf_status:
            #if both handle names are correct
            p = Person(name=data['name'],codechef_handle=data['codechef_handle'],
                                         codeforces_handle=data['codeforces_handle']
                                         ,owner=request.user ) 
            p.save()
            data = { 'result':serializer.data }
            return HttpResponse( status=200 )
        else:
            HttpResponse(400)         #not cottect details provided for handles
    return JSONResponse(serializer.errors,status=400)   #Bad request
    

@api_view( ['DELETE'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def delete_contact( request,person_id ):
    '''
    Deletes a contact provided its person_id/pk from Person class.
    '''
    p_object = Person.objects.get( pk = person_id )
    if p_object is not None:
        p_object.delete()
        return HttpResponse(status=204)    
    else :
        return HttpResponse(status=400)  #Bad request

@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def profile( request,person_id ):
    '''
    Gives all questions done a particular contact provided its person_id/pk from Person class.
    '''
    person = Person.objects.get(owner=request.user,pk=person_id)
    
    cf_contest = Contest.objects.filter( site ='Codeforces' )
    cf_obj=[]                                         
    for contest in cf_contest:                        # fetching all contest problems
        ques = Question.objects.filter( contest = contest,person=person )
        if len(ques) != 0:
            serializer = QuestionSerializer(ques,many=True)
            cf_obj.append( [ {'Contest name':contest.name},{'questions':serializer.data} ] )
        
    cc_contest = Contest.objects.filter( site='Codechef' )
    cc_obj=[]
    for contest in cc_contest:
        ques = Question.objects.filter( contest = contest, person = person )
        if len(ques) != 0:
            serializer = QuestionSerializer(ques,many=True)
            cc_obj.append( [ {'Contest name':contest.name},{'questions':serializer.data} ] )
            
             
    return JSONResponse( { 'codeforces_problems' : cf_obj ,
                            'codechef_problems' : cc_obj ,
                         } )

@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def search_contestwise( request,site ):
    '''
    Gives list of all contest when site ( Codechef/Codeforces ) is provided
    '''
    print request.user
    cons = Contest.objects.filter( site=site )
    serializer = ContestSerializer(cons,many=True)
    data = {'contests':serializer.data}
    return JSONResponse(data,status=200)
    
@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def SearchForThisContest(request,site,contest):
    '''
    for codechef   : write contest name.
    for codeforces : write contestId.
    Fetches all the questions of all contacts when a contest in selected
    '''
    print request.user
    questions_done_by_all_person = []
    if site == "Codeforces":
        contest = Contest.objects.get(contestId = contest)
    else:
        contest = Contest.objects.get(name=contest)
    persons = Person.objects.filter( owner = request.user )
    #persons = Person.objects.filter()
    for person in persons:
        ques = Question.objects.filter( person = person, contest = contest )
        qserializer = QuestionSerializer(ques,many=True)
        pserializer = PersonSerializer(person)
        questions_done_by_all_person.append( [pserializer.data,qserializer.data] )
        
    return JSONResponse( questions_done_by_all_person ,status=200)

@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated, TokenHasReadWriteScope,))
@csrf_exempt
def update_a_person_info(request,person_id):
    '''
    Updates information about a particular contact provided its person_id/pk from Person class.
    '''
    print request.user
    current = HelperFunctions(request,person_id)
    current.FetchContentForAPerson()
    objs = Person.objects.filter()
    serializer = PersonSerializer(objs,many-True)
    return JSONResponse(serializer.data,status=200)