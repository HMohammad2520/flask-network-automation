from flask import Blueprint, jsonify, abort, request

test = Blueprint('test', 'test', url_prefix='/test')



@test.route('/test_error')
def raise_error():
    code = int(request.args.get('code', 500))
    mode = request.args.get('mode', 'raise')
    if mode == 'raise':
        raise Exception(str(code))

    elif mode == 'abort':
        return abort(code)

    else:
        return abort(501)
