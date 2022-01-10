import re
import mechanize

br = mechanize.Browser()
response = br.open("http://webauth.login/auth1.html")
br.select_form(nr=0)
br.form["userName"] = "cherpin"
br.form["pwd"] = "P@ssword36"
br.form["digest"]
response = br.submit()
print(response.read())