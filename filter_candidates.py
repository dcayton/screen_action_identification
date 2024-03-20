#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:14:12 2024

@author: donaldcayton
"""

from id_utility_functions import *

def filter_candidate_events(events):
  """
  This function takes in a generator of events and outputs a generator that is filtered to only include potential PNR/PNP actions.
  It also modifies the events to be worked with in a uniform format by rotating the coordinates depending on the direction of play.
  There is a bit of hard-coding in the directionality section, which is necessary due to mistimed events in the raw data.
  """
  import math

  filter_events = {1, 2, 5, 6}
  start_counter = 0
  game_id = events[0]['gameid']
  for event in events:
    if (event['event_info']['type'] in filter_events) and not math.isnan(event['event_info']['possession_team_id']):
      if event['gameid'] != game_id:
        start_counter = 0

      game_id = event['gameid']

      if len(event['moments']) == 0:
        continue

      quarter = event['moments'][0]['quarter']

      if quarter == 1 and start_counter == 0:
        for moment in event['moments']:
          if left_basket(moment):
            first_poss_team_id = event['event_info']['possession_team_id']
            first_direction = 'left'
            second_direction = 'right'
            if game_id in ["0021500292", "0021500648"]:
              first_direction = 'right'
              second_direction = 'left'
            event['event_info']['direction'] = first_direction
            start_counter += 1
            break
          elif right_basket(moment):
            first_poss_team_id = event['event_info']['possession_team_id']
            first_direction = 'right'
            second_direction = 'left'
            if game_id == "0021500648":
              first_direction = 'left'
              second_direction = 'right'
            event['event_info']['direction'] = first_direction
            start_counter += 1
            break
      elif quarter < 3:
        if event['event_info']['possession_team_id'] == first_poss_team_id:
          direction = first_direction
        else:
          direction = second_direction
        event['event_info']['direction'] = direction
      elif quarter >= 3:
        if event['event_info']['possession_team_id'] == first_poss_team_id:
          direction = second_direction
        else:
          direction = first_direction
        event['event_info']['direction'] = direction

      if 'direction' not in event['event_info']:
        continue

      # assign now rotate coordinates based on direction
      if event['event_info']['direction'] == 'left':
        for moment in event['moments']:

          ball_x = moment['ball_coordinates']['y']
          ball_y = 94 - moment['ball_coordinates']['x']
          moment['ball_coordinates']['x'] = ball_x
          moment['ball_coordinates']['y'] = ball_y

          for player_coord in moment['player_coordinates']:
            x = player_coord['y']
            y = 94 - player_coord['x']
            player_coord['x'] = x
            player_coord['y'] = y

      else:
        for moment in event['moments']:

          ball_x = 50 - moment['ball_coordinates']['y']
          ball_y = moment['ball_coordinates']['x']
          moment['ball_coordinates']['x'] = ball_x
          moment['ball_coordinates']['y'] = ball_y

          for player_coord in moment['player_coordinates']:
            x = 50 - player_coord['y']
            y = player_coord['x']
            player_coord['x'] = x
            player_coord['y'] = y

      # method to find screen situations for potential pnr / pnp for each event
      event_poss_team_id = event['event_info']['possession_team_id']
      handler_id = None
      defender_id = None
      screener_id = None

      last_clock = 0
      screen_frame_start = None
      frame_id = 0
      screen_frame_count = 0
      num_moments = len(event['moments'])

      for moment in event['moments']:
        current_handler = locate_ballhandler(moment, event_poss_team_id)
        current_defender = locate_defender(moment, event_poss_team_id, current_handler)
        current_screener = locate_screener(moment, event_poss_team_id, current_handler, current_defender)

        screen = find_screen(moment, event_poss_team_id, current_handler, current_defender, current_screener)

        current_clock = moment['game_clock']

        if screen[0] == True and current_clock != last_clock:
          if screen_frame_count == 0:
            screen_frame_start = frame_id
            screen_frame_count += 1
            screen_time_stamp_start = moment['game_clock']

            handler_id = current_handler
            defender_id = current_defender
            screener_id = current_screener

          elif screen[1] == handler_id and screen[2] == defender_id and screen[3] == screener_id:
            screen_frame_count += 1

            handler_id = screen[1]
            defender_id = screen[2]
            screener_id = screen[3]

        elif screen[0] == False and screen_frame_count > 8 and current_clock != last_clock:
          event['event_info']['screen_potential'] = True
          event['event_info']['handler_id'] = handler_id
          event['event_info']['defender_id'] = defender_id
          event['event_info']['screener_id'] = screener_id
          event['event_info']['screen_frame_start'] = screen_frame_start
          event['event_info']['screen_frame_end'] = frame_id
          event['event_info']['screen_time_stamps'] = [round(screen_time_stamp_start, 2), round(moment['game_clock'])]
          screen_frame_count = 0
          break
        else:
          screen_frame_count = 0

        frame_id += 1
        last_clock = current_clock
        if frame_id == num_moments:
          event['event_info']['screen_potential'] = False
          event['event_info']['handler_id'] = handler_id
          event['event_info']['defender_id'] = defender_id
          event['event_info']['screener_id'] = screener_id
          event['event_info']['screen_frame_start'] = screen_frame_start
          event['event_info']['screen_frame_end'] = frame_id
          event['event_info']['screen_time_stamps'] = [0, 0]
          screen_frame_count = 0
          break

      if event['event_info']['screen_potential'] == True:
        yield event