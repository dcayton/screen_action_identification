#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:10:35 2024

@author: donaldcayton
"""

def left_basket(moment):
  """
  This function takes a moment in the game and returns if the ball is in the left basket.
  """
  return (3.5 <= moment['ball_coordinates']['x'] <= 6) and (24 <= moment['ball_coordinates']['y'] <= 26)

def right_basket(moment):
  """
  This function takes a moment in the game and returns if the ball is in the right basket.
  """
  return (88 <= moment['ball_coordinates']['x'] <= 90.5) and (24 <= moment['ball_coordinates']['y'] <= 26)

def locate_ballhandler(moment, poss_team_id):
  """
  This function takes a moment in the game as well as the team ID in possession.
  It returns the ID of the presumed ball-handler (player closest to the ball).
  The outline of this function is based on criteria from 'https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=csu14943636475232&disposition=inline'
  """
  import math

  ball_coords = [moment['ball_coordinates']['x'], moment['ball_coordinates']['y']]

  # arbitrarily large distance
  shortest_distance = 10000

  for player in moment['player_coordinates']:
    player_coords = [player['x'], player['y']]
    distance = math.dist(ball_coords, player_coords)

    if (distance < shortest_distance) and (player['teamid'] == poss_team_id):
      shortest_distance = distance
      handler_id = player['playerid']

  if shortest_distance > 5:
    return None

  return handler_id

def locate_defender(moment, poss_team_id, handler_id = None):
  """
  This function takes a moment in the game, the team ID in possession, and the ID of the ball-handler (output of locate_handler).
  It returns the ID of the presumed on-ball defender (defender closest to the ball).
  The outline of this function is based on criteria from 'https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=csu14943636475232&disposition=inline'
  """
  import math

  # if no ball-handler, then there is no on-ball defender
  if handler_id is None:
    return None

  handler_coords = [[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == handler_id][0]

  # arbitrarily large distance
  shortest_distance = 10000

  for player in moment['player_coordinates']:
    player_coords = [player['x'], player['y']]
    distance = math.dist(handler_coords, player_coords)

    if (distance < shortest_distance) and (player['teamid'] != poss_team_id):
      shortest_distance = distance
      defender_id = player['playerid']

  # if defender > 12 ft away from handler, defender is likely not the on-ball defender
  if shortest_distance > 12:
    return None

  return defender_id

def locate_screener(moment, poss_team_id, handler_id = None, defender_id = None):
  """
  This function takes a moment in the game, the team ID in possession, the ball-handler ID and the on-ball defender ID.
  It returns the ID of the presumed screener (offensive player setting the screen).
  The of this function is based on criteria from 'https://etd.ohiolink.edu/acprod/odb_etd/ws/send_file/send?accession=csu14943636475232&disposition=inline'
  """
  import math

  # if no ball handler, on-ball screen cannot occur
  if handler_id is None:
    return None

  handler_coords = [[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == handler_id][0]

  # arbitrarily large distance
  shortest_distance = 10000

  screener_id = None
  for player in moment['player_coordinates']:
    player_coords = [player['x'], player['y']]
    distance = math.dist(handler_coords, player_coords)

    if (distance < shortest_distance) and (player['teamid'] == poss_team_id) and (player['playerid'] != handler_id):
      shortest_distance = distance
      screener_id = player['playerid']

  # if no screener, end function
  if screener_id is None:
    return None

  # if w/in distance of 10 ft from basket, not a screen and reject example
  screener_coords = [[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == screener_id][0]
  basket_coords = [25, 89.25]
  if math.dist(screener_coords, basket_coords) < 10:
    return None

  # if screener > 5ft from handler, not a screen and reject example
  if shortest_distance > 5:
    return None

  # if no defender, no ball screen and reject
  if defender_id is None:
    return None

  defender_coords = [[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == defender_id][0]

  # if handler and defender not w/in 10 ft, not a ball screen and reject example
  if math.dist(handler_coords, defender_coords) > 10:
    return None

  return screener_id

def find_screen(moment, poss_team_id, handler_id = None, defender_id = None, screener_id = None):
  """
  This function takes a moment in the game, the team ID in possession, and the player ID's of the ball-handler, on-ball defender, and screener.
  It returns a tuple of the form:
    - True if a screen is found, False otherwise
    - The ID of the ball-handler
    - The ID of the on-ball defender
    - The ID of the screener
  """
  import math

  if handler_id and defender_id and screener_id:
    ball_coords = [moment['ball_coordinates']['x'], moment['ball_coordinates']['y']]
    basket_coords = [25, 89.25]
    # check if ball past half-court and not too close to basket
    if (ball_coords[1] > 47) and math.dist(ball_coords, basket_coords) > 10:
      return True, handler_id, defender_id, screener_id
  return False, handler_id, defender_id, screener_id

