from flask import Flask, request , redirect , url_for , Response,session

app=Flask(__name__)
app.secret_key = "supersecret" 

#login page 
@app.route('/',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            session["user"] = username
            return redirect(url_for('welcome'))
        else:
            return Response("Invalid Credentials",mimetype='text/plain') #html by default
    return '''
    <h1>Login Page</h1>
    <p>Please enter your username and password:</p>
    <form method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        <input type="submit" value="Login">
    </form>
    ''' 

# Welcome page
@app.route("/welcome")
def welcome():
    if "user" in session:
        return f'''
        <h1>Welcome {session["user"]}!</h1>
        <p>You have successfully logged in.</p>
        <a href="{url_for('logout')}">Logout</a> 
      '''
    else:
        return redirect(url_for('login'))
    

# Logout page
@app.route("/logout")    
def logout ():
    session.pop("user",None)
    return redirect(url_for('login'))



  