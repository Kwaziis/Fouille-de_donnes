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
def load_actions(filename):
    with open(filename, 'r') as f:
        actions_data = json.load(f)
    actions = []
    for action_data in actions_data:
        action = Action(action_data["user"],action_data["date"],action_data["heure"],action_data["actionType"],action_data["actionDetails"])
        actions.append(action)
    return actions

def get_forum_details(actions):
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

def get_forum_with_most_actions(actions):
    forumDetails = {}
    for action in actions:
        if(action.actionType in InterestingActions):
            forumId = action.actionDetails["IDForum"]
            if(forumId not in forumDetails):
                forumDetails[forumId] = ForumDetail(forumId)
            forumDetails[forumId].addForumAction(action)
            forumDetails[forumId].addForumAction(action)
    
    # Find the forum with the most actions
    max_actions = 0
    max_forum = None
    for forum in forumDetails.values():
        if forum.actionNumber() > max_actions:
            max_actions = forum.actionNumber()
            max_forum = forum.forumId
    
    return max_forum

if(__name__ == "__main__"):
    actions = load_actions("actions.json")
    forumDetails = get_forum_details(actions)
    print(len(forumDetails))