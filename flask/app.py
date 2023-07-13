# Import required libraries
from flask import Flask, render_template, request, session, redirect, url_for,flash, Response 
import ibm_db
import sys
sys.path.insert(0,'/home/arj/IBM_project/Model_building')
sys.path.insert(1,'/home/arj/IBM_project/Data')
from car_par import process_video
import cv2
import cvzone
import numpy as np
from flask_mail import Mail,Message

# Create Flask app instance and set secret key
app = Flask(__name__)
app.secret_key = 'ARJ23400'

# Establish connection with IBM database
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=ssl;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ncc97793;PWD=TvIsFuhT1vXc7Zif;", "", "")
print("Connected to IBM Database...")
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='arj0654@gmail.com'
app.config['MAIL_PASSWORD']='enhlidejnzplqumx'
app.config['MAIL_DEFAULT_SENDER']='arj0654@gmail.com'

mail=Mail(app)
# Define route for home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Process the form data
        # ...
        
        # Check if the user is logged in
        if session.get('logged_in'):
            return redirect(url_for('userhome'))  # Redirect to the user home page after processing the form
        else:
            return redirect(url_for('popup'))  # Redirect to the sign-in page if the user is not logged in

    return render_template('home.html')



@app.route('/about')
def about():
    return render_template('about.html',firstname=None)

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html',firstname=None)

@app.route('/why')
def why():
    return render_template('why.html',firstname=None)

@app.route('/login')
def login():
    error = request.args.get('error')
    return redirect(url_for(signup) ,error=error) 
@app.route('/userabout')
def userabout():
    firstname=session.get('firstname')

    return render_template('about.html',firstname=firstname)
@app.route('/video_feed')
def video_feed():
    c=session['c']
    return Response(gen(c), mimetype='multipart/x-mixed-replace;boundary=frame')


@app.route('/usermodel', methods=['POST', 'GET'])
def usermodel():
    firstname = session.get('firstname')
    #c value defines which parking lot information does the user requires
    c = session.get('c')
    if firstname is None:
        return "Not logged in"
    if c is None:
        return "No parking lot were selected"
    return render_template('model.html', firstname=firstname)

    
@app.route('/video_feed')
def video_feed_endpoint(c):
    c = session['c']
    return Response(gen(c), mimetype='multipart/x-mixed-replace;boundary=frame')


def gen(c):
    if c == '1':
        cap = cv2.VideoCapture('/home/arj/IBM_project/Data/carParkingInput.mp4')
    elif c == '2':
        cap = cv2.VideoCapture('/home/arj/IBM_project/Data/carparking3.mp4')
    elif c == '3':
        cap = cv2.VideoCapture('/home/arj/IBM_project/Data/carparking2.mp4')
    else:
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        processed_frame = process_video(frame, c)   
        _, jpeg = cv2.imencode('.jpg', processed_frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()



@app.route('/userhome', methods=['POST', 'GET'])
def userhome():
    firstname = session.get('firstname')
    if firstname is None:
        return "No 'firstname' value found in the session"

    if request.method == "POST":
        parkingslot = request.form.get("parkingslot")
        if parkingslot == "parking slot 1":
            c = '1'
            session['c'] = c
            return redirect(url_for('usermodel'))
        elif parkingslot == "parking slot 2":
            c = '2'
            session['c'] = c
            return redirect(url_for('usermodel'))
        elif parkingslot == "parking slot 3":
            c = '3'
            session['c'] = c
            return redirect(url_for('usermodel'))

    return render_template('home.html', firstname=firstname) 
@app.route('/popup')
def popup():
    return render_template('popup.html')

# Define route and function for sign up page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = request.args.get('error')
    if request.method == 'POST':
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        password = request.form["password"]
        passwordconfirmation = request.form["passwordconfirmation"]
       
        # Insert new user data into IBM database
        sql = "INSERT INTO AI_Enabled_car_parking_signup(firstname, lastname, email, password, confirmpassword) VALUES (?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare(conn, sql)

        ibm_db.bind_param(stmt, 1, firstname)
        ibm_db.bind_param(stmt, 2, lastname)
        ibm_db.bind_param(stmt, 3, email)
        ibm_db.bind_param(stmt, 4, password)
        ibm_db.bind_param(stmt, 5, passwordconfirmation)
        ibm_db.execute(stmt)
        print("Success")

        # Flash success message and redirect user to sign in page
        flash('Successfully signed up!')
        sign_in_link=request.host_url+url_for('signin')
        send_email(email,'Welcome to our Website',f'Dear {firstname} {lastname}, you have successfully registered with our platform.You can now login and utilize our service by clicking the link below:\n\n\n{sign_in_link}')
        return redirect(url_for('signin'))
    
    return render_template('signup.html',error=error)

def send_email(to,subject,body):
    msg=Message(subject=subject,recipients=[to],body=body)
    mail.send(msg)




@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        email = request.form["mail"]
        password = request.form["password"]
        # Check if user exists in IBM database
        sql = "SELECT firstname  FROM AI_Enabled_car_parking_signup WHERE email = ? AND password = ?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        
        ibm_db.execute(stmt)
        result = ibm_db.fetch_tuple(stmt)

        if result :
            
            print("Success")
            username=result[0]
            session['firstname']=username
            print(username)
            return redirect(url_for('userhome'))
            
        else:
            error = "Invalid UserId or password"
            return redirect(url_for('signup', error=error))
        ibm_db.free_stmt(conn)
        print("failed conditions")

    return render_template('signin.html')


# Run the app in debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000 ,debug=True)