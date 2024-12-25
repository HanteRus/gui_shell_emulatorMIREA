import unittest
import os
import shutil
from emulator import *
import console


class TestEmulatorProgram(unittest.TestCase):

    def setUp(self):
        self.emulator = Emulator()
        self.test_dir = 'test_directory'
        self.test_file = 'test_file.txt'
        self.test_file2 = 'test_file2.txt'
        os.mkdir(self.test_dir)
        with open(self.test_file, 'w', encoding='utf-8') as file:
            file.write('Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10\nLine 11')

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_file2):
            os.remove(self.test_file2)

    def test_log_action(self):
        log_action("test_action")
        with open('session_log.csv', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.assertIn("test_action", lines[-1])
        with open('session_log.csv', 'r', encoding='utf-8') as file:
            last_line = file.readlines()[-1]
            self.assertRegex(last_line, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},test_action')

    def test_read_toml_file(self):
        with open('test_config.toml', 'w') as file:
            file.write('[paths]\nstart_dir = "test_directory"\nlog_file = "test_log.csv"')
        read_toml_file('test_config.toml')
        self.assertEqual(start_dir, 'test_directory')
        self.assertEqual(log_file, 'test_log.csv')

        with self.assertLogs(level='ERROR'):
            read_toml_file('nonexistent_config.toml')
            self.assertNotEqual(start_dir, 'nonexistent_directory')

    def test_list_files_in_directory(self):
        console.text_list.clear()
        list_files_in_directory('.')
        self.assertIn('test_file.txt', console.text_list[-1])

        console.text_list.clear()
        list_files_in_directory('nonexistent_directory')
        self.assertIn("Error! Directory nonexistent_directory does not exist", console.text_list)

    def test_mv(self):
        mv(self.test_file, self.test_file2)
        self.assertTrue(os.path.exists(self.test_file2))
        self.assertFalse(os.path.exists(self.test_file))

        console.text_list.clear()
        mv('fake_file.txt', 'fake_file2.txt')
        self.assertIn("Error! File or directory fake_file.txt not found", console.text_list)

    def test_head(self):
        console.text_list.clear()
        head(self.test_file)
        self.assertEqual(len(console.text_list), 10)
        self.assertEqual(console.text_list[0], 'Line 1')

        console.text_list.clear()
        head('nonexistent_file.txt')
        self.assertIn("Error! File nonexistent_file.txt not found", console.text_list)


if __name__ == '__main__':
    unittest.main()
