# Stalker
Eases your work by collecting information of codechef/codeforces activities of your friends.
It is implemented with a simple REST API with Django, Django REST Framework and OAuth2.

### APIs Used:
    - Codeforces

### Features :
    - Provides contest-wise search for both codechef and codeforces.
    - Provides individual profile, containing codechef and codeforces questions done by a particular contact.
    - Uses OAuth2 for signup/registration and sending requests.
    - you can update your contact list as required.

### Dependies :
      django==1.7.7
      django_oauth2_provider 
      djangorestframework
      markdown
      django-filter
      json
      urllib2
      BeautifulSoup4

For further help on how to register your app and send request see help.md.
For results of request see result.txt.

#### Features can be integrated:
    - Filtering of questions done on a particular date.
    - Scores obtained for questions.

### Useful links:
    - http://www.django-rest-framework.org/
    - https://django-oauth-toolkit.readthedocs.org/en/latest/rest-framework/getting_started.html