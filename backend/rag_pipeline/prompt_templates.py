import random

ROTATING_PROMPTS = [
    "Give me a list of {MAX_QUERIES} artists known for having strong isolated percussion or vocal sections, ideal for sampling in Afro, Latin, funk, or world music genres. List only the names—no extra explanation.",
    "Name {MAX_QUERIES} obscure funk or Latin artists known for minimal arrangements or instrumental intros, perfect for sample-based production. List only the names—no extra explanation.",
    "List {MAX_QUERIES} rare Afrobeat or highlife musicians with clean breaks in their songs ideal for sampling. List only the names—no extra explanation.",
    "Give me {MAX_QUERIES} Colombian or Peruvian artists from the 60s to 80s with raw isolated percussion that’s ideal for sampling. List only the names—no extra explanation.",
    "Suggest {MAX_QUERIES} artists from the Caribbean or West Africa with songs that have isolated vocal intros or outros suitable for sampling. List only the names—no extra explanation.",
    "Provide {MAX_QUERIES} experimental or psychedelic world music bands that use prominent percussion in minimal arrangements. List only the names—no extra explanation.",
    "List {MAX_QUERIES} crate-digger gems from African, Brazilian, or Caribbean records that often have acapella intros or sparse breakdowns. List only the names—no extra explanation.",
    "Name {MAX_QUERIES} underappreciated percussion-heavy acts with sample-worthy rhythms in non-English funk, cumbia, or Afrobeat. List only the names—no extra explanation.",
    "Give me a list of {MAX_QUERIES} artists featured in obscure vinyl compilations of world funk or spiritual jazz who are known for isolated sampleable sections. List only the names—no extra explanation.",
    "List {MAX_QUERIES} rare musicians with clean drum or vocal breakdowns suitable for chopping and sampling in global groove genres. List only the names—no extra explanation."
]

def get_random_prompt(max_queries=10):
    prompt = random.choice(ROTATING_PROMPTS)
    return prompt.replace("{MAX_QUERIES}", str(max_queries))