#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 13:59:44 2024

@author: donaldcayton
"""

import pandas as pd
import numpy as np

def play_feature_csv_generator(filter_dict):
    """

    Parameters
    ----------
    filter_dict : dictionary generator
        This must take the form of the filtered dictionary generator output by
        filter candidate events.

    Returns
    -------
    Dataframe
        The returned dataframe will contain a row for each 
        candidate event along with necessary features.

    """
    from math import dist

    event_prior_stamp_start = 0

    handler_position = []
    screener_position = []
    handler_distance = []
    screener_distance = []
    handler_avg_velo = []
    screener_avg_velo = []
    handler_start_x = []
    handler_start_y = []
    screener_start_x = []
    screener_start_y = []
    handler_end_x = []
    handler_end_y = []
    screener_end_x = []
    screener_end_y = []

    for event in filter_dict:
        if event['event_info']['screen_time_stamps'][0] == event_prior_stamp_start:
            continue

        handler_id = event['event_info']['handler_id']
        screener_id = event['event_info']['screener_id']

        for player in (event['visitor']['players'] + event['home']['players']):
            if player['playerid'] == handler_id:
                handler_pos = player['position']
                handler_position.append(handler_pos)
            elif player['playerid'] == screener_id:
                screener_pos = player['position']
                screener_position.append(screener_pos)

        action_start = event['event_info']['screen_frame_start']
        action_end = min(len(event['moments']) - 1, event['event_info']['screen_frame_end'] + 30)

        initial_locations = event['moments'][action_start]['player_coordinates']

        if len(initial_locations) == 0:
            initial_locations = event['moments'][action_start+1]['player_coordinates']

        handler_start_loc = [[d['x'], d['y']] for d in initial_locations if d['playerid'] == handler_id][0]
        screener_start_loc = [[d['x'], d['y']] for d in initial_locations if d['playerid'] == screener_id][0]
    
        handler_start_x.append(handler_start_loc[0])
        handler_start_y.append(handler_start_loc[1])
        screener_start_x.append(screener_start_loc[0])
        screener_start_y.append(screener_start_loc[1])
    
        handler_loc = handler_start_loc
        screener_loc = screener_start_loc
    
        hstep_distances = []
        sstep_distances = []
        hstep_velos = []
        sstep_velos = []
        for moment in event['moments'][action_start:action_end]:
            if len([[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == handler_id]) == 0:
                handler_current_pos = handler_loc
            else:
                handler_current_pos = [[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == handler_id][0]
            if len([[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == screener_id]) == 0:
                screener_current_pos = screener_loc
            else:
                screener_current_pos = [[d['x'], d['y']] for d in moment['player_coordinates'] if d['playerid'] == screener_id][0]

            # distance covered at this step
            handler_step_distance = dist(handler_loc, handler_current_pos)
            hstep_distances.append(handler_step_distance)
      
            screener_step_distance = dist(screener_loc, screener_current_pos)
            sstep_distances.append(screener_step_distance)
      
            # velocity at this step, .04 seconds btwn each frame
            handler_step_velocity = handler_step_distance / .04
            hstep_velos.append(handler_step_velocity)
      
            screener_step_velocity = screener_step_distance / .04
            sstep_velos.append(screener_step_velocity)
      
            # add to lists and update locs
            handler_loc = handler_current_pos
            screener_loc = screener_current_pos

        handler_distance.append(sum(hstep_distances))
        screener_distance.append(sum(sstep_distances))
    
        handler_avg_velo.append(np.mean(hstep_velos))
        screener_avg_velo.append(np.mean(sstep_velos))
    
        handler_end_loc = handler_loc
        screener_end_loc = screener_loc
    
        handler_end_x.append(handler_end_loc[0])
        handler_end_y.append(handler_end_loc[1])
        screener_end_x.append(screener_end_loc[0])
        screener_end_y.append(screener_end_loc[1])
    
        event_prior_stamp_start = event['event_info']['screen_time_stamps'][0]

    df_dict = {
        'handler_position': handler_position,
        'screener_position': screener_position,
        'handler_distance': handler_distance,
        'screener_distance': screener_distance,
        'handler_avg_velo': handler_avg_velo,
        'screener_avg_velo': screener_avg_velo,
        'handler_start_x': handler_start_x,
        'handler_start_y': handler_start_y,
        'screener_start_x': screener_start_x,
        'screener_start_y': screener_start_y,
        'handler_end_x': handler_end_x,
        'handler_end_y': handler_end_y,
        'screener_end_x': screener_end_x,
        'screener_end_y': screener_end_y
    }
  
    return pd.DataFrame(df_dict)
    
def play_csv_generator(filter_dict):
    """

    Parameters
    ----------
    filter_dict : dictionary generator
        This must take the form of the filtered dictionary generator output by
        filter candidate events.

    Returns
    -------
    Dataframe
        The returned dataframe will contain a row for each 
        candidate event along with necessary features for labeling.

    """
    game_id = []
    event_number = []
    event_desc = []
    handler_name = []
    screener_name = []
    start_time = []

    event_prior_stamp_start = 0

    for event in filter_dict:
        if event['event_info']['screen_time_stamps'][0] == event_prior_stamp_start:
            continue

        start_time.append(event['event_info']['screen_time_stamps'][0])
        game_id.append(event['gameid'])
        event_number.append(event['event_info']['id'])
        event_desc.append(event['event_info']['desc_home'] + " / " + event['event_info']['desc_away'])

        for player in (event['visitor']['players'] + event['home']['players']):
            if event['event_info']['handler_id'] == player['playerid']:
                handler_name.append(player['firstname'] + " " + player['lastname'])
            elif event['event_info']['screener_id'] == player['playerid']:
                screener_name.append(player['firstname'] + " " + player['lastname'])
        event_prior_stamp_start = event['event_info']['screen_time_stamps'][0]

    return pd.DataFrame({
        'game_id': game_id,
        'event_number': event_number,
        'start_time': start_time,
        'event_desc': event_desc,
        'handler_name': handler_name,
        'screener_name': screener_name
    })
