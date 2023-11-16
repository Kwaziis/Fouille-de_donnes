class Action:
    def __init__(self,user,date,heure,actionType,actionDetails):
        self.user = user
        self.date = date
        self.heure = heure
        self.actionType = actionType
        self.actionDetails = actionDetails#dico qui contient attribut

class ForumDetail:
    def __init__(self,forumId):
        self.forumId = forumId
        self.forumActions = []
    def addForumAction(self,action):
        self.forumActions.append(action)
    def actionNumber(self):
        return len(self.forumActions)
    def userNumber(self):
        users = []
        for action in self.forumActions:
            if(action.user not in users):
                users.append(action.user)
        return len(users)
    def __repr__(self):
        return "ForumDetail: forumId = {}, actionNumber = {}, userNumber = {}".format(self.forumId,self.actionNumber(),self.userNumber())