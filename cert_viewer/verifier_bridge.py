from cert_verifier import verifier
from flask import request
from cert_core.cert_store import helpers
from cert_core.cert_model import model
import json
from cert_viewer import app


def verify():
    model_id = request.args.get('verify-button')
    certificate_model = app.config[model_id]

    from . import cert_store
    # certificate = cert_store.get_certificate(certificate_uid)
    certificate = certificate_model
    if certificate:
        # A walk around to set default etherscan api token as '' to avoid
        # TypeError in composing ethesan URL. The options can be removed
        # when https://github.com/blockchain-certificates/cert-verifier/pull/21
        # is deployed. 
        options={'etherscan_api_token':''}
        verify_response = verifier.verify_certificate(certificate, options=options)
        return verify_response
    else:
        raise Exception('Cannot find certificate with uid=%s', certificate_uid)
