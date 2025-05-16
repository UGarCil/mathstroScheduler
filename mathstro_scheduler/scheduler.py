'''
Control module for the evaluation of the different objects and helper methods required by the algorithm.

The program integrates a heuristic approach to solve the optimality problem of matching schedules with 
available time slots. 

Symbols and definitions:
- CD: Class definition
- FD: Function definition
- DD: Data definition 

The following defiinitions are used:
- CD. SESSION: a single class session object, defined by a target instructor: session.Session()
- DD. LIST_OF_SESSION: List of SESSION objects to be used in the algorithm: [SESSION, SESSION, ...]
- CD. INSTRUCTOR_PREF: Object to be assigned to a SESSION.instructor_pref attribute: instructor_pref.InstructorPref()
- DD. LIST_OF_INSTRUCTOR_PREF: List of INSTRUCTOR_PREF objects to be used in the algorithm.: [INSTRUCTOR_PREF, INSTRUCTOR_PREF, ...]

HYPERPARAMETERS:
- EPOCHS: Number of epochs to run the algorithm: int
- REPLICATES: Number of replicates to run the algorithm: int
- MAX_ATTEMPTS: Maximum number of attempts to assign a session to an instructor: int
- _ATTEMPTS: LOCAL variable to count the number of attempts to assign a session to an instructor: int

ALGORITHM:
for a certain number of EPOCHS:
    for a given number of REPLICATES: 
        for each SESSION in LIST_OF_SESSION:
            set variable _ATTEMPTS to 0
            with INSTRUCTOR_PREF sampled from randomized LIST_OF_INSTRUCTOR_PREF:
                try_assign_instructor(INSTRUCTOR_PREF, SESSION) -> success: bool
                if success: break then move to next SESSION 
                else: _ATTEMPTS += 1 and if _ATTEMPTS > MAX_ATTEMPTS, break and move to next SESSION
  
            
'''

import random
from typing import List, Dict, Any, Union, Optional, Tuple
from .scheduler_utils import parse_inputSESSION_text, parse_inputINSTRUCTOR_PREF_text
from .session import Session
from .instructor_pref import InstructorPref
import tqdm 
import os 
from os.path import join as jn

def try_assign_instructor(instructor_pref: Session, session: InstructorPref) -> bool:
    '''
    Attempts to assign an instructor to a session based on a set of optimality criteria.
    
    Parameters:
    - instructor_pref (InstructorPref): The instructor preference object.
    - session (Session): The session object to be assigned.
    
    Returns:
    - bool: True if the assignment is successful, False otherwise.
    '''
    # Check if the instructor is available for the session
    if instructor_pref.encoded_start_time_code == session.encoded_start_time_code:
        return instructor_pref.uid
    return None
        

def calculate_session_assignments(list_of_session, list_of_instructor_prefs,replicates) -> List[Union[int, None]]:
    # Shuffle the instructor preferences for randomness
    list_of_randomized_instructor_pref_indices = [i for i in range(len(list_of_instructor_prefs))]
    random.shuffle(list_of_randomized_instructor_pref_indices)
    
    # Output to store session assignments
    session_assignments = []
    
    # Iterate over each session
    for session in list_of_session:
        _assigned = False
        
        # Try to assign an instructor to the session
        for idx in list_of_randomized_instructor_pref_indices:
            instructor_pref = list_of_instructor_prefs[idx]
            # Attempt to assign the instructor to the session 
            success = try_assign_instructor(instructor_pref, session)
            # If assignment was successful, there's no need to try more instructors
            if success and idx not in session_assignments:
                # Store the assignment and break out of the loop
                session_assignments.append(idx)
                _assigned = True
                break
        # If no instructor was assigned after traversing the list, assign None
        if not _assigned:
            session_assignments.append(None)
    
    # Print the session assignments
    return session_assignments

def update_best_session_assignment(best_session_assignments, best_score, candidate_session_assignments) -> Tuple[int, List[Union[int,None]]]:
    '''
    Update the best session assignments based on the score of the candidate session assignments.

    Parameters:
    - best_session_assignments (List[int]): The current best session assignments.
    - best_score (int): The current best score.
    - candidate_session_assignments (List[int]): The candidate session assignments to evaluate.

    Returns:
    - Tuple: Updated best session assignments and score.

    - RULES:
        for each session in the candidate_session_assignments:
            - A penalty of -5 for any session not filled
            - A reward of +2 if previous session has the same instructor AND is on the same day
                - prev_instructor_pref = list_of_instructor_prefs[best_session_assignments[idx-1]] if idx > 0
                - current_instructor_pref = list_of_instructor_prefs[candidate_session_assignments[idx]]
                - Use current_instructor_pref.uid to evaluate if the instructor is the same as the previous one
                  IF current_instructor_pref.week_day == prev_instructor_pref.week_day
            - Update score 
        Is score > best_score?
            - if yes, update best_session_assignments and best_score
            - else, return best_session_assignments and best_score
    '''
    score = 0

    for idx, instructor_idx in enumerate(candidate_session_assignments):
        if instructor_idx is None:
            score -= 5  # Penalty for unfilled session
        else:
            if idx > 0:
                prev_idx = candidate_session_assignments[idx - 1]
                if prev_idx is not None:
                    prev_instructor_pref = list_of_instructor_prefs[prev_idx]
                    curr_instructor_pref = list_of_instructor_prefs[instructor_idx]
                    if (curr_instructor_pref.uid == prev_instructor_pref.uid and
                        curr_instructor_pref.week_day == prev_instructor_pref.week_day):
                        score += 2  # Reward for same instructor on same day

    if score > best_score or best_session_assignments is None:
        return candidate_session_assignments, score
    else:
        return best_session_assignments, best_score
   
def map_assignments(best_session_assignments):
    '''
    Maps the best session assignments to the original format, adding the instructor and saving as a table .txt.
    An entry of the final table takes the form:
    
    Session.week_day	Session.start_time_code - Session.end_time_code	InstructorPref.instructor_uid InstructorPref.name
    Monday	09:00 AM - 10:00 AM gacu001 Uriel Garcilazo Cruz
    
    '''
    _mappings = ""
    for idx, instructor_idx in enumerate(best_session_assignments):
        # session is list_of_session[idx]
        _current_session = list_of_session[idx]
        # instructor is list_of_instructor_prefs[instructor_idx]
        _current_instructor_pref = list_of_instructor_prefs[instructor_idx]
        formatted_session = f"{_current_session.week_day}\t{_current_session.start_time_code} - {_current_session.end_time_code}\t{_current_instructor_pref.uid}\t{_current_instructor_pref.name}\n"
        _mappings += formatted_session 
    return _mappings


def scheduler(epochs: int, replicates: int, max_attempts: int, session_file: str, instructor_pref_file: str,output_path="./", verbose=True) -> None:
    '''
    Main function to run the scheduling algorithm.
    
    Parameters:
    - epochs (int): Number of epochs to run the algorithm.
    - replicates (int): Number of replicates to run the algorithm.
    - max_attempts (int): Maximum number of attempts to assign a session to an instructor.
    - session_file (str): Path to the input file containing session data.
    - instructor_pref_file (str): Path to the input file containing instructor preference data.
    
    Returns:
    - A .txt file with the unique identifier of an INSTRUCTOR_PREF.uid for each SESSION.
    '''
    # Parse input files to get session and instructor preference data
    global list_of_session, list_of_instructor_prefs
    
    list_of_session = parse_inputSESSION_text(session_file)
    list_of_instructor_prefs = parse_inputINSTRUCTOR_PREF_text(instructor_pref_file)

    

    # Run the algorithm for the specified number of epochs
    # Iniitalize a score and best_session_assignments veriables
    best_score = 0
    best_session_assignments = None
    for epoch in tqdm.tqdm(range(epochs), desc="Epochs", unit="epoch"):
        candidate_session_assignments = calculate_session_assignments(list_of_session, list_of_instructor_prefs,replicates)
        best_session_assignments, best_score = update_best_session_assignment(best_session_assignments, best_score, candidate_session_assignments)
        if verbose:
            print(f"best_session_assignments: {best_session_assignments}, best_score: {best_score}")
    
    
    # Remap the best session assignment schedule ot the original format, adding the instructor and saving as table .txt
    final_session_assignments = map_assignments(best_session_assignments)
    print(final_session_assignments) if verbose else None
    with open(jn(output_path,"output_schedules.txt"), "w") as f:
        f.write(final_session_assignments)




