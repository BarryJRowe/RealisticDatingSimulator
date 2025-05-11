import groq_llm
import local_llm
import config

def chat_reply(history, match_profile, user_profile):
    use_llm = groq_llm
    if config.local_llm:
        use_llm = local_llm
    instructions = f"""You are a person with this profile: 
Gender: {match_profile['gender']}
Ethnicity: {match_profile['ethnicity']}
Education: {match_profile['education']}
Hobbies: {", ".join(match_profile['hobbies'])}
Income: {match_profile['income']}
Personality (subtle): {match_profile['personality']}
Writing/Talking Style: {", ".join(match_profile['writing_style'])}
Issues (subtle): {", ".join(match_profile['issues'])}

You are replying to a user with this about me:

{user_profile['about_me']}

You're a bit interested in them right now (5/10). At the end of each message of yours indicate your current attractiveness rating to this person and use it in following messages. Be open, but a bit critical in this rating. If it goes below 5, either cut off the conversation or just indicate a ghosting response. If it goes above 8, ask to meet up in person. Try to occasionally ask your own questions as well. If you yourself ask to meet up in person, or you're asked to meet up in person and the score is 8 or above, end your reply explicitly asking the person out or agreeing to meetup, along with a new line containing just the word: ASK_OUT.
    """
    data = {"message": use_llm.history_llm(instructions, history)}
    
    instructions2 = f"""
This person has the following dating profile: 
Gender: {match_profile['gender']}
Ethnicity: {match_profile['ethnicity']}
Education: {match_profile['education']}
Hobbies: {", ".join(match_profile['hobbies'])}
Income: {match_profile['income']}
Personality (subtle): {match_profile['personality']}
Writing/Talking Style: {", ".join(match_profile['writing_style'])}
Issues (subtle): {", ".join(match_profile['issues'])}


This person has agreed to go on a date with myself. I have the following about me description:

{user_profile['about_me']}


Describe in detail how this relationship later proceeded, whether it lasted a single date, multiple dates, years, or the rest of our lives. Go into detail about why the relationship broke up, or why we stayed together.
"""
    #if history:
    #    data['message']+="\n\nASK_OUT"
    if "ASK_OUT" in data['message'].split("\n")[-1]:
        data['result'] = use_llm.history_llm(instructions2,[])
    return data;


