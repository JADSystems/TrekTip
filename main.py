

import webapp2

import jinja2;
import os;
import MySQLdb;

# defining the jinja2 hook to utilize for accessing the templates;

jinja_environment= jinja2.Environment(
                                      
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"));
    
    
# defining default variable to go into template_values;
dummyvalue="<p></p>";
defaultBackgroundImg='''
<img src="/images/blank.jpg" >

'''

# defining the default template_values;

template_values={
                         
             'firstName':'',
             'lastName':'',
             'testP':dummyvalue
             
             };
# class LoginHandler(webapp2.RequestHandler):
#     def get(self):
#         template=jinja_environment.get_template('userHome.html');
#         self.response.out.write(template.render(template_values));            

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values.update({'backgroundImg':defaultBackgroundImg});
        template=jinja_environment.get_template('default.html');
        self.response.out.write(template.render(template_values));
        
    def post(self):
        env = os.getenv('SERVER_SOFTWARE')
        if (env and env.startswith('Google App Engine/')):
            # Connecting from App Engine
            db = MySQLdb.connect(
            unix_socket='/cloudsql/trektip:trektipsql',
            user='root',passwd='TfReETO88zFyArUa65za');
        else:
            # Connecting from an external network.
            # Make sure your network is whitelisted
            db = MySQLdb.connect(
            host='173.194.248.180',
            port=3306,
            user='root',
            passwd='TfReETO88zFyArUa65za');
        cursor=db.cursor();
       
        username=self.request.get("username");
        passKey=self.request.get("password");
        getFirstName='''
            select trektip.User.firstName from trektip.User
            where trektip.User.userName='%s';
        '''%username;
        cursor.execute(getFirstName);
        firstName='';
        for i in cursor.fetchall():
            firstName+=str(i);
        getLastName='''
            select trektip.User.lastName from trektip.User
            where trektip.User.userName='%s';
        '''%username;
        cursor.execute(getLastName);
        lastName='';
        for i in cursor.fetchall():
            lastName+=str(i);
        
        template_values.update({'firstName':firstName,'lastName':lastName});
        template=jinja_environment.get_template('userHome.html');
        self.response.out.write(template.render(template_values));
        

class UserHomeHandler(webapp2.RequestHandler):
    def get(self):
        template=jinja_environment.get_template('userHome.html');
        self.response.out.write(template.render(template_values));
        
class CreateAttractionHandler(webapp2.RequestHandler):
    def get(self):
        template=jinja_environment.get_template('attractionCreation.html');
        self.response.out.write(template.render(template_values));

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template=jinja_environment.get_template('login.html');
        self.response.out.write(template.render(template_values));

class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        template=jinja_environment.get_template('register.html');
        self.response.out.write(template.render(template_values));
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/default', MainHandler),
    ('/userHome', UserHomeHandler),
    ('/attractionCreation', CreateAttractionHandler),
    ('/login',LoginHandler),
    ('/register',RegisterHandler)
], debug=True)
