import json
from model import Action, ForumDetail

InterestingActions = [
    "Afficher une structure (cours/forum)",
    "Répondre à un message",
    "Afficher le fil de discussion",
    "Poster un nouveau message",
    "Afficher le contenu d'un message",
    "Bouger la scrollbar en bas - afficher la fin du message",
    "Bouger la scrollbar en bas",
    "Citer un message"
    ]

#Step 1 extract actions from the actions.json file
from datetime import datetime, time

def load_actions(filename):
    with open(filename, 'r') as f:
        actions_data = json.load(f)
    actions = []
    for action_data in actions_data:
        date_str = action_data["date"]
        heure_str = action_data["heure"]
        # Convert date and heure into date and time objects
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        heure = datetime.strptime(heure_str, '%H:%M:%S').time()
        action = Action(action_data["user"], date, heure, action_data["actionType"], action_data["actionDetails"])
        actions.append(action)
    return actions

def get_forum_details(actions,InterestingActions):
    forumDetails = []
    for action in actions:
        if action.actionType in InterestingActions:
            forumId = action.actionDetails["IDForum"]
            # Check if forumId already exists in forumDetails
            forumDetail = next((f for f in forumDetails if f.forumId == forumId), None)
            if not forumDetail:
                forumDetail = ForumDetail(forumId)
                forumDetails.append(forumDetail)
            forumDetail.addForumAction(action)
    return forumDetails

#sort the actions by date
def sort_actions_by_date(actions):
    return sorted(actions, key=lambda action: action.date)

def get_number_of_weeks(date1, date2):
    days = abs((date2 - date1).days)
    weeks = days // 7
    if days % 7 != 0:
        weeks += 1
    return weeks

def split_action_list_by_week(actions):
    sorted_actions = sort_actions_by_date(actions)
    min_date =  sorted_actions[0].date
    max_date = sorted_actions[-1].date
    number_of_weeks = get_number_of_weeks(min_date, max_date)
    week_actions = [[] for i in range(number_of_weeks)]
    for action in sorted_actions:
        week_number = get_number_of_weeks(min_date, action.date)
        week_actions[week_number-1].append(action)
    return week_actions

def total_message_number(forums):
    total = 0
    for forum in forums:
        total += forum.message_number()
    return total

def forum_actif_indice(forums):
    total = total_message_number(forums)
    if(total == 0):
        return
    for forum in forums:
        active_indice = forum.message_number()/total
        forum.setActiveIndice(round(active_indice,2))
def total_citation_number(forums):
    total = 0
    for forum in forums:
        total += forum.citation_number()
    return total

def forum_discute_indice(forums):
    for forum in forums:
        message_number = forum.message_number()
        if(message_number == 0):
            continue
        forum.setCitationIndice(forum.citation_number()/message_number)

def total_utilisateurs_actifs(forums):
    total = 0
    for forum in forums:
        total += forum.userNumber()[1]
    return total

def forum_populaire_indice(forums):
    total = total_utilisateurs_actifs(forums)
    if(total == 0):
        return
    for forum in forums:
        popularite_indice = forum.userNumber()[1]/total
        forum.setPopulariteIndice(round(popularite_indice,2))

def dataProcessing(filename):
    actions = load_actions(filename)
    forums = get_forum_details(actions,InterestingActions)
    #on cree un aray pour chaque forum avec le complet d'abord puis le détail pour chaque semaine
    data = {}
    for forum in forums:
        data[forum.forumId] = []
        data[forum.forumId].append(forum)
    #on process les indicateurs sur le overall
    forum_actif_indice(forums)
    forum_discute_indice(forums)
    forum_populaire_indice(forums)

    #maintenant on s'ocupe du détail par semaine
    week_actions = split_action_list_by_week(actions)
    for week_action in week_actions:
        week_forum = get_forum_details(week_action,InterestingActions)
        #on process les indicateurs sur le weekly
        forum_actif_indice(week_forum)
        forum_discute_indice(week_forum)
        forum_populaire_indice(week_forum)

        #on ajoute les données dans le data
        for weeklyForum in week_forum:
            data[weeklyForum.forumId].append(weeklyForum)
        for key in data.keys():
            if key not in week_forum:
                data[key].append(ForumDetail(key))
    return data

if(__name__ == "__main__"):
    data = dataProcessing("actions.json")
    print(data)