from instagram.client import InstagramAPI

# Fix Python 2.x.
try:
    import __builtin__

    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass

client_id = input("Client ID: ").strip()
client_secret = input("Client Secret: ").strip()
redirect_uri = input("Redirect URI: ").strip()
scope = ['basic', 'comments', 'relationships', 'likes']

api = InstagramAPI(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope=scope)

print ("Visit this page and authorize access in your browser: " + redirect_uri)

code = (str(input("Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)
print ("access token: ")
print (access_token)