import subprocess
import requests
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from pathlib import Path
from loguru import logger

# FOLDER_PATH = Path("download")
# PYTHON_VER = "3.11"
# PYTHON_URL = "https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe"
# # PYTHON_FILE_NAME = f"python{PYTHON_VER}.exe"
# PYTHON_LIBRARIES = ["opencv-python","pynput","pyserial","Pillow","pythonnet","pygubu","requests","pandas","numpy","scipy","packaging","customtkinter","loguru","pygame"]
# GIT_URL = "https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/Git-2.31.1-64-bit.exe"
# GIT_FILE_NAME = "Git-2.31.1-64-bit.exe"
# GIT_POKECON = "https://github.com/Moi-poke/Poke-Controller-Modified.git"
# POKECON_PATH = Path("C:\PokeCon9999")
# POKECON_NAME = "Poke-Controller-Modified"
	

class MainApp:
	def __init__(self, master=None):
		self._logger = logger

		self.pokecon_version_list =  ["Poke-Controller", "Poke-Controller-Modified", "Poke-Controller-Modified-Extension"]
		self.python_version_list = ["3.7","3.11","3.7"]
		self.python_url_list = ["https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe",
						  		"https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe",	
								"https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe"
								]
		self.git_url = "https://github.com/git-for-windows/git/releases/download/v2.31.1.windows.1/Git-2.31.1-64-bit.exe"
		
		self.git_pokecon_list = ["https://github.com/KawaSwitch/Poke-Controller.git",
						   		 "https://github.com/Moi-poke/Poke-Controller-Modified.git",
								 "https://github.com/futo030/Poke-Controller-Modified-Extension.git"
								]
		self.install_libralie_list = ["opencv-python",
									  "pynput",
									  "pyserial",
									  "Pillow",
									  "pythonnet",
									  "pygubu",
									  "requests",
									  "pandas",
									  "numpy",
									  "scipy",
									  "packaging",
									  "customtkinter",
									  "loguru",
									  "pygame"]
		
		self.git_name = "Git-2.31.1-64-bit.exe"

		self.root = tk.Tk()
		self.root.withdraw()
		# self.load_settings()

		toplevel_1 = tk.Toplevel(self.root)
		toplevel_1.configure(background="#c0c0c0", height=200, width=200)
		toplevel_1.geometry("500x600")
		frame_1 = ttk.Frame(toplevel_1)
		frame_1.configure(height=588, width=488)
		label_2 = ttk.Label(frame_1)
		label_2.configure(anchor="center",background="#008040",font="{游ゴシック} 12 {}",justify="center",relief="ridge",text='Poke-Controller 環境構築')
		label_2.place(anchor="nw",relheight=0.1,relwidth=0.8,relx=0.1,rely=0.05,x=0,y=0)
		label_3 = ttk.Label(frame_1)
		label_3.configure(anchor="center",background="#008040",font="{游ゴシック} 12 {}",justify="center",relief="ridge",text='Path')
		label_3.place(anchor="nw",relheight=0.1,relwidth=0.3,relx=0.1,rely=0.2,x=0,y=0)
		label_4 = ttk.Label(frame_1)
		label_4.configure(anchor="center",background="#008040",font="{游ゴシック} 12 {}",justify="center",relief="ridge",text='PokeCon')
		label_4.place(anchor="nw",relheight=0.1,relwidth=0.3,relx=0.1,rely=0.35,x=0,y=0)
		label_5 = ttk.Label(frame_1)
		label_5.configure(anchor="center",background="#008040",font="{游ゴシック} 12 {}",justify="center",relief="ridge",text='Python Ver')
		label_5.place(anchor="nw",relheight=0.1,relwidth=0.3,relx=0.1,rely=0.5,x=0,y=0)
		
		self.combobox_select_path = ttk.Combobox(frame_1)
		self.install_folder_path = tk.StringVar()
		self.combobox_select_path.configure(justify="center",state="readonly",textvariable=self.install_folder_path,values='"" "参照"')
		self.combobox_select_path.place(anchor="nw",relheight=0.1,relwidth=0.5,relx=0.4,rely=0.2,x=0,y=0)
		
		self.combobox_select_pokecon_ver = ttk.Combobox(frame_1)
		self.select_pokecon_ver = tk.StringVar()
		self.combobox_select_pokecon_ver.configure(justify="center",state="readonly",textvariable=self.select_pokecon_ver,values=self.pokecon_version_list)
		self.combobox_select_pokecon_ver.place(anchor="nw", relheight=0.1, relwidth=0.5, relx=0.4, rely=0.35, x=0, y=0)
		
		self.combobox_install_python_ver = ttk.Combobox(frame_1)
		self.install_python_ver = tk.StringVar()
		self.combobox_install_python_ver.configure(state="disabled", textvariable=self.install_python_ver,values=self.python_version_list)
		self.combobox_install_python_ver.place(anchor="nw", relheight=0.1, relwidth=0.5, relx=0.4, rely=0.5, x=0, y=0)
		
		button_1 = ttk.Button(frame_1)
		button_1.configure(text='インストール開始',command=self.start_install)
		button_1.place(anchor="nw",relheight=0.1,relwidth=0.8,relx=0.1,rely=0.85,x=0,y=0)
		frame_1.grid(column=0, padx=6, pady=6, row=0, sticky="nsew")
		# Main widget
		self.mainwindow = toplevel_1
		self.mainwindow.protocol("WM_DELETE_WINDOW",self.closing)
		self.combobox_select_path.bind("<<ComboboxSelected>>",self.select_folder)
		self.combobox_select_pokecon_ver.bind("<<ComboboxSelected>>",self.select_pokecon)

	def select_folder(self,event):
		if self.install_folder_path.get() == "参照":
			path_name = filedialog.askdirectory(title="ポケコンをインストールするフォルダーを指定してください。")
			self.install_folder_path.set(path_name)
			path_name = Path(path_name)
			if not path_name.is_absolute():
				messagebox.showerror("","フォルダーが正しく選択されていません。")
			else:
				# self.install_folder_path = path_name
				return
			
	def select_pokecon(self,event):
		self._logger.info("test")
		pokecon_name = self.select_pokecon_ver.get()
		list_idx = self.pokecon_version_list.index(pokecon_name)
		self.install_python_ver.set(self.python_version_list[list_idx])

	def start_install(self):
		pokecon_ver = self.select_pokecon_ver.get()
		if pokecon_ver in self.pokecon_version_list:
			idx  = self.pokecon_version_list.index(pokecon_ver)
		python_url = self.python_url_list.pop(idx)
		pokecon_git = self.git_pokecon_list.pop(idx)
		self.convert_path()
		self.download_files(python_url)
		self.install_libralies()
		self.make_pokecon(pokecon_git)
		self._logger.info("finish")
		self.closing()



	def convert_path(self):
		folder_path = Path(self.install_folder_path.get())
		py_name = f"python{self.install_python_ver.get()}.exe"
		self.install_folder = folder_path.joinpath("download")
		# self.install_pokecon_folder = folder_path.joinpath(self.select_pokecon_ver.get())
		if not self.install_folder.exists():
			self.install_folder.mkdir(parents=True)
		self.python_exe_name = folder_path.joinpath("download",py_name)
		self.git_exe_name = folder_path.joinpath("download",self.git_name)



	def download_files(self,python_url):
		self._logger.info("download files")
		py_res = requests.get(python_url)
		if py_res.status_code == 200:
			with open(str(self.python_exe_name),"wb")as file:
				file.write(py_res.content)
		else:
			pass
		git_res = requests.get(self.git_url)
		if git_res.status_code == 200:
			with open(str(self.git_exe_name),"wb")as file:
				file.write(git_res.content)
		python_args = [str(self.python_exe_name),"/quiet","InstallAllUsers=1","PrependPath=1","Include_test=0"]
		git_args = [str(self.git_exe_name),"/VERYSILENT","/NORESTART","/NOCANCEL","/SP-","/CLOSEAPPLICATIONS","/RESTARTAPPLICATIONS","/COMPONENTS=icons,ext\reg\shellhere,assoc,assoc_sh"]
		self._logger.info("Start Install Python")
		subprocess.run(python_args,shell=True)
		self._logger.info("Start Install GIT")
		subprocess.run(git_args,shell=True)

	def install_libralies(self):
		self._logger.info("start install libraries")
		subprocess.run(["py",f"-{self.install_python_ver.get()}","-m","pip","install","--upgrade","setuptools"],shell=True)
		subprocess.run(["py",f"-{self.install_python_ver.get()}","-m","pip","install","--upgrade","pip","--user"],shell=True)
		for name in self.install_libralie_list:
			subprocess.run(["py",f"-{self.install_python_ver.get()}","-m","pip","install",name,"--user"],shell=True)
		self._logger.info("installed librariles")

	def make_pokecon(self,pokecon_git):
		self._logger.info("make pokecon modified")
		subprocess.run(["git","clone","--recursive",str(pokecon_git)],cwd=self.install_folder_path.get(),shell=True)
		subprocess.run(["git","pull","origin","master"],cwd=self.install_folder_path.get(),shell=True)
		self._logger.info("installed PokeCon Modified")



	def run(self):
		self.mainwindow.mainloop()

	def closing(self):
		res = messagebox.askyesno("終了確認","終了しますか？")
		if res:
			self._logger.info("インストールを終了しました。")
			self.mainwindow.destroy()
			self.root.destroy()
		else:
			return


if __name__ == "__main__":
	# BuildingEnvironment()
	app = MainApp()
	app.run()