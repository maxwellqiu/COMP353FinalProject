from mysqlCtrl import MysqlCtrl
from CONSTANTS import user, password, host, port, database_name


class MVC:

    sqlctrl = MysqlCtrl(user, password, host, port, database_name)

    def getLocation(self):
        query = """
                SELECT *
                FROM Location;
                """
        result = self.sqlctrl.query(query)
        return result

    def getPersonnel(self):
        query = """
                SELECT *
                FROM Personnel;
                """
        result = self.sqlctrl.query(query)
        return result

    def getFamilyMember(self):
        query = """
                SELECT *
                FROM FamilyMember;
                """
        result = self.sqlctrl.query(query)
        return result

    def getClubMember(self):
        query = """
                SELECT *
                FROM ClubMember;
                """
        result = self.sqlctrl.query(query)
        return result

    def getTeamFormation(self):
        query = """
                SELECT *
                FROM TeamFormation;
                """
        result = self.sqlctrl.query(query)
        return result

    def getLog(self):
        query = """
                SELECT *
                FROM Log;
                """
        result = self.sqlctrl.query(query)
        return result


if __name__ == "__main__":

    mvc = MVC()

    print(mvc.getLocation())
