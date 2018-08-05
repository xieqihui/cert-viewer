from flask import request
from cert_core.cert_store import helpers
from cert_core.cert_model import model
from cert_viewer import app
from datetime import datetime

def award(certificate_uid=None):
    requested_format = request.args.get('format', None)
    # TO show and verify uploaded json certificate
    if request.method == 'POST':
        certificate_bytes = request.files['cert_json'].read()
        certificate_json = helpers.certificate_bytes_to_json(certificate_bytes)
        certificate_model = model.to_certificate_model(certificate_json)
        from . import certificate_formatter
        award = certificate_formatter.certificate_to_award(certificate_model)    
        model_id = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
        print(model_id)
        app.config[model_id] = certificate_model
        return {'award': award, 
                'verification_info': model_id}
    elif requested_format == 'json':
        return get_award_json(certificate_uid)
    else:
        from . import cert_store, certificate_formatter
        award, verification_info = certificate_formatter.get_formatted_award_and_verification_info(
             cert_store,
             certificate_uid)
        return {'award': award,
                'verification_info': verification_info}


def get_award_json(certificate_uid):
    from . import cert_store
    certificate_json = cert_store.get_certificate_json(certificate_uid)
    return certificate_json
