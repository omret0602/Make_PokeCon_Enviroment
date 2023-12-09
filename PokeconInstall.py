import subprocess
import requests
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from pathlib import Path
from loguru import logger
import git

class MainApp:
	def __init__(self, master=None):
		self._logger = logger

		self.pokecon_version_list =  ["Poke-Controller", "Poke-Controller-Modified", "Poke-Controller-Modified-Extension"]
		self.python_version_list = ["3.7","3.10","3.7"]
		self.python_url_list = ["https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe",
						  		"https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe",	
								"https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe"
								]		
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
									  ]
		self.root = tk.Tk()
		self.root.withdraw()
		toplevel_1 = tk.Toplevel(self.root)
		toplevel_1.configure(background="#c0c0c0", height=200, width=200)
		toplevel_1.geometry("500x600")
		toplevel_1.title("Make-PokeCon-Enviroment")
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

	def select_folder(self,event=None):
		folder_path = self.install_folder_path.get()
		if folder_path == "参照":
			path_name = filedialog.askdirectory(title="ポケコンをインストールするフォルダーを指定してください。")
			path_name = Path(path_name)
			if not path_name.is_absolute():
				messagebox.showerror("","フォルダーが正しく選択されていません。")
			else:
				self.install_folder_path.set(str(path_name))
				return
		else:
			return
			
	def select_pokecon(self,event):
		# self._logger.info("test")
		pokecon_name = self.select_pokecon_ver.get()
		list_idx = self.pokecon_version_list.index(pokecon_name)
		self.install_python_ver.set(self.python_version_list[list_idx])

	def start_install(self):
		pokecon_ver = self.select_pokecon_ver.get()
		idx  = self.pokecon_version_list.index(pokecon_ver)
		python_url = self.python_url_list.pop(idx)
		pokecon_git = self.git_pokecon_list.pop(idx)
		python_exe_name = self.convert_path()
		self.download_files(python_url,python_exe_name)
		venv_path = self.create_venv()
		self.make_pokecon(pokecon_git)
		self.install_libralies(venv_path)

	def convert_path(self):
		folder_path = Path(self.install_folder_path.get())
		py_name = f"python{self.install_python_ver.get()}.exe"
		folder_path.joinpath("download").mkdir(parents=True)
		python_exe_name = folder_path.joinpath("download",py_name)
		return python_exe_name

	def download_files(self,python_url, python_exe_name):
		self._logger.info("Download Python")
		py_res = requests.get(python_url)
		if py_res.status_code == 200:
			with open(str(python_exe_name),"wb")as file:
				file.write(py_res.content)
		else:
			pass
		self._logger.info("Start Install Python")
		python_args = [str(python_exe_name),"/quiet","InstallAllUsers=1","PrependPath=1","Include_test=0"]
		subprocess.run(python_args,shell=True)
		self._logger.info("Python Install Successfully")

	def create_venv(self):
		self._logger.info("Create Virtual Enviroment")
		venv_path = Path(self.install_folder_path.get()).joinpath("venv")
		# venv.create(str(venv_path), with_pip=True)
		subprocess.run(["python","-m","venv","venv"],cwd=self.install_folder_path.get())
		self._logger.info("Virtual Enviroment Construction Complete")
		return venv_path

	def install_libralies(self,venv_path):
		self._logger.info("Start Install Library")
		pokecon_ver = self.select_pokecon_ver.get()
		res, library = self.install_libralies_module(pokecon_ver)
		venv_path = Path(venv_path) 
		venv_python = venv_path.joinpath("Scripts","python")
		subprocess.run([str(venv_python),"-m","pip","install","--upgrade","setuptools"],shell=True)
		subprocess.run([str(venv_python),"-m","pip","install","--upgrade","pip"],shell=True)
		if not res:
			for name in library:
				subprocess.run([str(venv_python),"-m","pip","install",name],shell=True)
		else:
			subprocess.run([str(venv_python),"-m","pip","install","-r", library],shell=True)
		self._logger.info("Install Library Complete")
		self._logger.info("Install Successfully")
		res = messagebox.askyesno("Install Successfully","インストールが完了しました。\n終了しますか？")
		if res:
			self.mainwindow.destroy()
			self.root.destroy()
			subprocess.run("pause",shell=True)
		else:
			return

	def install_libralies_module(self,pokecon_ver):		
		if pokecon_ver == "Poke-Controller":
			library_list = self.install_libralie_list
			return False, library_list
		else:
			try:
				pokecon_folder_path = Path(self.install_folder_path.get())
				folder_list = [folder.name for folder in pokecon_folder_path.iterdir() if folder.is_dir()]
				delete_folder_name_list = ["venv","download"]
				for name in delete_folder_name_list:
					folder_list.remove(name)
				requirements_txt = pokecon_folder_path.joinpath(folder_list[0],"requirements.txt")
				self._logger.info("requirements.txt GET")
				return True, requirements_txt
			except:
				_, _ = self.install_libralies_module("Poke-Controller")


	def make_pokecon(self,pokecon_git):
		self._logger.info(f"Start Install {self.select_pokecon_ver.get()}")
		pokecon_folder_path = Path(self.install_folder_path.get()).joinpath(self.select_pokecon_ver.get())
		pokecon_folder_path.mkdir(parents=True)
		git.Repo.clone_from(pokecon_git,pokecon_folder_path,branch="master")
		

	def closing(self):
		res = messagebox.askyesno("終了確認","終了しますか？")
		if res:
			self.mainwindow.destroy()
			self.root.destroy()
			self._logger.info("インストールをキャンセルしました。")
			subprocess.run("pause",shell=True)
		else:
			return
		
	def run(self):
		self.mainwindow.mainloop()


if __name__ == "__main__":
	app = MainApp()
	app.run()