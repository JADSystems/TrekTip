'''
Created on Jul 21, 2015

@author: Florida

This is a code dump; Mainly to keep track of where the code to be deleted
is being dumped for possible future use;
'''



'''
#fetchCredentialsDB(self) ;
        #logOutB=self.request.get('logOutButton');
        #strB=str(logOutB);
        
        #if fetchCredentialsDB(self)==True:
        #loggedIn='Logged In';
        #template_values.update({'firstName':firstName,'lastName':lastName,'loginForm':logOut, 'homeLink':'/userHome'});
      #  else:
      
       #session=get_current_session();
        #session.terminate()
        
        
        #logOutB=self.request.get('logOutButton');
        #strB=str(logOutB);
        
        # if logout text was submitted properly, this should log out;
        if fetchCredentialsDB(self)==True:
            # Check for another button because the credentials are still good. Login is still working;
            loggedIn='Logged In';
            template_values.update({'firstName':firstName,'lastName':lastName,'loginForm':logOut, 'homeLink':'/userHome'});
            getComments(self);
            template_values.update({'comments':comments});
            template=jinja_environment.get_template('userHome.html');
            self.response.out.write(template.render(template_values));
        else:
            
            template=jinja_environment.get_template('default.html');
            session=get_current_session();
            session['userName']=userName;
            logInfo=str(session['userName']);
            session.terminate()
            template_values.update({'firstName':'','lastName':'','loginForm':loginForm, 'homeLink':'/default','testP':logInfo});
            template_values.update({'backgroundImg':defaultBackgroundImg});
            self.response.out.write(template.render(template_values));
        
        
        #template_values.update({'firstName':firstName,'lastName':lastName,'loginForm':loggedIn});
        #getComments(self);
        #template_values.update({'comments':comments});
        #template=jinja_environment.get_template('userHome.html');
        #self.response.out.write(template.render(template_values));
        
        
        
        
<div class="loginForm">
    <form method ="post">
        <label for="userName"> Username: </label>
        <input name="userNameLogin" type="text" value="user"><br/>
        <label for="password"> Password: </label>
        <input name="password" type="text" value="pass"> <br/>
    <input name="loginButton" type="submit" value="Login">

    </form>

</div>


'''