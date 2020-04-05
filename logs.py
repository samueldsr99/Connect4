from datetime import datetime
import os

"""
    Functions & classes to log game data & print stadistics
"""
class Log:
    def __init__(self):
        """
            history[i] = (
                Turn Counter,
                Id of Turn (1 or 2),
                Last Action,
                Last Action Wins,
                Last Action Simulations,
                Win Estimed Probability,
                Response Time (provided outside of the class)
            )
        """
        self.History = []
        self.messages = []
        self.TurnCounter = 0

    """
        Register the Last Action on the Game
    """
    def RegisterLastAction(self, turn, lastAction, wins, simulations, responseTime):
        self.TurnCounter += 1
        self.History.append((
            self.TurnCounter,
            turn,
            lastAction,
            "--" if not simulations else wins,
            "--" if not simulations else simulations,
            "--" if not simulations else wins / simulations,
            "--" if not simulations else responseTime
        ))

    def log(self, msg):
        self.messages.append(msg)

    def _actionStatistics(self, it):
        last = self.History[it]
        return "____________________________________________\nmove #: \t\t\t%s\nPlayer: \t\t\t%s\nAction: \t\t\t%s\nWins: \t\t\t\t%s\nSimulations: \t\t\t%s\nWin Estimated Probability: \t%s\nResponse Time: \t\t\t%s\n____________________________________________\n" % last

    def LastActionStatistics(self):
        return self._actionStatistics(-1)

    """
        Save the Data of the Game
    """
    def SaveData(self):
        now = datetime.now()
        
        filename = "snapshot_from_" + "_".join([str(now.year), str(now.month), str(now.day), str(now.hour), str(now.minute), str(now.second)])

        if not "history" in os.listdir():
            os.mkdir("history")
        
        out = open("history/" + filename + ".hst", "w")

        for m in self.messages:
            out.write(m + '\n')

        for i in range(len(self.History)):
            out.write(self._actionStatistics(i))
        
        out.close()
