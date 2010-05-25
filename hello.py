from twisted.web import resource, server
from twisted.internet import reactor, defer


class Example(resource.Resource):
  
  def __init__(self):
    self.rqs = None
   
  def render(self, request):
    """ Handle GET request, but don't finish it """
    print self.rqs, request
    if self.rqs:
      self.rqs.write("x")
      self.rqs.finish()
      self.rqs = None
    self.rqs = request
    return server.NOT_DONE_YET
 

