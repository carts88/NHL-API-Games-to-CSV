
# ===================================================================
# Time String Manipulation Helpers
# ===================================================================
"""
These 3 functions are for manipulating the timestrings within the nhl api into numbers
so they can easily be used for mathmatical purposes such as summing toi, averaging toi etc
"""
def time_string_to_mins_secs(time_string: str):
    minutes, seconds = map(int, time_string.split(':'))
    return  minutes, seconds

 
def time_string_to_secs(time_string: str):
    minutes, seconds = map(int, time_string.split(':'))
    minutes_to_seconds = minutes * 60
    return  minutes_to_seconds + seconds

def time_in_seconds_to_time_string(seconds: int):
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"  # Zero-padded for consistency

# ===================================================================
# ===================================================================