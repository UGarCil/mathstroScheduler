'''
A module for utility functions used in the mathstronauts scheduling algorithm.
This module contains functions to parse input data for sessions (SESSION) and instructor preferences (INSTRUCTOR_PREF).

From txt files, the SESSION data should look as follows (tab as separator):
Monday	09:00 AM - 10:00 AM
Tuesday	09:00 AM - 10:00 AM
Wednesday	09:00 AM - 10:00 AM
Thursday	09:00 AM - 10:00 AM
Friday	09:00 AM - 10:00 AM

Where the first column is the day of the week (Monday to Sunday) 
and the second column is the time range of the session.

output:
- LIST_OF_SESSION: List of SESSION objects to be used in the algorithm: [SESSION, SESSION, ...]

From txt files, the INSTRUCTOR_PREF data should look as follows (tab as separator):
gacu001 Uriel Garcilazo Monday   09:00 AM - 10:00 AM
gacu001 Uriel Garcilazo Monday   10:00 AM - 11:00 AM

'''

import json 
import os 
from os.path import join as jn 
from .session import Session
from .instructor_pref import InstructorPref
from typing import List, Dict, Any

def parse_inputSESSION_text(file_path: str) -> List[Session]:
    '''
    Parses the input file for sessions and creates a list of Session objects.
    
    Parameters:
    - file_path (str): Path to the input file containing session data.
    
    Returns:
    - List[Session]: List of Session objects created from the input data.
    
    '''
    sessions = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                day, time_range = line.split('\t')
                start_time, end_time = time_range.split(' - ')
                session = Session(week_day=day, start_time_code=start_time, end_time_code=end_time)
                sessions.append(session)
    except Exception as e:
        print(f"Error parsing session file: {e}")
    return sessions


def parse_inputINSTRUCTOR_PREF_text(file_path: str) -> List[InstructorPref]:
    '''
    Parses the input file for instructor preferences and creates a list of InstructorPref objects.
    
    Parameters:
    - file_path (str): Path to the input file containing instructor preference data.
    
    Returns:
    - List[InstructorPref]: List of InstructorPref objects created from the input data.
    '''
    instructor_prefs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                uid, name, day, time_range = line.split('\t')
                start_time, end_time = time_range.split(' - ')
                instructor_pref = InstructorPref(uid=uid, name=name, week_day=day, start_time_code=start_time, end_time_code=end_time)
                instructor_prefs.append(instructor_pref)
    except Exception as e:
        print(f"Error parsing instructor preference file: {e}")
    return instructor_prefs
    
    