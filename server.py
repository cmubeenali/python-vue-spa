from werkzeug.wrappers import Request,Response
from werkzeug.routing import Rule,Map
from werkzeug.middleware.shared_data import SharedDataMiddleware
import logging,json,os

class App(object):
    def __init__(self):
        self.url_map = Map([
            Rule('/',endpoint='api_handler')
        ])
    
    def wsgi_app(self,env,start_resp):
        try:
            request=Request(environ=env)
            template_content="hello world!"
            with open(os.path.dirname(__file__)+'/static/template/index.html','rb')as file:
                template_content=file.read()
            return Response(template_content,mimetype='text/html')(env,start_resp)
        except Exception as err:
            logging.error("ERROR(SRV) : "+str(err))

    def __call__(self, env, start_resp):
        return self.wsgi_app(env, start_resp)

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    app = App()
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/':  os.path.join(os.path.dirname(__file__)+'/static', 'template')
    })
    run_simple('0.0.0.0', 8000, app, use_reloader=True,threaded=True)