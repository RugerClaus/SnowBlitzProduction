class User:

    def __init__(self, system):

        self.system = system

    @property
    def username(self):

        username = self.system.persistence.load.read_constant("username")

        if username is None:
            username = "Player"
            self.system.persistence.save.write_constant(
                "username",
                username
            )

        return username
    
    @username.setter
    def username(self,value):
        username = value
        self.system.persistence.save.write_constant(
            "username",
            username
        )

    @property
    def high_score(self):

        score = self.system.persistence.load.read_constant("high_score")

        if score is None:
            score = 0
            self.system.persistence.save.write_constant(
                "high_score",
                score
            )

        return int(score)
    
    @high_score.setter
    def high_score(self, value):
        self.system.persistence.save.write_constant(
            "high_score",
            int(value)
        )