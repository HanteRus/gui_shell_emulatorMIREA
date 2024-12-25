import time
import pygame
import console
import os
import sys
import getpass
import zipfile
import configparser
import csv
import toml

start_dir = 'C:/Users/user/Desktop/DZKonfig'
log_file = 'session_log.csv'
username = getpass.getuser()

def read_toml_file(filename):
	global start_dir, log_file
	try:
		config = toml.load(filename)
		start_dir = config.get('paths', {}).get('start_dir', start_dir)
		log_file = config.get('paths', {}).get('log_file', log_file)
	except FileNotFoundError:
		console.text_list.append("Error with loading config file!")

def log_action(action):
	with open(log_file, mode='a', newline='', encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), action])

def exit_programm():
	log_action("exit")
	pygame.quit()
	sys.exit()

def print_help():
	commands = [
		"help: Displays this list of commands",
		"clear: Clears the console output",
		"about: Shows information about this program",
		"exit: Exits the emulator",
		"ls [directory]: Lists all files and directories",
		"tree -d/-a/-f: Displays a directory tree",
		"cd [directory]: Changes the current working directory",
		"mv [source] [destination]: Moves or renames files",
		"head [file]: Displays the first 10 lines of a file"
	]
	for command in commands:
		console.text_list.append(f" * {command}")
	log_action("help")

def clear():
	console.text_list.clear()
	log_action("clear")

def list_files_in_directory(start_path, indent='', zip_file=None):
    if zip_file:
        with zipfile.ZipFile(zip_file, 'r') as z:
            for item in z.namelist():
                console.text_list.append(f"{indent}-> {item}")
    else:
        try:
            items = os.listdir(start_path)
            for item in items:
                path = os.path.join(start_path, item)
                if os.path.isfile(path):
                    console.text_list.append(f"{indent}-> {item}")
                elif os.path.isdir(path):
                    console.text_list.append(f"{indent}-> {item}")
                    list_files_in_directory(path, indent + '    ')
        except FileNotFoundError:
            console.text_list.append(f"Error! Directory {start_path} does not exist")

def cd(data):
    global start_dir
    try:
        if data.endswith('.zip'):
            start_dir = data
            console.text_list.append(f"Changed to ZIP file: {start_dir}")
            list_files_in_directory(start_dir, zip_file=start_dir)
        else:
            os.chdir(data)
            start_dir = os.getcwd()
            log_action(f"cd {data}")
    except (FileNotFoundError, NotADirectoryError):
        console.text_list.append(f"Error! Directory {data} does not exist")

def tree(data):
	option = data.split(" ")[-1] if " " in data else None
	if not option:
		console.text_list.append("Error! No options")
		return

	if start_dir.endswith('.zip'):
		with zipfile.ZipFile(start_dir, 'r') as z:
			items = z.namelist()
			process_tree_option(items, option)
	else:
		items = os.listdir(start_dir)
		process_tree_option(items, option)
	log_action(f"tree {option}")

def process_tree_option(items, option):
	if option == "-d":
		for item in items:
			if os.path.isdir(item):
				console.text_list.append(f"-> {item}")
	elif option == "-a":
		for item in items:
			console.text_list.append(f"-> {item}")
	elif option == "-f":
		for item in items:
			if os.path.isfile(item):
				console.text_list.append(f"-> {item}")
	else:
		console.text_list.append("Invalid tree option")

def mv(source, destination):
    try:
        # Если источник и назначение не совпадают,
        # то переименовываем источник в назначение
        if source != destination:
            # Получаем имя файла, который нужно переместить
            file_name = os.path.basename(source)
            # Создаем относительный путь к файлу в целевом каталоге
            relative_path = os.path.join(destination, file_name)
            os.rename(source, relative_path)
            console.text_list.append(f"Moved {source} to {destination}")
            log_action(f"mv {source} {destination}")
        else:
            console.text_list.append(f"Source and destination are the same. Nothing to move.")
    except FileNotFoundError:
        console.text_list.append(f"Error! File or directory {source} not found")
    except PermissionError:
        console.text_list.append(f"Error! Permission denied for {source} or {destination}")

def head(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			lines = file.readlines()[:10]
			for line in lines:
				console.text_list.append(line.strip())
		log_action(f"head {file_path}")
	except FileNotFoundError:
		console.text_list.append(f"Error! File {file_path} not found")
	except UnicodeDecodeError:
		console.text_list.append("Error! File cannot be read as text")

def error_command(command):
	console.text_list.append(f"Command {command} does not exist. Type 'help' for a list of commands")
	log_action(f"Invalid command: {command}")

class Emulator:
	def __init__(self):
		pass

	def read_command(self, command):
		if command == "help":
			print_help()
		elif command == "clear":
			clear()
		elif command == "exit":
			exit_programm()
		elif command == "ls":
			list_files_in_directory(start_dir)
		elif command.startswith("ls "):
			ls_path = command[3:]
			list_files_in_directory(ls_path)
		elif command == "cd":
			cd(start_dir)
		elif command.startswith("cd "):
			cd_path = command[3:]
			cd(cd_path)
		elif command.startswith("tree"):
			tree(command)
		elif command.startswith("mv "):
			_, src, dst = command.split()
			mv(src, dst)
		elif command.startswith("head "):
			file_path = command[5:]
			head(file_path)
		else:
			error_command(command)

		print(console.text_list)

read_toml_file('config.toml')