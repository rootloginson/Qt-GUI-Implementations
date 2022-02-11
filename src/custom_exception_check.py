import logging
import requests
import time


def create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
    formatter.converter = time.gmtime
    file_handler = logging.FileHandler("spotify_app.log")
    file_handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    return logger, formatter


def trigger_starttime_log(info_msg: str) -> None:
    """Logging time is GMT 0"""
    time_format_name = formatter.converter.__name__
    logger.info(f"{info_msg}. (time format: {time_format_name})")


logger, formatter = create_logger()


def request_call_with_exception_check(f):
    """
    Request object.__bool__ returns:
            True (success): if 200 <= status < 400
            False (error) : else

   ! Logging time is in GMT/UTC +0

    Arguments:
        API request
            r = request_call_with_exception_check(
            lambda: requests.get(url, headers=headers),
            )

    Returns :
        If no exception raise returns a "request object".
        If exception catched returns "None".
    """
    request_from = f.__qualname__.split(".")[:-2]
    request_from = ".".join(request_from)
    request_from = "=".join(["request_from", request_from])
    # request_from format e.g.: "request_from:
    error_body = "request_status=FAILED, requests.exception="

    def log_failed_request_exception(exception_name: str) -> None:
        """When the requests.models.Response object cannot be retrieved"""
        logger.error("%s%s, %s", error_body, exception_name, request_from)

    try:
        r = f()  # r is a requests.models.Response object
        r.raise_for_status()

    except requests.exceptions.ConnectionError:
        log_failed_request_exception('ConnectionError')

    except requests.exceptions.Timeout:
        log_failed_request_exception('Timeout')

    except requests.exceptions.HTTPError:
        log_failed_request_exception('HTTPError')

    except requests.exceptions.ProxyError:
        log_failed_request_exception('ProxyError')

    except requests.exceptions.SSLError:
        log_failed_request_exception('SSLError')

    except requests.exceptions.RequestException as e:
        log_failed_request_exception(str(type(e)))

    else:
        # For the condition in which requests.models.Response is received
        # Authentication Error Object Check
        try:
            _ = r.json()['error']
        except KeyError:
            logger.info("%s, %s=%s, %s",
                        "request_status=SUCCESS",
                        "status_code", r.status_code,
                        request_from,
                        )
            return r
        else:
            logger.error("%s, %s=%s, %s=%s, %s",
                         "request_status=ERROR",
                         "status_code", r.status_code,
                         "error", r.json(),
                         request_from
                         )
            return r

    return None
