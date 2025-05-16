'''
This modules contains the definition of the INSTRUCTOR_PREF class 
'''

class InstructorPref():
    '''
    Class definition for an INSTRUCTOR_PREF object.
    '''
    def __init__(self, uid: str, name: str, week_day: str, start_time_code: str, end_time_code: str):
        '''
        Constructor for the InstructorPref class.
        
        Parameters:
        - name (str): Name of the instructor.
        - uid (str): Unique identifier for the instructor.
        - week_day (str): Day of the week for the session (e.g., "Monday").
        - start_time_code (str): Start time of the session in "HH:MM AM/PM" format.
        - end_time_code (str): End time of the session in "HH:MM AM/PM" format.
        '''
        self.name = name
        self.uid = uid
        self.week_day = week_day
        self.start_time_code = start_time_code
        self.end_time_code = end_time_code
        self.encoded_start_time_code = self.remap_time_code(start_time_code, week_day)
        
        
        
    def __repr__(self):
        '''
        String representation of the Session object.
        
        Returns:
        - str: String representation of the session object.
        
        '''
        return f"Instructor {self.name} on {self.week_day} at {self.start_time_code} - {self.end_time_code} = {self.encoded_start_time_code}\n"
    
    def remap_time_code(self, time_code: str, week_day: str) -> str:
        '''
        Remaps the time code to a different format.
        
        Parameters:
        - time_code (str): Time code to be remapped.
        
        Returns:
        - str: Remapped time code.
        
        EXAMPLE: (time:"9:00 AM", day:"Monday") -> "0_3"
        where first digit is the day of the week (0 = Monday, 1 = Tuesday, etc.)
        and second digit is the hour of the day (0 = 7:00 AM, 1 = 8:00 AM, etc.)
        INVARIANT: from 7:00 AM to 7:00 PM inclusive (12 hours)
        '''
        days_mapping = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }
        week_day = week_day.strip()
        # Extract hour and period (AM/PM) from the time code
        hour, period = time_code.split(" ")
        hour = int(hour.split(":")[0])
        
        # Convert to 24-hour format
        if period == "PM" and hour != 12:
            hour += 12
        elif period == "AM" and hour == 12:
            hour = 0
        
        # Ensure the hour is within the invariant range (7:00 AM to 7:00 PM)
        if hour < 7 or hour > 19:
            raise ValueError("Time code is outside the allowed range (7:00 AM to 7:00 PM).")
        
        # Map the hour to the range 0-11 (7:00 AM = 0, 8:00 AM = 1, ..., 7:00 PM = 11)
        hour_code = hour - 7
        
        # Get the day code
        day_code = days_mapping.get(week_day, -1)
        if day_code == -1:
            raise ValueError(f"Invalid week day: {week_day}")
        
        # Combine day code and hour code
        return f"{day_code}_{hour_code}"
        
        
