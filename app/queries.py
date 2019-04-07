from neomodel import db
from .models import Airport, FlightRoute

class RouteNotFound(Exception):
  pass

class AirportNotFound(Exception):
  pass

class FlightConnectionsQuery:
  def __init__(self, origin_code, destination_code):
    self._origin = Airport.nodes.get_or_none(code=origin_code)
    self._origin_code = origin_code
    self._destination = Airport.nodes.get_or_none(code=destination_code)
    self._destination_code = destination_code

  def perform(self):
    if not self._origin:
      raise AirportNotFound("Airport {0} not found".format(self._origin_code))
    if not self._destination:
      raise AirportNotFound('Airport {0} not found'.format(self._destination_code))

    query_str = "MATCH (start:Airport {code:'%s'}), (end:Airport {code:'%s'}), \
      p = shortestPath((start)-[:DESTINATION*]-(end)) RETURN (p)"
    res, meta = db.cypher_query(query_str % (self._origin.code, self._destination.code))
    if len(res) and len(res[0]):
      return [FlightRoute.inflate(i) for i in res[0][0]]
    else:
      raise RouteNotFound('No route found')
