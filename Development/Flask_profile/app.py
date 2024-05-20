from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def farmprofile():
	return render_template('fprofile.html')


@app.route('/farmerfeed',methods=['GET','POST'])
def farmerfeed():
	return render_template('ffeed.html')

@app.route('/market',methods=['GET','POST'])
def market():
	return render_template('market.html')

@app.route('/tlease',methods=['GET','POST'])
def tlease():
	return render_template('lease.html')


@app.route('/customerprofile',methods=['GET','POST'])
def cusdtomerprofile():
	return render_template('cprofile.html')


@app.route('/cfeed',methods=['GET','POST'])
def customerfeed():
	return render_template('cfeed.html')

@app.route('/cart',methods=['GET','POST'])
def cart():
	return render_template('shopCart.html')



if __name__=='__main__':
    app.run(debug=True)
