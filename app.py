from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from .models import User
from .forms import SignupForm
from . import db

app = Flask(__name__)

# Define sign up route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

# Run app
if __name__ == '__main__':
    app.run(debug=True)
