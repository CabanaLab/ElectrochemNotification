"""Unit tests for EmailWhenDone"""

import unittest, re, datetime, sys, testsettings as ts

sys.path.append("..")
import DirectoryWatcher, message_preparation as mp, send_notification as sn, user_info_test as uit, globalsettings as gs

class test_message_preparation(unittest.TestCase):
    def test_get_user_data(self):
        """Tests the ability of filename strings to match with names and email addresses of users"""
        test_data = (
            ("C:/DATA/Alvin/2017/XXX_650_#195_LP57_Li(29-#195)_dischar1d5 then charge to 2d5 V_01_PEIS_CA2",(['Alvin'], ['alvin@chip.edu'])),
            ("C:/DATA/Simon/cycling/021417_66CSLNMC_rep1_CD3",(["Simon"], ["simon@chip.edu"])),
            ("C:/DATA/Theodore/Alvin/20170206 NMC111 800C1h AN_CD4", (["Alvin", "Theodore"], ["alvin@chip.edu", "theodore@chip.edu"]))
        )
        for exp_in, exp_out in test_data:
            result = mp.find_user(exp_in, user_list=uit)
            self.assertEqual(result, exp_out)

class test_DirectoryWatcher(unittest.TestCase):
    def test_is_valid(self):
        """Tests whether the ignore_list works"""
        test_data = (
            ("C:/DATA/Data/Theodore/XXX/6d1mg impedance 10 cycle",(False)), # Good file
            ("C:/DATA/Alvin/.ignore/impedance",(True)), # .sync in
            ("C:/DATA/list/data",(True)),
        )
        for exp_in, exp_out in test_data:
            result = DirectoryWatcher.is_valid(exp_in, settingsfile=ts)
            self.assertEqual(result, exp_out)
            
class test_send_notification(unittest.TestCase):
    def test_make_message(self):
        test_data = (
            ("Alvin",("C:/DATA/Alvin/2017/XXX_650_#195_LP57_Li(29-#195)_dischar1d5 then charge to 2d5 V_01_PEIS_CA2")),
    )
        test_html = """\
        <html>
        <head></head>
        <body bgcolor="#FFFFFF" text="#000000">
        <p>Hello Alvin, <br>
        </p>
        <p>You are receiving this email to notify you that your electrochemical experiment <em>"C:/DATA/Alvin/2017/XXX_650_#195_LP57_Li(29-#195)_dischar1d5 then charge to 2d5 V_01_PEIS_CA2"</em> has finished. Please collect it at your earliest convenience.</p>
        <p>Regards, <br>
    </p>
        <p>Cabana Server</p>
        <p><em>This message is automated: sent out by a bot that collects and distributes the relevant data. For questions, complaints, bug reports, or feature requests; please <a href="mailto:moderator@chip.edu">contact your moderator</a> ({version})</em></p>
        </html>
        """.format(version=gs.version)

    # print(test_data)
    
    for (exp_user, exp_email) in test_data:
        # print('[DEBUG]', exp_user, exp_email)
        result = sn.make_message(exp_user, exp_email, settingsfile=ts)
        self.assertEqual(result.strip('\t'), test_html.strip('\t'))    
