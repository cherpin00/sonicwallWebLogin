from webbot import Browser 
web = Browser()
web.go_to('http://webauth.login') 
web.type("cherpin", into="Username")
web.type("P@ssword36", into="Password")
r = web.click('Login')