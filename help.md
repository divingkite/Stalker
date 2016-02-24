### For creating database tables run in stalksite directory:
  <pre>
  python manage.py makemigrations
  python manage.py migrate
  </pre>
### For develpoment purpose you can build a local server by running in stalksite directory:
  <pre>
  python manage.py runserver
  </pre>

  This will create a server at http://127.0.0.1:8000

Request here use curl to test the API on localhost. You can use any http client like Postman too.

### Register your app through:
    http://localhost:port/o/applications/register/
    Enter your name.
    Select Authorization grant type to be Resource owner password-based and register.
    Collect client-id and client-password after registering.

### Example requests:

    1. To register:
        curl -X POST http://localhost:port/register/ --data '{"username":"Your Guess","passowrd":"your password"}'
        
    2. To get access token :
        curl -X POST -d "grant_type=password&username=<your useranme>&password=<your password>" -u"<client_id>:<client_password>" http://localhost:Port/o/token/

        this will provide access token and its expire time.

    3. To send request:
        curl -X REQUEST_METHOD -H "Authorization: Bearer <access_token>" <url>  --data '{"":"","":"","":""}'
        
### Example:
   
    1. To get contact list:
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/friend_list/ 
      
    2. To add contact:
        curl -X POST -H "Authorization: Bearer <access_token>" http://localhost:8000/expand_list/  
         --data '{"name":"hitesh","codechef_handle":"hiteshiitbhu",
                   "codeforces_handle":"hiteshagrawal"}'
          
    3. To update every contacts information/data:
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/refresh/
        
    4.  To access individual profile:
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/profile/10/
        
    5.   To remove a person from contact list:
        curl -X DELETE -H "Authorization: Bearer <access_token>" http://localhost:8000/delete/10/
  
    6.  To show list of all contests:
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/search_contest/Codechef/

        for codechef  : /search_contest/Codechef/
        for codeforces: /search_contest/Codeforces/

    7. To show every contact's performance in a contest:
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/contest_performance/Codechef/FEB16/

         for codechef   : /contest_performance/Codechef/contest_name
         for codeforces : /contest_performance/Codeforces/contestId
 
    8. To update a particular contact,provided by person_id/pk ,information/data:
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/refresh/10/
