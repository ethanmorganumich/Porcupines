from urllib.parse import urlparse
from supabase import create_client
from dotenv import load_dotenv
import jwt, os, re


load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
SECRET = os.getenv("SECRET")

# Checks that an incoming API request is coming from an authenticated session
# Accepts an http request with JSON content
# Returns:
#   if(session is invalid) -> Exception explainging error
#   else -> Dict containing access_token and refresh_token
def check_valid_request(request):

    json_data = {}
    if(request.method == 'GET'):
        param_array = re.split(';|=', urlparse(request.path).params)
        json_data = {
            'access_token': param_array[1],
            'refresh_token': param_array[3]
        }
    else:
        json_data = request.get_json()

    check = check_JWT_token(json_data)
    ret = {
        'access_token': json_data['access_token'],
        'refresh_token': json_data['refresh_token']
    }

    # return exception if invalid request
    if(type(check) is Exception):
        return check
    # add new tokens if session refreshed
    elif(type(check) is dict):
        ret['access_token'] = check['access_token']
        ret['refresh_token'] = check['refresh_token']
    
    return ret


# Parse JWT token to confirm that token session is valid and user is authenticated
# Accepts a json representation of request data
# Returns:
#   if(token is Valid) -> True
#   elif(token was refreshed) -> Dict containing new refresh_token and access_token
#   else -> Exception explaining error
def check_JWT_token(json_data):
    try: 
        jwt_token = jwt.decode(jwt=json_data['access_token'], key=SECRET ,algorithms=["HS256"], audience="authenticated")
    except:
        return Exception("user token not authenticated")


    jwt_args = {
        "sid": jwt_token['session_id'],
        "uid": jwt_token['sub'],
        "ts": jwt_token['exp']
    }

    supabase = create_client(API_URL, API_KEY)
    valid = supabase.rpc('confirm_JWT_token', jwt_args).execute()

    if(not valid.data):
        try:
            session = supabase.auth._call_refresh_token(json_data['refresh_token'])
            supabase.auth._remove_session()
            return {
                "access_token": session['access_token'],
                "refresh_token": session['refresh_token']  
            }
        except:
            return Exception("could not refresh user session")
    return 1

# Helper for merging dicts
def Merge(dict1, dict2):
    if dict1: 
        res = {**dict1, **dict2}
    else:
        res = {**dict2}
    return res
    