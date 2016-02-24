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
    <pre>
    http://localhost:port/o/applications/register/
    </pre>

    Enter your name.
    Select Authorization grant type to be Resource owner password-based and register.
    Collect client-id and client-password after registering.

### Example requests:

    1. To register:
        <pre>
        curl -X POST http://localhost:port/register/ --data '{"username":"Your Guess",
                                                         "passowrd":"your password"}'
        </pre>

    2. To get access token :
        <pre>
        curl -X POST -d "grant_type=password&username=<your useranme>&password=<your password>" -u"<client_id>:<client_password>" http://localhost:Port/o/token/
        </pre>

        this will provide access token and its expire time.

    3. To send request:
        curl -X REQUEST_METHOD -H "Authorization: Bearer <access_token>" <url>  --data '{"":"","":"","":""}'
        
## Example:
   
   i. To get contact list:
      <pre>
      curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/friend_list/ 
      </pre>

   ii. To add contact:
       <pre>  
   	   curl -X POST -H "Authorization: Bearer <access_token>" http://localhost:8000/expand_list/  
         --data '{"name":"hitesh","codechef_handle":"hiteshiitbhu",
                   "codeforces_handle":"hiteshagrawal"}'
       </pre>
   
   iii. To update every contacts information/data:
        <pre>
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/refresh/
        </pre>

   iv.  To access individual profile:
        <pre>
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/profile/10/
        </pre>

   v.   To remove a person from contact list:
        <pre>
        curl -X DELETE -H "Authorization: Bearer <access_token>" http://localhost:8000/delete/10/
        </pre>

   vi.  To show list of all contests:
        <pre>
        curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/search_contest/Codechef/
        </pre>

        for codechef  : /search_contest/Codechef/
        for codeforces: /search_contest/Codeforces/

    vii. To show every contact's performance in a contest:
         <pre>
         curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/contest_performance/Codechef/FEB16/
         </pre>

         for codechef   : /contest_performance/Codechef/contest_name
         for codeforces : /contest_performance/Codeforces/contestId
 
    viii. To update a particular contact,provided by person_id/pk ,information/data:
          <pre>
          curl -X GET -H "Authorization: Bearer <access_token>" http://localhost:8000/refresh/10/
          </pre>
