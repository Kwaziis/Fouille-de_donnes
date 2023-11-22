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
        self.ActiveIndice = 0
        self.citationIndice = 0
        self.populariteIndice = 0

    def addForumAction(self,action):
        self.forumActions.append(action)
    def setActiveIndice(self,indice):
        self.ActiveIndice = indice
    def setCitationIndice(self,indice):
        self.citationIndice = indice
    def setPopulariteIndice(self,indice):
        self.populariteIndice = indice

    def actionNumber(self):
        return len(self.forumActions)
    def userNumber(self):
        active_users = self.activeUsers()
        activeUserNumber = 0
        for user in active_users:
            if(active_users[user]):
                activeUserNumber += 1
        return len(active_users),activeUserNumber
    def activeUsers(self):
        userData = {}
        for action in self.forumActions:
            if(action.user not in userData):
                userData[action.user] = False
            if(action.actionType == "Poster un nouveau message"):
                userData[action.user] = True
        return userData
    def message_number(self):
        number = 0
        for action in self.forumActions:
            if(action.actionType == "Poster un nouveau message"):
                number += 1
        return number
    def citation_number(self):
        number = 0
        for action in self.forumActions:
            if(action.actionType == "Citer un message"):
                number += 1
        return number
    def __repr__(self):
        return "ForumDetail: forumId = {}, actionNumber = {}, userNumber = {}, indice d'activité ={}, indice de discussion ={}, indice de popularité={}\n".format(self.forumId,self.actionNumber(),self.userNumber(),self.ActiveIndice,self.citationIndice,self.populariteIndice)