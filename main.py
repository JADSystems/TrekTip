

from imports import *;
#import __init__;
# defining the jinja2 hook to utilize for accessing the templates;

jinja_environment= jinja2.Environment(
                                      
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+"/templates"));

# Defining globals;

#----------------------------------------------------------      
def fetchCredentialsDB(web):
    # Web will be the variable self passed through to be used; 
    global firstName,lastName,userName;
    userName=web.request.get("userName");
    session=get_current_session();
    userNameSession=session.get('userName',userName);
    if userNameSession=='' or userNameSession==' ' or userNameSession=='userName' or userNameSession==None:
        return False;
    #if not (str(userNameSession).__contains__(userName)):
    #    return False;
    password=session.get('password',' ');
    env = os.getenv('SERVER_SOFTWARE');
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
    
    
    #passKey=web.request.get("password");
    getUserName='''
        select trektip.User.userName from trektip.User
        where trektip.User.userName='%s';
    '''%userNameSession;
    cursor.execute(getUserName);
    userNameDB='';
    userNameDB+=str(cursor.fetchone());
    
    if  userNameDB.__contains__(userName):
        getfirstName='''
        select trektip.User.firstName from trektip.User
        where trektip.User.userName='%s';
        '''%userNameSession;
        cursor.execute(getfirstName);
        firstName=str(cursor.fetchone());
        firstName=firstName.translate(None,'''()@#,$\'''')
        getlastName='''
        select trektip.User.lastName from trektip.User
        where trektip.User.userName='%s';
        '''%userNameSession;
        cursor.execute(getlastName);
        lastName=str(cursor.fetchone());
        lastName=lastName.translate(None,'''()@#,$\'''')
        
    else:
        
        return False;
   
    
#         for i in cursor.fetchall():
#             firstName+=str(i);
   
    getPassword='''
        select trektip.User.passKey from trektip.User
        where trektip.User.userName='%s';
    '''%userNameSession;
    cursor.execute(getPassword);
    passwordDB='';

    passwordDB+=str(cursor.fetchone());
    if passwordDB.__contains__(password):
        
        return True;
    else:
        
        return False;
    
#----------------------------------------------------------

def getComments(web):
    global comments;
    session=get_current_session();
    userName=session.get('userName',' ');
    env = os.getenv('SERVER_SOFTWARE');
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
    
    #username=web.request.get("username");
    #passKey=web.request.get("password");
    getAllComments='''
        SELECT distinct c.ID, c.rating, c.infoID, i.infoText
        FROM trektip.Comment c, trektip.User u, trektip.Information i
        where c.userName='%s'
        and u.userName='%s'
        and c.ID=i.commentID;
    '''%(userName,userName);
    cursor.execute(getAllComments);
    comments=[];
    n=0;
    for r in cursor.fetchall():
        #comments+= str(r)+'<br/>';
        comments.append(str(r));
        comments[n]=comments[n].translate(None,'''()@#,$\'''')
        n=n+1;
    
    
    
    
    
def checkLogOut(web):
    if fetchCredentialsDB(web)==False:
            
        session=get_current_session();
        #session['userName']=userName;
        #logInfo=str(session['userName']);
        session.terminate()
        template_values.update({'firstName':'','lastName':'','loginForm':loginForm, 'homeLink':'/default'});
        template_values.update({'backgroundImg':defaultBackgroundImg});
        template=jinja_environment.get_template('default.html');
        
        #self.response.out.write(template.render(template_values));
        #self.response=MainHandler(self);
        #web.redirect('/default');
        return True; # if log out is strue, then that means we are logged out;
    else:
        return False;


def search(web, searchval, searchlat, searchlng):

    env = os.getenv('SERVER_SOFTWARE');
    if (env and env.startswith('Google App Engine/')):
        # Connecting from App Engine
        db = MySQLdb.connect(
        unix_socket='/cloudsql/trektip:trektipsql',
        user='root',passwd='TfReETO88zFyArUa65za');
    else:
        # Connecting from an external network.
        # Make sure your network is whitelisted
        db = MySQLdb.connect(
        host='2001:4860:4864:1:4c3a:dc28:7694:1e53',
        port=3306,
        user='root',
        passwd='TfReETO88zFyArUa65za');
    cursor=db.cursor();
    if searchval != '123':
        searchQuery='use trektip; \nCALL search_attr(' + searchlat +',' + searchlng +',' + searchval+');';
    else:
        searchQuery='use trektip; \nCALL search_loc(' + searchlat +',' + searchlng+');';
    cursor.execute(searchQuery);
    resultSet = '';

    for r in cursor.fetchall():
        resultSet += str(r);
     
    template_values.update({'searchResult':searchQuery});
    return;
    

#----------------------------------------------------------

class MainHandler(webapp2.RequestHandler):
    def get(self):
        
        #Check if Search, if so.. perform search
        searchButton=self.request.get("searchButtonInput")
        if searchButton == 'ON':
            #search(self);
            self.redirect('/login');
            return;
        
        
        if checkLogOut(self)==False:
            self.redirect('/userHome');
            return;
        
        template_values.update({'firstName':'','lastName':'','loginForm':loginForm, 'homeLink':'/default'});
       
            
        template_values.update({'backgroundImg':defaultBackgroundImg});
        template=jinja_environment.get_template('default.html');
        #template=jinja_environment.get_template('mapTest.html');
        #self.response.out.write(template.render(template_values));
        self.response.out.write(template.render(template_values));
        
  
        
    def post(self):
        #Check if Search, if so.. perform search
        searchButton=self.request.get("searchButtonInput")
        lat=self.request.get("searchLat");
        lng=self.request.get("searchLng");
        searchVal=self.request.get("searchVal");
        if searchButton == 'ON':
            search(self, searchVal,lat,lng);
            self.redirect('/searchHome');
            return;
        else:
            session=get_current_session();
            userName=self.request.get('userNameLogin');
            password=self.request.get('password');
            session['userName']=userName;
            session['password']=password;
            if fetchCredentialsDB(self)==True:
                loggedIn='';
                template_values.update({'firstName':firstName,'lastName':lastName,'backgroundImg':defaultBackgroundImg,'loginForm':logOut, 'homeLink':'/userHome'});
            else:
                template_values.update({'testP':'Error in Credentials', 'homeLink':'/default'});
                template=jinja_environment.get_template('default.html');
                self.response.out.write(template.render(template_values));
                return;
                     
                
            self.redirect('/userHome');
i=0;

#----------------------------------------------------------        
class TestHandler(webapp2.RequestHandler):
    
    def get(self):
        
        if checkLogOut(self)==True:
            self.redirect('/default');
            return;
            
        template=jinja_environment.get_template('test.html');
        self.response.out.write(template.render(template_values));
    def post(self):
        
        #Check if Search, if so.. perform search
#         searchButton=self.request.get("searchButton")
#         if searchButton == 'ON':
#             search(self);
        
        #Check if logOut. IF so, then go back to default.html
        logOutButton=self.request.get('logOutButton');
        if logOutButton=='ON':
            loggedOut=checkLogOut(self);
   
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
        #img=self.request.get('imgIn');
        img='';
        imgB=self.request.get('imgButton');
        if imgB=='Submit':
            img='';
            img1URL=blobstore.create_upload_url('/uploadBlob');
            #img=open('brooklynBridge0.jpg','rb');
            query='''
            update trektip.Information as info
            set info.infoType='%s',
            info.infoText='test0'
            where info.ID=1;
            
        '''
        #cursor.execute()
        global i;
        i=i+1;
        testText='Testing from post; %s'%str(i);
        template_values.update({'testText':testText,'testImg':img});
        template=jinja_environment.get_template('test.html');
        self.response.out.write(template.render(template_values));
#----------------------------------------------------------
class UserHomeHandler(webapp2.RequestHandler):
    def get(self):
        #Check if logged on. If not, then go back to default.html
        if checkLogOut(self)==True:
            self.redirect('/default');
            return;
        getComments(self);
        template_values.update({'comments':comments});
        template=jinja_environment.get_template('userHome.html');
        self.response.out.write(template.render(template_values));
        
    def post(self):
#         #Check if Search, if so.. perform search
#         searchButton=self.request.get("searchButton")
#         if searchButton == 'ON':
#             search(self);
            
        #Check if logOut. IF so, then go back to default.html
        logOutButton=self.request.get('logOutButton');
        if logOutButton=='ON':
            loggedOut=checkLogOut(self);
            self.redirect('/default');
            return;
        else:
            getComments(self);
            template_values.update({'comments':comments});
            template=jinja_environment.get_template('userHome.html');
            self.response.out.write(template.render(template_values));
#---------------------------------------------------------- 
         
class CreateAttractionHandler(webapp2.RequestHandler):
    def get(self):
        if checkLogOut(self)==True:
            self.redirect('/default');
            return;
        template=jinja_environment.get_template('attractionCreation.html');
        self.response.out.write(template.render(template_values));
        
        
    def post(self):
        #Check if Search, if so.. perform search
#         searchButton=self.request.get("searchButton")
#         if searchButton == 'ON':
#             search(self);
#         
        #Check if logOut. IF so, then go back to default.html
        logOutButton=self.request.get('logOutButton');
        if logOutButton=='ON':
            loggedOut=checkLogOut(self);
            self.redirect('/default');
            return;
        
        self.redirect('/userHome');
#---------------------------------------------------------- 

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        
        #Check if Search, if so.. perform search
#         searchButton=self.request.get("searchButton")
#         if searchButton == 'ON':
#             search(self);
            
        if checkLogOut(self)==False:
            self.redirect('/userHome');
            return;
        template=jinja_environment.get_template('login.html');
        self.response.out.write(template.render(template_values));
        
        
    def post(self):
        
        getLoginButton=self.request.get('loginButtonInput');
        
    
        
        if getLoginButton=='ON':
            session=get_current_session();
            userName=self.request.get('userNameLogin');
            password=self.request.get('password');
            session['userName']=userName;
            session['password']=password;
            if fetchCredentialsDB(self)==True:
                
                template_values.update({'firstName':firstName,'lastName':lastName,'backgroundImg':defaultBackgroundImg,'loginForm':logOut, 'homeLink':'/userHome'});
            else:
                template_values.update({'testP':'Error in Credentials', 'homeLink':'/default'});
                template=jinja_environment.get_template('default.html');
                #self.response.out.write(template.render(template_values));
                self.redirect('/default');
                return;
            self.redirect('/userHome');
        else:
            # other button input to take in; 
            # for the moment, default to back to default.html;
            self.redirect('/default');
        
            
        
        
#---------------------------------------------------------- 
 
class SearchHandler(webapp2.RequestHandler):
    def get(self):       
        template=jinja_environment.get_template('searchHome.html');
        template
        self.response.out.write(template.render(template_values));
    
    def post(self):
        template=jinja_environment.get_template('searchHome.html');
        self.response.out.write(template.render(template_values));
            
class RegisterHandler(webapp2.RequestHandler):
    def get(self):
#         if checkLogOut(self)==False:
#             self.redirect('/userHome');
#             return;
        template=jinja_environment.get_template('register.html');
        self.response.out.write(template.render(template_values));    
    
    def post(self):
        
        getRegisterButtonInput=self.request.get('registerButtonInput');
        if getRegisterButtonInput=='ON':
            newFirstName=self.request.get('firstNameRegister');
            newLastName=self.request.get('lastNameRegister');
            newUserName=self.request.get('userNameRegister');
            newEmail=self.request.get('email');
            newPassword=self.request.get('passwordInput');
            registerUser(newFirstName,newLastName,newUserName,newEmail,newPassword);
            session=get_current_session();
            session['userName']=newUserName;
            session['password']=newPassword;
            if fetchCredentialsDB(self)==True:
                template_values.update({'firstName':firstName,'lastName':lastName,'backgroundImg':defaultBackgroundImg,'loginForm':logOut, 'homeLink':'/userHome'});
            self.redirect('/userHome');
        else:
            self.redirect('/default');
        
        
        
def registerUser(fn,ln,un,e,p):
    
    env = os.getenv('SERVER_SOFTWARE');
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
    putRegisterUserDB='''
        insert into trektip.User (userName, userType, firstName, lastName, passKey)
        values ('%s','user','%s','%s','%s');commit
    '''%(un,fn,ln,p);
    cursor.execute(putRegisterUserDB);
    
    
        

        
#----------------------------------------------------------       


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/default', MainHandler),
    ('/userHome', UserHomeHandler),
    ('/test',TestHandler),
    ('/userHome', UserHomeHandler),
    ('/attractionCreation', CreateAttractionHandler),
    ('/login',LoginHandler),
    ('/register',RegisterHandler),
    ('/searchHome', SearchHandler)
], debug=True)
