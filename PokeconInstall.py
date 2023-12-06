import subprocess
import requests
from pathlib import Path
from loguru import logger

FOLDER_PATH = Path("download")
PYTHON_VER = "3.11"
PYTHON_URL = "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"
PYTHON_FILE_NAME = f"python{PYTHON_VER}.exe"
PYTHON_LIBRARIES =["opencv-python","pynput","pyserial","Pillow","pythonnet","pygubu","requests","pandas","numpy","scipy","packaging","customtkinter","loguru","pygame"]
GIT_URL = "https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/Git-2.31.1-64-bit.exe"
GIT_FILE_NAME = "Git-2.31.1-64-bit.exe"
GIT_POKECON = "https://github.com/Moi-poke/Poke-Controller-Modified.git"
POKECON_PATH = Path("C:\PokeCon9999")
POKECON_NAME = "Poke-Controller-Modified"



class BuildingEnvironment:
	def __init__(self) -> None:
		self._logger = logger

		self.install_folder = POKECON_PATH.joinpath(FOLDER_PATH)
		self.install_pokecon_folder = POKECON_PATH.joinpath(POKECON_NAME)
		if not self.install_folder.exists():
			self.install_folder.mkdir(parents=True)
			# self.install_pokecon_folder.mkdir(parents=True)
		self.python_exe_name = POKECON_PATH.joinpath(FOLDER_PATH,PYTHON_FILE_NAME)
		self.git_exe_name = POKECON_PATH.joinpath(FOLDER_PATH,GIT_FILE_NAME)
		self.download_files()
		self.install_libralies()
		self.make_pokecon_modified()




	def download_files(self):
		self._logger.info("download files")
		py_res = requests.get(PYTHON_URL)
		if py_res.status_code == 200:
			with open(str(self.python_exe_name),"wb")as file:
				file.write(py_res.content)
		else:
			pass
		git_res = requests.get(GIT_URL)
		if git_res.status_code == 200:
			with open(str(self.git_exe_name),"wb")as file:
				file.write(git_res.content)
		python_args = [str(self.python_exe_name),"/quiet","InstallAllUsers=1","PrependPath=1","Include_test=0"]
		git_args = [str(self.git_exe_name),"/VERYSILENT","/NORESTART","/NOCANCEL","/SP-","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/COMPONENTS=icons,ext\reg\shellhere,assoc,assoc_sh"]
		subprocess.run(python_args,shell=True)
		self._logger.info("installed python")
		subprocess.run(git_args,shell=True)
		self._logger.info("installed git")

	def install_libralies(self):
		self._logger.info("start install libraries")
		subprocess.run(["py",f"-{PYTHON_VER}","-m","pip","install","--upgrade","setuptools"],shell=True)
		subprocess.run(["py",f"-{PYTHON_VER}","-m","pip","install","--upgrade","pip","--user"],shell=True)
		for name in PYTHON_LIBRARIES:
			subprocess.run(["py",f"-{PYTHON_VER}","-m","pip","install",name,"--user"],shell=True)
		self._logger.info("installed librariles")

	def make_pokecon_modified(self):
		self._logger.info("make pokecon modified")
		subprocess.run(["git","clone","--recursive",str(GIT_POKECON)],cwd=POKECON_PATH,shell=True)
		subprocess.run(["git","pull","origin","master"],cwd=POKECON_PATH,shell=True)
		self._logger.info("installed PokeCon Modified")


if __name__ == "__main__":
	BuildingEnvironment()