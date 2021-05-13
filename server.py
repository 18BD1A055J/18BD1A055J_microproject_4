from flask import Flask, render_template, request, redirect
import requests
from twilio.rest import Client

account_sid = 'Axxx4'
auth_token = 'exxxc'

client = Client(account_sid, auth_token)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/epass', methods = ['POST'])
def confirmation():
    if request.method == 'POST':
        aadharNo = request.form['aadharNo']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        fromState = request.form['fromState']
        toState = request.form['toState']
        source = request.form['source']
        destination = request.form['destination']
        date = request.form['date']
        phone = request.form['phone']
        r = requests.get('https://api.covid19india.org/v4/data.json')
        json_data = r.json()
        confirmed = json_data[toState]['districts'][destination]['total']['confirmed']
        population = json_data[toState]['districts'][destination]['meta']['population']
        th = (confirmed/population)*100
        print(confirmed)
        print(population)
        print(th)
        if (th < 30):
            client.messages.create(
                     body="Hello " + fname + " your ePass registration is successful. Date: " + date + ", from " + source + " to " + destination,
                     from_='+12146922946',
                     to='+91'+str(phone)
                 )
            return render_template('confirm.html', aadharNo = aadharNo, fname = fname, lname = lname, email = email, source = fromState + ", " + source, destination = toState + ", " + destination, date = date, phone = phone, status = "CONFIRMED")
        else:
            client.messages.create(
                     body="Hello " + fname + " your ePass registration is unsuccessful due to surge in covid cases in " + destination,
                     from_='+12146922946',
                     to='+91'+str(phone)
                 )
            return render_template('confirm.html', aadharNo = aadharNo, fname = fname, lname = lname, email = email, source = fromState + ", " + source, destination = toState + ", " + destination, date = date, phone = phone, status = "NOT CONFIRMED") 
    else: 
        return redirect('/')
app.run(host="0.0.0.0", port=3000, debug=True)




