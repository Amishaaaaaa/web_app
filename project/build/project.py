#----------------------Modules-----------------------
from flask import Flask,render_template,request,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse
from flask_cors import CORS
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


#--------------------------------------------Configuration------------------------------------------

app=Flask(__name__,template_folder='templates',static_folder='static')
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///onemanydata.sqlite3"
app.app_context().push()
CORS(app)

#api.init_app(app)
db=SQLAlchemy(app)
#db.init_app(app)

app.secret_key = "my_secret_key"


#-----------------------------------------------Model----------------------------------------------

class Venue(db.Model):
    Venue_id=db.Column(db.Integer(),primary_key=True)
    Venue_name=db.Column(db.String(50),nullable=False)
    Place=db.Column(db.String(50),nullable=False)
    Capacity=db.Column(db.Integer(),nullable=False)
    Rating=db.Column(db.Integer())
    rel_show=db.relationship("Show",backref='rel_venue', secondary="link")


class Show(db.Model):
    Show_id=db.Column(db.Integer(),primary_key=True)
    Show_name=db.Column(db.String(50),nullable=False)
    Rating=db.Column(db.Integer())
    Tags=db.Column(db.String(50))
    Date=db.Column(db.String(20))
    Time=db.Column(db.String(20))
    TicketPrice=db.Column(db.Integer(),nullable=False)
    Language=db.Column(db.String(30),nullable=False)
    Type=db.Column(db.String(20),nullable=False)
    Venue_id=db.Column(db.Integer(),db.ForeignKey("venue.Venue_id"))
    Show_Capacity=db.Column(db.Integer())
    #rel_venue=db.relationship("Venue", secondary="link")


#-------association btwn Show and Venue--------
class Link(db.Model):
    #Link_id=db.Column(db.Integer(),primary_key=True)
    Venue_id=db.Column(db.Integer(),db.ForeignKey("venue.Venue_id"),primary_key=True)
    Show_id=db.Column(db.Integer(),db.ForeignKey("show.Show_id"),primary_key=True)


class User_data(db.Model):
    Email_Address=db.Column(db.String(50),nullable=False,unique=True)
    Username=db.Column(db.String(30),primary_key=True)
    Password=db.Column(db.String(80),nullable=False)


class Admin_data(db.Model):
    Username=db.Column(db.String(30),primary_key=True)
    Email_Address=db.Column(db.String(50),unique=True,nullable=False)
    Password=db.Column(db.String(80),nullable=False)


class Booking(db.Model):
    ID=db.Column(db.Integer(),primary_key=True)
    Show_id=db.Column(db.Integer())
    Show_name=db.Column(db.String(50))
    Venue_id=db.Column(db.Integer())
    Venue_name=db.Column(db.String(30))
    Username=db.Column(db.String(30))
    email=db.Column(db.String(50))
    phone=db.Column(db.Integer())
    Number_of_Seats=db.Column(db.Integer())

db.create_all()


#-----------------------------------------------Api----------------------------------------------
 
 #----------Api for Venue--------------
parser=reqparse.RequestParser()
parser.add_argument('V_name')
parser.add_argument('place')
parser.add_argument('capacity')
parser.add_argument('rating')

class Api_Venue(Resource):
    #--------------create venue----------
    def post(self):
        info=parser.parse_args()
        new_venue=Venue(Venue_name=info['V_name'],
            Place=info['place'],
            Capacity=info['capacity'],
            Rating=info['rating'])
        db.session.add(new_venue)
        db.session.commit()
        return { "status":"venue created"},201
    
    #--------------read venue-------------
    def get(self):
        all_venues={}
        v1=Venue.query.all()
        for ven in v1:
            all_venues[ven.Venue_id]=ven.Venue_name
        return all_venues
    
    #-------------update venue---------------
    def put(self,Venue_id):
        info=parser.parse_args()
        v_update=Venue.query.get(Venue_id)
        v_update.Venue_name=info['V_name']
        v_update.Place=info['place']
        v_update.Capacity=info['capacity']
        v_update.Rating=info['rating']
        db.session.commit()
        return { "status":"venue updated"},201
    
    #------------delete venue--------------
    def delete(self,Venue_id):
        v_del=Venue.query.get(Venue_id)
        db.session.delete(v_del)
        db.session.commit()
        return {"status":"venue deleted"},202
    
#------------api endpoints for venue--------------
api.add_resource(Api_Venue,"/api/create_venue","/api/all_venues","/api/update_venue/<int:Venue_id>","/api/delete_venue/<int:Venue_id>")


#-----------api for show-------------
parser.add_argument('S_name')
parser.add_argument('rating')
parser.add_argument('tags')
parser.add_argument('date')
parser.add_argument('time')
parser.add_argument('ticketPrice')
parser.add_argument('language')
parser.add_argument('type')
parser.add_argument('Venue_id')
parser.add_argument('Show_Capacity')
class Api_Show(Resource):

    #--------create show-----------
    def post(self):
        info=parser.parse_args()
        new_show = Show(
            Show_name=info['S_name'],
            Rating=info['rating'],
            Tags=info['tags'],
            Date=info['date'],
            Time=info['time'],
            TicketPrice=info['ticketPrice'],
            Language=info['language'],
            Type=info['type'],
            Venue_id=info['Venue_id'],
            Show_Capacity=info['Show_Capacity']
        )
        db.session.add(new_show)
        db.session.commit()
        return { "status":"show created"},201
    

    #---------read show------------
    def get(self):
        all_shows={}
        s1=Show.query.all()
        for sho in s1:
            all_shows[sho.Show_id]=sho.Show_name
        return all_shows
    
    #-----------update show-----------
    def put(self,Show_id):
        info=parser.parse_args()
        s_update=Show.query.get(Show_id)
        s_update.Show_name=info['S_name']
        s_update.Rating=info['rating']
        s_update.Tags=info['tags']
        s_update.Date=info['date']
        s_update.Time=info['time']
        s_update.TicketPrice=info['ticketPrice']
        s_update.Language=info['language']
        s_update.Type=info['type']
        s_update.Venue_id=info['Venue_id']
        s_update.Show_Capacity=info['Show_Capacity']
        
        db.session.commit()
        return { "status":"show updated"},201
    
    #-------------delete show---------------
    def delete(self,Show_id):
        s_del=Show.query.get(Show_id)
        db.session.delete(s_del)
        db.session.commit()
        return {"status":"show deleted"},202
    
#-------------api endpoints for show------------------
api.add_resource(Api_Show,"/api/create_show","/api/all_shows","/api/update_show/<int:Show_id>","/api/delete_show/<int:Show_id>")



#-------------------------------------Controllers--------------------------------------

#----------firstpage uri-------------
@app.route('/',methods=['GET','POST'])  #starting controllers
def home():
    return render_template('firstpage.html')

#--------------user login/signup----------------
@app.route('/login_page', methods=['GET','POST'])
def user_index():
    if request.method=='GET':
        #print("get h")
        return render_template('loginpage.html')
    if request.method == 'POST':
        #print("post h")
        form_type = request.form.get("form_type")
        if form_type == "login":
            return user_login()
        if form_type == "signup":
            return user_signup()
        else:
            return redirect('/')
        

#---------func. for user login----------
def user_login():
    if request.method=='GET':
        return render_template('loginpage.html')
    if request.method== 'POST':
        email=request.form.get('email')
        Username=request.form.get('Username')
        session['Username']= Username
        password=request.form.get('password')
        client=User_data.query.filter_by(Email_Address=email,Username=Username,Password=password).first()
        if client:
            return redirect('/U_dashboard/{}'.format(Username))
        else:
            flash("No Email exists with this account. Please sign up to continue.")
            return redirect('/login_page')


#-----------func. for user signup-------------   
def user_signup():
    if request.method=='GET':
        return render_template('loginpage.html')
    if request.method=='POST':
        email=request.form.get('email')
        Username=request.form.get('Username')
        session['Username']= Username
        password=request.form.get('password')
        client=User_data.query.filter_by(Email_Address=email,Username=Username,Password=password).first()
        if client:
            flash("Admin already exists. Please login")
            return redirect('/login_page')
        else:
            new_client=User_data(
            Email_Address= email,
            Username= Username,
            Password= password)
            db.session.add(new_client)
            db.session.commit()
            return redirect('/U_dashboard/{}'.format(Username))


#------------admin login/signup-------------
@app.route('/admin_page', methods=['GET','POST'])
def admin_index():
    if request.method=='GET':
        return render_template('adminlogin.html')
    if request.method == 'POST':
        form_type = request.form.get("form_type")
        if form_type == "login":
            return admin_login()
        if form_type == "signup":
            return admin_signup()


#-----------func. for admin login-----------    
def admin_login():
    if request.method=='GET':
        return render_template('adminlogin.html')
    if request.method== 'POST':
        Username=request.form.get('Username')
        session['Username']= Username
        email=request.form.get('email')
        password=request.form.get('password')
        admin=Admin_data.query.filter_by(Username=Username,Email_Address=email,Password=password).first()
        if admin:
            return redirect('/A_dashboard/{}'.format(Username))
        else:
            flash("This Email does not exist. Please enter correct Email and password")
            return redirect('/admin_page')

        
#-------------func. for admin signup-----------         
def admin_signup():
    if request.method=='GET':
        return render_template('adminpage.html')
    if request.method=='POST':
        Username=request.form.get('Username')
        session['Username']= Username
        email=request.form.get('email')
        password=request.form.get('password')
        admin=Admin_data.query.filter_by(Username=Username,Email_Address=email,Password=password).first()
        if admin:
            flash("User already exists. Please login")
            return redirect('/admin_page')
        else:
            new_admin=Admin_data(
            Username= Username,
            Email_Address= email,
            Password= password)
            db.session.add(new_admin)
            db.session.commit()
            return redirect('/A_dashboard/{}'.format(Username))


#-----------user dashboard--------------
@app.route('/U_dashboard/<Username>',methods=['GET','POST'])
def U_dashboard(Username): 
    if request.method=='GET':
        Username=session.get('Username')
        venues=Venue.query.all()  
        shows=Show.query.all()  
        return render_template('U_dashboard.html',Username=Username,venues=venues,shows=shows)
    if request.method=='POST':
        word=request.form.get('word')
        session['word']= word
        #query="%"+word+"%"
        shows=Show.query.filter(Show.Show_name.like(f'%{word}%')).all()
        return redirect(f'/search/{Username}/{word}')


@app.route('/search/<Username>/<word>',methods=['GET','POST'])
def search(Username,word):
    Username=session.get('Username')
    shows = Show.query.filter(Show.Show_name.like(f'%{word}%')).all()
    for sho in shows:
        venuess=sho.rel_venue
    return render_template("search.html", word=word, shows=shows,Username=Username,venuess=venuess)

#------------venues for a particular show----------
@app.route('/see_venue/<int:Show_id>/<Username>',methods=['GET','POST'])
def see_venue(Show_id,Username):
    s1=Show.query.get(Show_id)
    venuess=s1.rel_venue
    Username=session.get('Username')
    return render_template('see_venue.html',s1=s1,venuess=venuess,Username=Username)


#------------shows for a particular venue----------
@app.route('/see_show/<int:Venue_id>/<Username>',methods=['GET','POST'])
def see_show(Venue_id,Username):
    v1=Venue.query.get(Venue_id)
    Username=session.get('Username')
    showss=v1.rel_show
    return render_template('see_show.html',v1=v1,showss=showss,Username=Username)

#-------------show booking-------------
@app.route('/booking/<int:Venue_id>/<int:Show_id>/<Username>',methods=['GET','POST'])
def booking(Venue_id,Show_id,Username):
    if request.method=='GET':
        v1=Venue.query.get(Venue_id)
        s1=Show.query.get(Show_id)
        Username=session.get('Username')
        return render_template('booking.html',Username=Username,v1=v1,s1=s1)
    
    if request.method=='POST':
        Show_id=Show_id
        Venue_id=Venue_id
        v1=Venue.query.get(Venue_id)
        Venue_name=v1.Venue_name
        s1=Show.query.get(Show_id)
        Show_name=s1.Show_name
        Username=request.form.get('Username')
        email=request.form.get('email')
        phone=request.form.get('phone')
        Number_of_seats=request.form.get('Number_of_seats')

        info=Booking(Show_id=Show_id,Venue_id=Venue_id,Username=Username,email=email,phone=phone,Number_of_Seats=Number_of_seats,Show_name=Show_name,Venue_name=Venue_name)
        db.session.add(info)
        #db.session.commit()
        a1=Show.query.filter_by(Show_id=Show_id).first()
        exp=int(a1.Show_Capacity)-int(Number_of_seats)
        Show.query.filter_by(Show_id=Show_id).update({'Show_Capacity':exp})
        db.session.commit()
        return redirect(f"/profile/{Venue_id}/{Show_id}/{Username}")
    

#-------------show booking(for fixing the venue wala prblm)-------------
@app.route('/booking/<int:Show_id>/<int:Venue_id>/<Username>',methods=['GET','POST'])
def bookingg(Show_id,Venue_id,Username):
    if request.method=='GET':
        v1=Venue.query.get(Venue_id)
        s1=Show.query.get(Show_id)
        Username=session.get('Username')
        return render_template('booking.html',Username=Username,v1=v1,s1=s1)
    
    if request.method=='POST':
        Show_id=Show_id
        Venue_id=Venue_id
        v1=Venue.query.get(Venue_id)
        Venue_name=v1.Venue_name
        s1=Show.query.get(Show_id)
        Show_name=s1.Show_name
        Username=request.form.get('Username')
        email=request.form.get('email')
        phone=request.form.get('phone')
        Number_of_seats=request.form.get('Number_of_seats')

        info=Booking(Show_id=Show_id,Venue_id=Venue_id,Username=Username,email=email,phone=phone,Number_of_Seats=Number_of_seats,Show_name=Show_name,Venue_name=Venue_name)
        db.session.add(info)
        #db.session.commit()
        a1=Show.query.filter_by(Show_id=Show_id).first()
        exp=int(a1.Show_Capacity)-int(Number_of_seats)
        Show.query.filter_by(Show_id=Show_id).update({'Show_Capacity':exp})
        db.session.commit()
        return redirect(f"/profile/{Username}/{int:Venue_id}/{int:Show_id}")
        
        
    
#----------user profile-----------
@app.route('/profile/<int:Venue_id>/<int:Show_id>/<Username>', methods=['GET','POST'])
def profile(Venue_id,Show_id,Username):
    if request.method=='GET':
        v1=Venue.query.get(Venue_id)
        s1=Show.query.get(Show_id)
        h1=Booking.query.filter_by(Username=Username).all()
        return render_template('profile.html',Username=Username,v1=v1,s1=s1,h1=h1)

#----------user profile when no current shows booked-----------
@app.route('/profile/<Username>', methods=['GET','POST'])
def profilee(Username):
    if request.method=='GET':
        v1=Venue.query.all()
        s1=Show.query.all()
        h1=Booking.query.filter_by(Username=Username).all()
        return render_template('profile.html',Username=Username,v1=v1,s1=s1,h1=h1)       

    

#------------admin dashboard=-----------
@app.route('/A_dashboard/<Username>',methods=['GET','POST'])
def A_dashboard(Username):
    Username=session.get('Username')
    users=User_data.query.all()
    venues=Venue.query.all()
    shows=Show.query.all()
    return render_template('A_dashboard.html',Username=Username,venues=venues,shows=shows,users=users)


#------------summary-----------
@app.route('/summary',methods=['GET','POST'])
def summary():
    shows=Show.query.all()
    a1=[]
    b1=[]
    for i in shows:
        a1.append(i.Show_id)
        b1.append(i.Show_Capacity)
    plt.figure()
    plt.bar(a1,b1)
    plt.xlabel('Show_id')
    plt.ylabel('Number of seats available')
    plt.title('Bar Graph')
    plt.savefig('static/bar_graph.png')

    plt.clf()

    venues=Venue.query.all()
    c1=[]
    d1=[]
    for j in venues:
        c1.append(j.Venue_id)
        d1.append(j.Capacity)
    plt.figure()
    plt.bar(c1,d1)
    plt.xlabel('Venue_id')
    plt.ylabel('Venue Capacity')
    plt.title('Bar Graph2')
    plt.savefig('static/graph2.png')

    return render_template('summary.html', img='static/bar_graph.png', img2='static/graph2.png')


#-----------add a show to show table-------------
@app.route('/add_show/<Username>',methods=['GET','POST'])
def add_show(Username):
    if request.method=='GET':
        return render_template('add_show.html',Username=Username)
    if request.method=='POST':
        Show_name=request.form.get('Show_name')
        Rating=request.form.get('Rating')
        Tags=request.form.get('Tags')
        Date=request.form.get('Date')
        Time=request.form.get('Time')
        TicketPrice=request.form.get('TicketPrice')
        Language=request.form.get('Language')
        Type=request.form.get('Type')
        Venue_id=request.form.get('Venue_id')
        Show_Capacity=request.form.get('Show_Capacity')
        show_already_exist=Show.query.filter_by(Show_name=Show_name,Rating=Rating,Tags=Tags,Date=Date,Time=Time,TicketPrice=TicketPrice,Language=Language,Type=Type,Venue_id=Venue_id,Show_Capacity=Show_Capacity).first()
        if show_already_exist:
            flash("Show already exists.")
            return redirect(f"/A_dashboard/{Username}")
        else:
            new_show=Show(
            Show_name=Show_name,
            Rating=Rating,                                                       
            Tags=Tags,
            Date=Date,
            Time=Time,
            TicketPrice=TicketPrice,
            Language=Language,
            Type=Type,
            Venue_id=Venue_id,
            Show_Capacity=Show_Capacity)
            db.session.add(new_show)
            db.session.commit()
            last_show=Show.query.order_by(Show.Show_id.desc()).first()
            last_show_id=last_show.Show_id
            venue_show=Link(Venue_id=Venue_id,Show_id=last_show_id)
            db.session.add(venue_show)
            db.session.commit()
            return redirect(f"/A_dashboard/{Username}")
        


#-------------add a venue to venue table----------
@app.route('/add_venue/<Username>',methods=['GET','POST'])
def add_venue(Username):
    if request.method=='GET':
        return render_template('add_venue.html',Username=Username)
    if request.method=='POST':
        Venue_name=request.form.get('Venue_name')
        Place=request.form.get('Place')
        Capacity=request.form.get('Capacity')
        Rating=request.form.get('Rating')
        venue_already_exist=Venue.query.filter_by(Venue_name=Venue_name,Place=Place,Capacity=Capacity,Rating=Rating).first()
        if venue_already_exist:
            return redirect('/A_dashboard/<Username>')
        else:
            new_venue=Venue(Venue_name=Venue_name,
                            Place=Place,
                            Capacity=2*int(Capacity),
                            Rating=Rating)
            db.session.add(new_venue)
            db.session.commit()
            return redirect(f"/A_dashboard/{Username}")


#---------------update a show----------
@app.route('/update_show/<Username>/<int:Show_id>',methods=['GET','POST'])
def update_show(Username,Show_id):
    if request.method=='GET':
        sho=Show.query.filter_by(Show_id=Show_id).one()
        return render_template('update_show.html',sho=sho,Username=Username)
    if request.method=='POST':
        sho=Show.query.filter_by(Show_id=Show_id).one()
        sho.Show_name=request.form.get('Show_name')
        sho.Rating=request.form.get('Rating')
        sho.Tags=request.form.get('Tags')
        sho.Date=request.form.get('Date')
        sho.Time=request.form.get('Time')
        sho.TicketPrice=request.form.get('TicketPrice')
        sho.Language=request.form.get('Language')
        sho.Type=request.form.get('Type')
        sho.Venue_id=request.form.get('Venue_id')
        sho.Show_Capacity=request.form.get('Show_Capacity')
        db.session.commit()

        linn=Link.query.filter_by(Show_id=Show_id).one()
        linn.Venue_id=request.form.get('Venue_id')
        linn.Show_id=Show_id
        db.session.commit()
        return redirect(f"/A_dashboard/{Username}")


#----------------update a venue-------------
@app.route('/update_venue/<Username>/<int:Venue_id>',methods=['GET','POST'])
def update_venue(Username,Venue_id):
    if request.method=='GET':
        ven=Venue.query.filter_by(Venue_id=Venue_id).one()
        return render_template('update_venue.html',ven=ven,Username=Username)
    if request.method=='POST':
        ven=Venue.query.filter_by(Venue_id=Venue_id).one()
        ven.Venue_name=request.form.get('Venue_name')
        ven.Place=request.form.get('Place')
        ven.Capacity=request.form.get('Capacity')
        ven.Rating=request.form.get('Rating')
        db.session.commit()
        return redirect(f"/A_dashboard/{Username}")

        
#-------------delete a show-------------
@app.route('/delete_show/<Username>/<int:Show_id>')
def delshow(Username,Show_id):
    sho=Show.query.filter_by(Show_id=Show_id).one()
    db.session.delete(sho)
    db.session.commit()
    return redirect(f'/A_dashboard/{Username}')


#-------------delete a venue-------------
@app.route('/delete_venue/<Username>/<int:Venue_id>')
def delvenue(Username,Venue_id):
    ven=Venue.query.filter_by(Venue_id=Venue_id).one()
    db.session.delete(ven)
    db.session.commit()
    return redirect(f'/A_dashboard/{Username}')



#------------app run----------
if __name__=="__main__":
    app.run(debug=True)