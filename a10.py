import re, string, calendar, requests, time
from wikipedia import WikipediaPage
import wikipedia
from bs4 import BeautifulSoup
from match import match
from typing import List, Callable, Tuple, Any, Match


def get_page_html(title: str) -> str:
    search_response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={"action": "query", "list": "search", "srsearch": title, "format": "json"},
        headers={"User-Agent": "intro-ai-class/1.0"},
        timeout=10
    )
    results = search_response.json().get("query", {}).get("search", [])
    if results:
        title = results[0]["title"]  # use the top search result title
        print(f"Searching Wikipedia for: {title}")

    for attempt in range(5):
        try:
            response = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "parse",
                    "page": title,
                    "prop": "text",
                    "format": "json",
                    "redirects": True,
                },
                headers={"User-Agent": "intro-ai-class/1.0"},
                timeout=10
            )
        except requests.exceptions.ConnectTimeout:
            print(f"Connection timed out, retrying '{title}'... (attempt {attempt+1}/5)")
            time.sleep(5)
            continue

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 5))
            print(f"Rate limited — waiting {wait}s before retrying '{title}'...")
            time.sleep(wait)
            continue
        if response.status_code == 200 and response.text.strip():
            data = response.json()
            if "error" not in data:
                time.sleep(3)
                return data["parse"]["text"]["*"]

    raise ConnectionError(f"Could not retrieve Wikipedia page for '{title}' after 5 attempts")

def get_first_infobox_text(html: str) -> str:
    """Gets first infobox html from a Wikipedia page (summary box)

    Args:
        html - the full html of the page

    Returns:
        html of just the first infobox
    """
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all(class_="infobox")

    if not results:
        raise LookupError("Page has no infobox")
    return results[0].text


def clean_text(text: str) -> str:
    """Cleans given text removing non-ASCII characters and duplicate spaces & newlines

    Args:
        text - text to clean

    Returns:
        cleaned text
    """
    only_ascii = "".join([char if char in string.printable else " " for char in text])
    no_dup_spaces = re.sub(" +", " ", only_ascii)
    no_dup_newlines = re.sub("\n+", "\n", no_dup_spaces)
    return no_dup_newlines


def get_match(
    text: str,
    pattern: str,
    error_text: str = "Page doesn't appear to have the property you're expecting",
) -> Match:
    """Finds regex matches for a pattern

    Args:
        text - text to search within
        pattern - pattern to attempt to find within text
        error_text - text to display if pattern fails to match

    Returns:
        text that matches
    """
    p = re.compile(pattern, re.DOTALL | re.IGNORECASE)
    match = p.search(text)

    if not match:
        raise AttributeError(error_text)
    return match


def get_polar_radius(planet_name: str) -> str:
    """Gets the radius of the given planet

    Args:
        planet_name - name of the planet to get radius of

    Returns:
        radius of the given planet
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(planet_name)))
    pattern = r"(?:Polar radius|Mean radius)(?:[^\d]*)(?P<radius>[\d,.]+)(?:.*?)km"
    error_text = "Page infobox has no polar radius information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group("radius")


def get_birth_date(name: str) -> str:
    """Gets birth date of the given person

    Args:
        name - name of the person

    Returns:
        birth date of the given person
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(name)))
    print(infobox_text)
    pattern = r"(?:Born|Date of birth.*)(?P<birth>\d{4}-\d{2}-\d{2})"
    error_text = (
        "Page infobox has no birth information (at least none in xxxx-xx-xx format)"
    )
    match = get_match(infobox_text, pattern, error_text)

    return match.group("birth")

def get_developer_game(game_name: str) -> str:
    """Gets the dev of the given game

    Args:
        game_name - name of the game to get dev of

    Returns:
        dev of the given game
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(game_name)))
    print(infobox_text)
    pattern = r"(?:Developer)(?P<developer>\w \w+)"
    error_text = "Page infobox has no developer information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group("developer")

def get_show_episodes(show_name: str) -> str: #this works 
    """Gets the episodes of the given show

    Args:
        show_name - name of the show

    Returns:
        episodes of the given show
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(show_name)))
    #print(infobox_text)
    pattern = r"(?:Episodes|Episode)(?P<episodes>\d+)"
    error_text = "Page infobox has no episode information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group("episodes")

def get_car_year(car_year: str) -> str: #this works 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(car_year)))
    print(infobox_text)
    pattern = r"(?:Production\w+ |Production)(?P<year>\d{4})"
    error_text = "Page infobox has no car year information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group("year")

def get_company_industry(company_industry: str) -> str: #works 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(company_industry)))
    #print(infobox_text)
    pattern = r"Industry\s*(?P<industry>.+?)\s*Founded"
    error_text = "Page infobox has no company industry information"
    match = get_match(infobox_text, pattern, error_text)

    return match.group("industry")
#Start of the new functions
def get_height_building(building_height: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(building_height)))
    #print(infobox_text)
    pattern = r"(?:Tip)(?P<height>.+?)\s*(?:Antenna|Roof)"
    error_text = "Page infobox has building height information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("height")
    
def get_employee_amount(employee_number: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(employee_number)))
    #print(infobox_text)
    pattern = r"(?:Number of employees)(?P<employees>.+?)\s(?:)"
    error_text = "Page infobox has employee information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("employees")

def get_(employee_number: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(employee_number)))
    #print(infobox_text)
    pattern = r"(?:Number of employees)(?P<employees>.+?)\s(?:)"
    error_text = "Page infobox has employee information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("employees")

def get_currency(currency_name: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(currency_name)))
    #print(infobox_text)
    pattern = r"(?:Currency)\s*(?P<currency>[A-Za-z ]+)"
    error_text = "Page infobox has currency information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("currency")

def get_family(family_name: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(family_name)))
    #print(infobox_text)
    pattern = r"(?:Family:)\s(?P<family>[A-Za-z ]+)"
    error_text = "Page infobox has family information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("family")

def get_calling_code(calling_code: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(calling_code)))
    #print(infobox_text)
    pattern = r"(?:Calling code)(?P<calling_code>.+)(?:ISO)"
    error_text = "Page infobox has calling code information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("calling_code")

def get_war(war_date: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(war_date)))
    #print(infobox_text)
    pattern = r"(?:Date)(?P<war_time>.+)(?:Location)"
    error_text = "Page infobox has war date information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("war_time")

def get_state_capital(capital: str) -> str: 
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(capital)))
    #print(infobox_text)
    pattern = r"(?:Capital)(?P<state_capital>.+)(?:Largest city)"
    error_text = "Page infobox has state capital information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("state_capital")

def get_f1_drivers(f1_team: str) -> str:
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(f1_team)))
    #print(infobox_text)
    pattern = r"(?:Race drivers)(?P<f1_drivers>.+)(?:Test driver)"
    error_text = "Page infobox has F1 drivers information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("f1_drivers")

def get_food_founders(food_name: str) -> str:
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(food_name)))
    #print(infobox_text)
    pattern = r"(?:Founders)(?P<food_founders>.+)(?:Headquarters)"
    error_text = "Page infobox has food founders information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("food_founders")

def get_NHL_team_division(nhl_team: str) -> str:
    """Gets the year of the given car

    Args:
        car_year - year of the car

    Returns:
        year of the given car
    """
    infobox_text = clean_text(get_first_infobox_text(get_page_html(nhl_team)))
    #print(infobox_text)
    pattern = r"(?:Division)(?P<nhl_division>.+)(?:Founded)"
    error_text = "Page infobox has NHL team division information"
    match = get_match(infobox_text, pattern, error_text)
    return match.group("nhl_division")



# below are a set of actions. Each takes a list argument and returns a list of answers
# according to the action and the argument. It is important that each function returns a
# list of the answer(s) and not just the answer itself. (?:Industry)(?P<products>\w[a-z]*)


def birth_date(matches: List[str]) -> List[str]:
    """Returns birth date of named person in matches

    Args:
        matches - match from pattern of person's name to find birth date of

    Returns:
        birth date of named person
    """
    return [get_birth_date(" ".join(matches))]


def polar_radius(matches: List[str]) -> List[str]:
    """Returns polar radius of planet in matches

    Args:
        matches - match from pattern of planet to find polar radius of

    Returns:
        polar radius of planet
    """
    return [get_polar_radius(matches[0])]

def show_episodes(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_show_episodes(" ".join(matches))]

def year_car(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_car_year(matches[0])]

def dev_game(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_developer_game(matches[0])]

def industry(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_company_industry(matches[0])]

def build_height(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_height_building(matches[0])]

def employee_amount(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_employee_amount(matches[0])]

def currency_type(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_currency(matches[0])]

def animal_family(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_family(matches[0])]

def calling_code(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_calling_code(matches[0])]

def war_period(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_war(matches[0])]

def state_capital(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_state_capital(matches[0])]

def f1_drivers(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_f1_drivers(matches[0])]

def food_founders(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_food_founders(matches[0])]

def nhl_team_division(matches: List[str]) -> List[str]:
    """Returns episodes of shows in matches

    Args:
        matches - match from pattern of shows to find amount of episodes

    Returns:
        episodes of show
    """
    return [get_NHL_team_division(matches[0])]



# dummy argument is ignored and doesn't matter
def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt


# type aliases to make pa_list type more readable, could also have written:
# pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [...]
Pattern = List[str]
Action = Callable[[List[str]], List[Any]]

# The pattern-action list for the natural language query system. It must be declared
# here, after all of the function definitions
pa_list: List[Tuple[Pattern, Action]] = [
    ("when was % born".split(), birth_date),
    ("what is the polar radius of %".split(), polar_radius),
    ("how many episodes does % have".split(), show_episodes),# WORKS
    ("what year was the % made".split(), year_car), # WORKS
    ("who made % ".split(), dev_game),
    ("what is % known for ".split(), industry),
    #new
    ("how tall is the % ".split(), build_height),
    ("how many employees does % ".split(), employee_amount), # WORKS
    ("what is the currency of % ".split(), currency_type),
    ("what is the family of % ".split(), animal_family),
    ("what is the calling code of % ".split(), calling_code),
    ("what is the war period of % ".split(), war_period),
    ("what is the state capital of % ".split(), state_capital),
    ("who are the f1 drivers of % ".split(), f1_drivers),
    ("who are the fast food founders of % ".split(), food_founders),
    ("what division is % in ".split(), nhl_team_division), 
    #("when was % born".split(), place_born),
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    for pat, act in pa_list:
        mat = match(pat, src)
        if mat is not None:
            answer = act(mat)
            return answer if answer else ["No answers"]

    return ["I don't understand"]


def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully"""
    print("Welcome to the wikipedia chatbot!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nSo long!\n")


# uncomment the next line once you've implemented everything are ready to try it out
query_loop()
