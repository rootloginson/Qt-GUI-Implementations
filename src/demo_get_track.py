import random
import requests
from . import auth
from . import api_task_requests
from .custom_exception_check import trigger_starttime_log


def random_string() -> str:
    consonants = "bcçdfgğhjklmnpqrstvwxyz"
    vowels = "aeıioöuü"
    word_len = random.randint(2, 5)
    word = []
    for i in range(word_len):
        if random.random() < 0.5:
            word.append(random.choice(vowels))
        else:
            word.append(random.choice(consonants))
    return ''.join(word)


def gui_auth_check(client_id: str,
                   client_secret: str) -> None or requests.models.Response:

    # instance variable for access token requests
    token = auth.Tokens()
    r = None  # requests.models.Response object

    # adds approximate function call time(GMT 0:00 format) to log file.
    trigger_starttime_log("gui_auth_check")

    # Access Token request for the track search
    r = token.request_client_credential_access_token(client_id, client_secret)

    if r is None:   # exception contol such as Connection Error
        return None
    else:
        # request object received
        return r


def run_spotify_app(client_credential_access_token: str):

    # instance variable for api requests and helper methods
    spochastify = api_task_requests.Spochastify()

    r_search = None       # requests.models.Response object
    search_string = ''           # word for track search request
    returned_items_list = []   # track list retrieved due to search request

    ### Make a Track Search Request, Retrieve the Result ###

    for i in range(5):  # range(5) is number of attempts if track list is empty
        # get a random search string
        search_string = random_string()

        # Requesting a track search with search string
        r_search = spochastify.make_track_search(
                        client_credential_access_token,
                        search_string
                        )

        # request object control
        if r_search is None:  # exception contol such as 'Connection Error'
            return None
        elif r_search.status_code == 200:  # 200 is OK. The request has succeeded
            returned_items_list = spochastify.extract_list_of_tracks(r_search)
        else:
            return r_search  # request received. But a non-desired result.

        # if there is a track in track list, pick a random track
        if returned_items_list:
            # pick one of the returned items
            random_track_item = random.choice(returned_items_list)
            track_details = spochastify.extract_track_info(random_track_item)
            return track_details

    # when retrieving random track fails
    print("Failed to retrieve any tracks list")
    return None
