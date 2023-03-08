import json

def application(environ, start_response):
    request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    request_body = environ['wsgi.input'].read(request_body_size)
    request_json = json.loads(request_body)

    response = { "result": 0 }
    for value in request_json['operands']:
        response['result'] += value
    
    start_response('200 OK', [('Content-Type', 'application/json')])
    yield str.encode(json.dumps(response))
