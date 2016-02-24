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
from rest_framework import status


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
    For registering new users.
    '''
    data = JSONParser().parse(request)  
    print data  
    serializer = RegistrationSerializer(data=data) 
    if serializer.is_valid():
        data = serializer.data
        u = User.objects.create(username=data['username'])
        u.set_password(data['password'])
        u.save() 
        return JSONResponse({"comment":"User created"}, status=status.HTTP_201_CREATED)
    return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST ) 


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
    return JSONResponse({"comment":"database updated"},status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def list_( request ):
    '''
    For url friend_list, provides a list of all contacts.
    '''
    objs = Person.objects.filter(owner=request.user)
    serializer = PersonSerializer(objs,many = True )
    data = { 'persons':serializer.data }
    return JSONResponse(data,status=status.HTTP_200_OK)


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
        cf_status = check_codeforces_handle(data['codeforces_handle'])

        if cc_status and cf_status:
            p = Person(name=data['name'],codechef_handle=data['codechef_handle'],
                                         codeforces_handle=data['codeforces_handle']
                                         ,owner=request.user ) 
            p.save()
            data = { 'result':serializer.data }
            return JSONResponse( data,status=status.HTTP_201_CREATED )
        else:
            JSONResponse({"comment":"Incorrect handle name provided"},status=status.HTTP_406_NOT_ACCEPTABLE )        #not cottect details provided for handles
    return JSONResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view( ['DELETE'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def delete_contact( request,person_id ):
    '''
    Deletes a contact provided its person_id/pk from Person class.
    '''
    try:
        Person.objects.get( pk = person_id )
    except Person.DoesNotExist:
        return JSONResponse({"comment":"Person Doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
    else:
        p_object = Person.objects.get( pk = person_id )
        if p_object is not None:
            p_object.delete()
            return HttpResponse(status=status.HTTP_200_OK)
        else :
            return JSONResponse({"comment":"Person Doesn't exist"},status=status.HTTP_400_BAD_REQUEST)

@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def profile( request,person_id ):
    '''
    Gives all questions done a particular contact provided its person_id/pk from Person class.
    {
    "codechef_problems":
       [ 
              {"Contest name":"qwert","questions":[list of questions]}
              {"":"","":""}
       ] 
    "codeforces_problems":
        [
              {"Contest name":"345","questions":[list of questions] }
              {"":"","":""}
        ]
     }

    '''
    try:
        Person.objects.get(owner=request.user,pk=person_id)
    except Person.DoesNotExist:
        return JSONResponse({"comment":"Person doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
    else:
        person = Person.objects.get(owner=request.user,pk=person_id)
    cf_contest = Contest.objects.filter( site ='Codeforces' )
    cf_obj=[]                                        # a list containing [[contest name,[questions]],[]] 
        
    for contest in cf_contest:                        # fetching all contest problems
        ques = Question.objects.filter( contest = contest,person=person )
        if len(ques) != 0:
            serializer = QuestionSerializer(ques,many=True)
            cf_obj.append( {'Contest name':contest.contestId,'questions':serializer.data}  )
        
    cc_contest = Contest.objects.filter( site='Codechef' )
        
    cc_obj=[]
    for contest in cc_contest:
        ques = Question.objects.filter( contest = contest, person = person )
        if len(ques) != 0:
            serializer = QuestionSerializer(ques,many=True)
            cc_obj.append( [ {'Contest name':contest.name,'questions':serializer.data} ] )
        
    return JSONResponse( { 'codeforces_problems' : cf_obj ,'codechef_problems' : cc_obj ,},
                        status=status.HTTP_200_OK )

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
    return JSONResponse(data,status=status.HTTP_200_OK)
    
@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated,TokenHasReadWriteScope, ))
def SearchForThisContest(request,site,contest):
    '''
    for codechef   : write contest name.
    for codeforces : write contestId.
    Fetches all the questions of all contacts when a contest in selected

    [
        {
           "person":"hitesh",
           "questions": [list of all questions]
        }
        etc..
    ]
    '''
    questions_done_by_all_person = []
    try:
        if site == "Codeforces":
            contest = Contest.objects.get(contestId = contest)
        else:
            contest = Contest.objects.get(name=contest)
    except Contest.DoesNotExist:
        return JSONResponse({"comment":"Contest doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
    
    persons = Person.objects.filter( owner = request.user )
    
    for person in persons:
        ques = Question.objects.filter( person = person, contest = contest )
        qserializer = QuestionSerializer(ques,many=True)
        pserializer = PersonSerializer(person)
        questions_done_by_all_person.append( { "person":pserializer.data,"questions":qserializer.data } )
        data = {"result" : questions_done_by_all_person}
    return JSONResponse( data ,status=status.HTTP_200_OK)

@api_view( ['GET'] )
@permission_classes((permissions.IsAuthenticated, TokenHasReadWriteScope,))
@csrf_exempt
def update_a_person_info(request,person_id):
    '''
    Updates information about a particular contact provided its person_id/pk from Person class.
    '''
    try:
        Person.objects.get(pk=person_id)
    except Person.DoesNotExist :
        return JSONResponse({"comment":"person doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
    person = Person.objects.get(pk=person_id)
    print person
    current = HelperFunctions(request,person_id)
    current.FetchContentForAPerson()
    
    return JSONResponse({"comment":"Info Updated"},status=status.HTTP_200_OK)