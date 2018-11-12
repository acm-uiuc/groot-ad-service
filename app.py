from flask import Flask, jsonify, request, make_response
import secrets
import logging
import json
import ldap

logger = logging.getLogger('groot_ad_service')
logging.basicConfig(level="INFO")

app = Flask(__name__)
app.config['JSONIFY_MIMETYPE'] = 'application/json; charset=UTF-8'

PORT = 8998


def addUserToAD(netid):
    logger.info('Adding {} to AD'.format(netid))

    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)

    USER_DN = 'cn=' + netid + ',' + secrets.USER_BASE_DN
    USER_DN = str.encode(USER_DN)
    modlist = [(ldap.MOD_ADD, 'member', [USER_DN])]

    try:
        ldap_connection = ldap.initialize(secrets.LDAP_SERVER)
        ldap_connection.start_tls_s()
        ldap_connection.simple_bind_s(secrets.BIND_DN, secrets.BIND_PASS)
        ldap_connection.modify_s(secrets.ACM_USERS_DN, modlist)
        ldap_connection.unbind_s()
        logger.info('Successfully added {}'.format(netid))
    except ldap.ALREADY_EXISTS:
        logger.info('{} was already a member'.format(netid))
        return True
    except Exception as e:
        logger.error('Error while adding {}, error {}'.format(netid, e))
        return False
    return True


@app.route('/activedirectory/add', methods=['POST'])
def addUser():
    data = request.get_json(force=True)
    if not data:
        logger.error('Bad JSON recieved')
        return make_response(jsonify(dict(error='Could not parse JSON')), 400)
    if(addUserToAD(data['netid'])):
        return make_response(jsonify(dict(message=str('Success'))), 200)
    else:
        return make_response(jsonify(dict(error='Error')), 400)


if __name__ == "__main__":
    app.run(port=PORT, host='0.0.0.0', debug=True)
