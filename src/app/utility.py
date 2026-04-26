import logging
import traceback
from typing import Any, Optional, Union
from fastapi import Request

import hmac
import hashlib
import urllib.parse

logger = logging.getLogger("server.error")

async def exception_handler(e:Exception, req:Optional[Request] = None, data:Optional[Union[dict, str]] = None):
    traceback_str = traceback.format_exception(type(e), e, e.__traceback__)
    traceback_message = ''.join(traceback_str)

    if req:
        try:
            if req.method == "POST":
                request_data = await req.json()
            else:
                request_data = dict(req.query_params)
        except Exception as ex:
            request_data = f"<failed to extract request data: {ex}>"
    else:
        request_data = data

    logger.error("================================================================================")
    if req: logger.error("🚨 Source:\n",f"[{req.method}] {str(req.url)}")
    if request_data : logger.error("📦 Request data:\n", request_data)
    logger.error("💥 An error occurred:\n", traceback_message)
    logger.error("================================== ERROR =======================================")

    return traceback_message

def verify_hmac(params: dict, client_secret: str) -> bool:
    """
    params: all query-string key-value pairs (including 'hmac')
    Returns True if the hmac is valid.
    """
    received_hmac = params.get("hmac", "")
    
    # Remove hmac, sort remaining params alphabetically
    filtered = [(k, v) for k, v in params.items() if k != "hmac"]
    filtered.sort(key=lambda x: x[0])
    
    # Rebuild query string: key=value&key=value...
    message = urllib.parse.urlencode(filtered)
    
    # Compute HMAC-SHA256
    computed = hmac.new(
        client_secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(computed, received_hmac)