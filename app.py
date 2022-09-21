
import bottle
import hmac
import hashlib
import ipdb as pdb
from bottle import request

SECRET_KEY = "123456"

@bottle.post("/hook")
def index():

    sig_header = request.headers.get("X-Hub-Signature")
    if not sig_header:
        raise Exception("value missing")

    sig_hash_type, sig_value = sig_header.split("=")

    body = request.body.read()
    hash_func = getattr(hashlib, sig_hash_type)

    sig_local = hmac.new(
        SECRET_KEY.encode("utf-8"), 
        msg=body, 
        digestmod=getattr(hashlib, sig_hash_type),
    )

    if not hmac.compare_digest(sig_local.hexdigest(), sig_value):
        raise Exception("invalid")

    print(bottle.request.json.get("ref"))

    return 1


if __name__ == "__main__":
    bottle.run(host="0.0.0.0", debug=True)
