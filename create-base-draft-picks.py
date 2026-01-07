from constants import team_codes, draft_rounds

draft_picks_list = []

def create_initial_draft_picks(draft_year: int):
    """
    This function creates the initial draft_pick data for a specific draft_year
    """
    for team in team_codes:
        for draft_round in draft_rounds:
            draft_pick_id = f"{draft_year}-{team}-{draft_round}"
            draft_pick = [
                draft_pick_id, # pickId
                team, #currentOwner
                team, #originalOwner
                draft_year,
                draft_round,                
            ]    
            draft_picks_list.append(draft_pick)

create_initial_draft_picks(2026)

print(draft_picks_list)
