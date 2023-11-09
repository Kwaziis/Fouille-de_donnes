class Action:
    def __init__(self,user,date,heure,actionType,actionDetails):
        self.user = user
        self.date = date
        self.heure = heure
        self.actionType = actionType
        self.actionDetails = actionDetails#dico qui contient attribut