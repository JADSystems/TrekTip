## Config file;
from gaesessions import SessionMiddleware

def webapp_add_wsgi_middleware(app):
    app=SessionMiddleware(app,cookie_key="afeawefwaedsfa43t65g1er6541bhrt854n64534346gr14e51v56fd1");
    return app;
