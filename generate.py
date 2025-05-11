import random
import numpy as np
import local_llm
import groq_llm
import json
import config

# Example values for random selection
gender = ["male", "female"]
ethnicities = [("White", 30), ("Black",10), ("Hispanic",15), ("Asian",15), ("Middle Eastern",5), ("Mixed",20), ("Indigenous",5)]
education_levels = [("Dropout",8), ("High School",20), ("Associate's",10), ("Bachelor's",40), ("Master's",10), ("PhD",5)]
wealth_levels = [("Low income",20), ("Middle income",50), ("High income",20), ("Trust fund",3), ("Self-made millionaire",3)]

def choose_random(arr):
    summ = sum([x[1] for x in arr])
    val = int(random.random()*summ)
    count = 0
    for x,v in arr:
        count+=v
        if count > val:
            return x
    return x

hobbies = [
    # Standard hobbies
    "reading", "writing", "painting", "drawing", "baking", "cooking", "hiking", "running", "cycling",
    "swimming", "traveling", "photography", "gardening", "playing guitar", "playing piano", "yoga",
    "meditation", "blogging", "journaling", "dancing", "playing video games", "watching movies",
    "watching TV series", "playing board games", "playing card games", "knitting", "crocheting",
    "fishing", "camping", "bird watching", "DIY projects", "home improvement", "acting", "singing",
    "karaoke", "collecting coins", "collecting stamps", "magic tricks", "drumming", "learning languages",
    "calligraphy", "volunteering", "working out", "rock climbing", "martial arts", "surfing", "snowboarding",
    "skiing", "ice skating", "scuba diving", "snorkeling", "skateboarding", "playing chess", "playing poker",
    "woodworking", "metalworking", "building model kits", "cosplaying", "attending conventions",
    "tattoo art", "piercing art", "fashion styling", "thrifting", "astrology", "tarot reading", "feng shui",

    # Niche and unusual hobbies
    "lockpicking", "beekeeping", "foraging", "urban exploration", "storm chasing", "mushroom hunting",
    "watching plane landings", "antiquing", "dumpster diving", "mechanical keyboards", "speedcubing",
    "fermenting foods", "guerilla gardening", "geocaching", "miniature painting", "creating fanfiction",
    "editing Wikipedia", "watching true crime documentaries", "watching surgery videos", "soap making",
    "perfume blending", "blacksmithing", "leather crafting", "tanning hides", "making chainmail",
    "historical reenactment", "LARPing", "building aquascapes", "fencing", "sword collecting",
    "watch collecting", "watch modding", "bonsai cultivation", "origami", "whittling", "bug collecting",
    "taxidermy", "fire dancing", "whip cracking", "building Rube Goldberg machines", "competitive eating",

    # Tech-centric/modern hobbies
    "coding", "ethical hacking", "cryptocurrency trading", "NFT collecting", "AI art creation",
    "3D printing", "robotics", "home automation", "building custom PCs", "VR gaming", "streaming on Twitch",
    "making TikToks", "YouTube vlogging", "photo editing", "digital art", "graphic design", "meme creation",

    # Socially frowned upon / controversial hobbies
    "gambling", "shoplifting", "catfishing", "online trolling", "dark web browsing", "conspiracy theorizing",
    "excessive drinking", "weed culture", "cigarette collecting", "watching disturbing films",
    "ghost hunting", "obsessing over exes", "online stalking", "fetish collecting", "knife throwing",
    "collecting weapons", "playing with fire", "dumpster diving for food", "exploring abandoned buildings",
    "vandalism art", "graffiti tagging", "frequenting adult sites", "debating strangers online", "doomscrolling",
    "hoarding", "messing with scammers", "breaking into abandoned places", "gambling crypto tokens",
    "pranking strangers", "pick-up artist seminars", "arguing politics online", "confrontational protesting",
    "dumpster furniture restoration", "writing revenge stories", "drama following", "flipping stolen goods",
    "fighting in public", "insult comedy", "running fake social media accounts",

    # Hyper-specific hobbies
    "collecting Funko Pops", "organizing cables", "watching speedruns", "writing parody lyrics",
    "ranking things in tier lists", "sorting coins by decade", "researching obscure history",
    "designing flags", "writing Yelp reviews", "watching courtroom livestreams", "microwave cooking",
    "rating public restrooms", "taking personality quizzes", "reading Reddit threads", "making playlists",
    "watching ASMR", "obsessing over niche fandoms", "following MLM drama", "building LEGO cities",
    "upgrading old laptops", "trading Pokemon cards", "ranking chip flavors", "collecting soda cans",
    "watching mukbangs", "farming karma on Reddit", "gossiping in DMs", "DM sliding", "eavesdropping in cafes",
    "organizing fantasy drafts", "roleplaying on forums", "watching courtroom shows", "following true crime TikTok"
]

issues = [
    # Common clinical diagnoses
    "Depression", "Anxiety", "Bipolar disorder", "Borderline Personality Disorder (BPD)",
    "Obsessive-Compulsive Disorder (OCD)", "Post-Traumatic Stress Disorder (PTSD)",
    "Attention Deficit Hyperactivity Disorder (ADHD)", "Autism Spectrum", "Eating Disorder",
    "Social Anxiety", "Panic Disorder", "Generalized Anxiety Disorder", "Schizophrenia",
    "Avoidant Personality Disorder", "Narcissistic Personality Disorder (NPD)",
    "Antisocial Personality Disorder", "Dependent Personality Disorder",

    # Addictions and compulsions
    "Alcohol addiction", "Drug addiction", "Nicotine addiction", "Porn addiction",
    "Shopping addiction", "Food addiction", "Gambling addiction", "Sex addiction",
    "Phone addiction", "Social media addiction", "Gaming addiction", "Adrenaline addiction",

    # Emotional/family baggage
    "Daddy issues", "Mommy issues", "Divorced parents trauma", "Abandonment issues",
    "Trust issues", "Jealousy issues", "Fear of commitment", "Divorce trauma",
    "Sibling rivalry scars", "Cheated on in past", "Emotionally unavailable",
    "Toxic ex trauma", "Still talks to ex", "Never had a long-term relationship",
    "High conflict past relationships",

    # Toxic traits and red flags
    "Controlling behavior", "Manipulative tendencies", "Gaslighting", "Ghosting people",
    "Love bombing", "Constant need for validation", "Passive-aggressive behavior",
    "Insecurity-driven drama", "Jealous over friends", "Excessive flirting",
    "Emotionally explosive", "Inability to apologize", "Always plays the victim",
    "Blames others for everything", "Refuses therapy", "Thinks therapy is a scam",
    "Overly cynical", "Always testing partners", "Fear of intimacy", "Self-sabotages relationships",

    # Self-destructive quirks or problematic habits
    "Impulsive spender", "Chronic procrastinator", "Sleeps all day", "Doesn’t clean",
    "Never answers texts", "Never replies to DMs", "Always late", "Constantly moving cities",
    "Overshares on social media", "Treats life like reality TV", "Addicted to chaos",
    "Secretly wants to be famous", "Poly but doesn’t tell partners", "Open relationship ambivalence",
    "Convinced they're the main character", "Won’t stop quoting astrology", "Obsessed with revenge",
    "Creates fake drama for fun", "Self-diagnoses constantly", "Blocks people for small things",
    "Compulsively checks partner's phone", "Overanalyzes texts", "Hyperfixates on red flags",
    "Sabotages happy moments", "Believes in soulmates but dumps everyone",

    # Socially problematic or extreme beliefs
    "Conspiracy theorist", "Flat earther", "Anti-vax beliefs", "Hyper political rants",
    "Extreme religious trauma", "Cult survivor", "Red pill ideology", "Misogynistic tendencies",
    "Gold digger accusations", "Thinks they're always right", "Believes they're misunderstood genius",
    "Constantly comparing self to others", "Incorrigibly sarcastic", "Thinks everyone is fake",
    "Believes love should hurt", "Romanticizes toxic relationships", "Only dates for status"
]

personalities = ["INTJ", "INTP", "INFJ", "INFP", "ISTJ", "ISTP", "ISFJ", "ISFP",
                 "ENTJ", "ENTP", "ENFJ", "ENFP", "ESTJ", "ESTP", "ESFJ", "ESFP"
                ]
style = [
    "Witty and sarcastic", "Shy but sweet", "Hopeless romantic", "Blunt and brutally honest",
    "Playful and flirty", "Quiet observer", "Overthinker who triple texts", "Always makes the first move",
    "Chaotic and unpredictable", "Loyal to a fault", "Loves deep convos at 2am", "The therapist friend",
    "Meme lord with trust issues", "Always down to argue (playfully)", "Easily distracted but passionate",
    "Drama magnet but self-aware", "Sweet talker who ghosts sometimes", "Lowkey emotionally unavailable",
    "Hyper-intelligent but socially awkward", "Extremely online and knows it", "Loves attention but hates people",
    "Type to fall in love after 3 texts", "Caring but won't show it first", "Dry texter in denial",
    "Romantic nihilist", "Silly and chaotic", "Too intense too fast", "Quiet but clingy", 
    "In love with the idea of love", "Dark humor only", "Chronically misunderstood",
    "Wildly affectionate", "Lowkey possessive", "Constantly roasting people",
    "Has a wall up but wants it broken", "The cool mysterious one", "Overshares way too early",
    "Wants to fix people", "Emotionally deep but jokes instead", "Subtle flirt who won’t admit it",
    "Ghosts then apologizes dramatically", "The golden retriever energy", "Introvert pretending to be extrovert",
    "Disarmingly charming", "Emotionally intense poet type", "Freak in the group chat, saint in public",
    "Sarcastic but sweet underneath", "The oversharer", "Clingy in a cute way", "Emotionally mature and grounded",
    "Acts tough but loves cuddles", "Simp energy but with standards", "Flirty but emotionally unavailable",
    "Dark and mysterious (but posts memes)", "The funny one with trauma", "Over-apologizes constantly",
    "Always playing therapist", "Soft-spoken but will fight for love", "Low maintenance but needs reassurance"
]

def generate_about_me(profile):
    # You can use an actual LLM API here. Below is a placeholder using f-string.
    length = random.choice(["a", "a short", "a long"])
    prompt = f"""
Write {length} dating profile 'about me' section for someone like the following: 

Gender: {profile['gender']}
Ethnicity: {profile['ethnicity']}
Education: {profile['education']}
Hobbies: {", ".join(profile['hobbies'])}
Income: {profile['income']}
Personality (subtle): {profile['personality']}
Writing/Talking Style: {", ".join(profile['writing_style'])}
Issues (subtle): {", ".join(profile['issues'])}

Start off with a username, and then the about me text. Try to avoid mentioning the education and ethnicity values if possible.
"""
    print(prompt)
    if config.local_llm:
       data = local_llm.call_llm(prompt)
    else:
       data = groq_llm.call_llm(prompt)
    print(data)
    # Replace the following with a real LLM call if needed:
    return data

def generate_profile(gender='female'):
    appearance = int(np.clip(np.random.normal(5.5, 1.5), 1, 10))
    profile = {
        "gender": gender,
        "appearance": appearance,
        "ethnicity": choose_random(ethnicities),
        "education": choose_random(education_levels),
        "hobbies": random.sample(hobbies, k=3),
        "income": choose_random(wealth_levels),
        "personality": random.choice(personalities),
        "writing_style": random.sample(style,k=2),
        "issues": random.sample(issues, k=random.randint(2, 3)),
    }
    about = generate_about_me(profile)
    name, _, about = about.partition("\n")
    name = name.strip()
    about = about.strip()
    profile["about_me"] = about
    profile['username'] = name

    save_profile(profile)
    return profile
    
g_profiles = {"female": [], "male": []}
def save_profile(profile):
    g = profile['gender'] 
    g_profiles[g].append(profile)
    open(f"profiles_{g}.json","a").write(json.dumps(profile)+"\n")


# Example usage
if __name__ == "__main__":
    config.load_config()
    for i in range(1000):
        for g in ["female", "male"]:
            profile = generate_profile(g)
    #for k, v in profile.items():
    #    print(f"{k.capitalize()}: {v}")

