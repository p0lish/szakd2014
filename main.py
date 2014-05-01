import jinja2
import os
import webapp2
import datetime
from google.appengine.api import xmpp
from google.appengine.api import channel
from google.appengine.api import users
from google.appengine.ext.webapp import xmpp_handlers

STD_MSG = "UNDEFINED INCOMING XMPP MESSAGE"

def bare_jid(sender):
    return sender.split('/')[0]

# XMPP kapcsolat kezelo. csak bejovo keresek feldolgozasa
class XmppHandler(xmpp_handlers.CommandHandler):


    # parancs lekezelese
    def unhandled_command(self, message=None):
        message.reply(STD_MSG.format(self.request.host_url))
    # adat lekezelese
    def text_message(self, message=None):
        message.reply(STD_MSG.format(self.request.host_url))



# Ez az osztaly szolgal a fooldal rendereleseert, illetve a socket funkciok megvalositasaert
class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return

    token = channel.create_channel(user.user_id())
    template_values = {'token': token,
                       'me': user.user_id()
                       }
    template = jinja_environment.get_template('templates/index.html')
    self.response.out.write(template.render(template_values))

# inicializalas
jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
app = webapp2.WSGIApplication([('/', MainPage), ('/_ah/xmpp/message/chat/', XmppHandler)], debug=True)