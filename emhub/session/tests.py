
import os
import unittest

from .data_manager import DataManager


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.ds = DataManager('/tmp/emhub.sqlite')

    def test_users(self):
        users = self.ds.get_users()

        print("\n>>> Users:")
        for u in users:
            pi = self.ds.get_user_pi(u)
            pi_str = pi.name if pi else 'None'
            print("User: %s, PI: %s" % (u.name, pi_str))

    def test_projects(self):
        projects = self.ds.get_projects()

        codes = [p.code for p in projects]

        self.assertEqual(codes, ['CEM00297', 'CEM00315', 'CEM00332', 'DBB00001'])

        users = self.ds.get_users()
        uList = []
        piDict = {}

        for u in users:
            if u.is_pi:
                if u.id not in piDict:
                    piDict[u.id] = [u]
                else:
                    piDict[u.id].append(u)

                uList.append("PI: %s, projects: %s" % (u.name, u.projects))
                uList.append("   Lab members:")
                for u2 in u.lab_members:
                    uList.append("     - %s" % u2.name)

        for l in uList:
            print(l)

        # Check that all users in the same lab, have the same projects
        for pi_id, members in piDict.items():
            pRef = members[0].get_projects()
            print("projects: ", pRef)
            for u in members[1:]:
                self.assertEqual(pRef, u.get_projects())


class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.ds = DataManager('/tmp/emhub.sqlite')
        #TODO: Create flask test App


if __name__ == '__main__':
    unittest.main()
