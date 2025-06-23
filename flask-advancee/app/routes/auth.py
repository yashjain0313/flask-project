from flask import url_for ,session, redirect, flash, Blueprint,render_template,request

auth_bp=Blueprint('auth',__name__) 

USER_CRED={
    'username':"admin",
    'password':'123'
}

@auth_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USER_CRED['username'] and password == USER_CRED['password']:
            session['user']=username
            flash("Login Successful !!",'success')
        else:
            flash("Invalid credentials",'danger')

    return render_template("login.html")


#logout 

@auth_bp.route("/logout")
def logout():
    session.pop('user',None)
    flash("Logged Out","info")
    return redirect(url_for('auth.login'))

