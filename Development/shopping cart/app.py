from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)



@app.route('/',methods=['GET','POST'])
def farmprofile():
	return render_template('shop.html')


if __name__ == '__main__':
	app.run(debug=True)