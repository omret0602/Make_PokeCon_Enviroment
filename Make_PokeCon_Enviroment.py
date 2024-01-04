import subprocess
import requests
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from pathlib import Path
from loguru import logger
import platform
import os
import tarfile
import shutil


log_folder = Path("./Log")
log_path = log_folder.joinpath(f"install_log.log")
logger.add(log_path,rotation="1 day",level="INFO")

class MainApp:
	def __init__(self, master=None):

		self._logger = logger
		try:
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
			self.combobox_select_pokecon_ver.configure(justify="center",state="readonly",textvariable=self.select_pokecon_ver)
			self.combobox_select_pokecon_ver.place(anchor="nw", relheight=0.1, relwidth=0.5, relx=0.4, rely=0.35, x=0, y=0)
			
			self.combobox_install_python_ver = ttk.Combobox(frame_1)
			self.install_python_ver = tk.StringVar()
			self.combobox_install_python_ver.configure(justify="center",state="readonly", textvariable=self.install_python_ver)
			self.combobox_install_python_ver.option_add("*TCombobox*Listbox.Font", ("{游ゴシック} 12 {}"))
			self.combobox_install_python_ver.place(anchor="nw", relheight=0.1, relwidth=0.5, relx=0.4, rely=0.5, x=0, y=0)
			
		
			self.button_install = ttk.Button(frame_1)
			self.button_install.configure(text='インストール開始',state="disabled",command=self.main)
			self.button_install.place(anchor="nw",relheight=0.1,relwidth=0.8,relx=0.1,rely=0.85,x=0,y=0)
			frame_1.grid(column=0, padx=6, pady=6, row=0, sticky="nsew")
			# Main widget
			self.mainwindow = toplevel_1
			self.mainwindow.protocol("WM_DELETE_WINDOW",self.closing)
			self.combobox_select_path.bind("<<ComboboxSelected>>",self.select_folder)
			self.combobox_select_pokecon_ver.bind("<<ComboboxSelected>>",self.input_check)
			self.combobox_install_python_ver.bind("<<ComboboxSelected>>",self.input_check)
			self.load_settings()

		except Exception as e:
			self._logger.exception(e)
			subprocess.run("pause",shell=True)



	def load_settings(self):
		try:
			current_file_path = Path(".").parent
			
			# Setting Path
			self.setting_path_name = current_file_path.joinpath("Settings")
			# Default Path Set
			default_path_file = self.setting_path_name.joinpath("Install_Default_Path.txt")
			self._logger.info("Get Install Default Path")
			with open(default_path_file,'r',encoding='utf-8') as file:
				install_path = file.read()
			self.install_folder_path.set(install_path)
			self.python_folder_path = self.setting_path_name.joinpath("Python_Versions")

			# Confirm Platform
			self.system_name = platform.system()
			# Get Python Versions
			self._logger.info("Get Python Versions")
			try:
				# Windows
				if self.system_name == "Windows":
					self.system_path = self.python_folder_path.joinpath("Windows")
					not_ext_python_txt_names = [f.stem for f in Path(self.system_path).glob('*') if f.is_file()]
					self.combobox_install_python_ver["values"] = not_ext_python_txt_names
				# Mac
				elif self.system_name == "Darwin":
					self.system_path = self.python_folder_path.joinpath("Darwin")
					not_ext_python_txt_names = [f.stem for f in Path(self.system_path).glob('*') if f.is_file()]
					self.combobox_install_python_ver["values"] = not_ext_python_txt_names
				# Linux
				elif self.system_name == "Linux":
					self.system_path = self.python_folder_path.joinpath("Linux")
					not_ext_python_txt_names = [f.stem for f in Path(self.system_path).glob('*') if f.is_file()]
					self.combobox_install_python_ver["values"] = not_ext_python_txt_names
				# Not an installable operating system.
				else:
					self._logger.error("Not an installable operating system.")
					return
				
			except Exception as e:
				self._logger.exception(e)
				return
			# Get PokeCon Versions
			try:
				pokecon_versions_folder = self.setting_path_name.joinpath("PokeCon_Versions")
				pokecon_versions = [f.stem for f in Path(pokecon_versions_folder).glob('*') if f.is_file()]
				self.combobox_select_pokecon_ver["values"] = pokecon_versions

			except Exception as e:
				self._logger.exception(e)
				return
			
		except Exception as e:
			self._logger.exception(e)
			return
		
	def select_folder(self, event=None):
		if self.install_folder_path.get() == "参照":
			self.install_folder_path.set("")
			install_folder_path = filedialog.askdirectory(title="PokeConをインストールする空のフォルダーを選択してください。")
			if install_folder_path == "":
				messagebox.showerror("フォルダー選択エラー","インストール先フォルダーが選択されませんでした。")
				return

			items = os.listdir(install_folder_path)
			if items:
				self._logger.error("")
				messagebox.showerror("フォルダー選択エラー","選択されたフォルダーにはインストールできません。\nインストール先は空のフォルダーを選択してください。")
				self.install_folder_path.set("")
				return
			self.install_folder_path.set(install_folder_path)
			self.input_check()

		else:
			return

	def main(self):
		try:
			self.button_install.configure(state="disabled")
			install_folder_path = Path(self.install_folder_path.get())
			install_pokecon_version = self.select_pokecon_ver.get()
			install_python_ver = self.install_python_ver.get()
			self._logger.info("Get Python Build Standalone URL")
			python_txt_file_path = self.system_path.joinpath(f"{install_python_ver}.txt")
			self._logger.info("Make Download Directry")
			download_folder = install_folder_path.joinpath("download")
			download_folder.mkdir(parents=True)

			with open(python_txt_file_path, "r", encoding="utf-8") as file:
				python_url = file.read()
			res = requests.get(python_url)
			self._logger.info("Start Download Python Standalone Builds")
			if res.status_code == 200:
				python_file_name = download_folder.joinpath("Python_Standalone_Builds.tar.gz")
				with open(python_file_name,"wb") as file:
					for chunk in res.iter_content(chunk_size=4096):
						if chunk:
							file.write(chunk)
				self._logger.info("Download Complete Python Standalone Builds")
			else:
				self._logger.error("Download ERROR")
				return
			self._logger.info("Expand File")
			with tarfile.open(python_file_name, 'r:gz') as tar:
				tar.extractall(path=install_folder_path)

			res_git = self.install_git(install_folder_path,install_pokecon_version)

			if not res_git:
				self.closing()
				return
			
			
			self._logger.info("Start installation of the library in a stand-alone environment")
			lib_res = self.install_libraries(install_folder_path)
			if not lib_res:
				self._logger.error("An error occurred while performing library installation in a standalone environment.")
				return
			
			shutil.rmtree(download_folder)
			self.make_start_bat(install_folder_path,install_pokecon_version)
			
			self._logger.info("The environment has been built.")
			messagebox.showinfo("インストール完了","PokeConの環境構築が完了しました。")
			if messagebox.askyesno("終了確認","終了しますか？"):
				self.mainwindow.destroy()
				self._logger.info("Exit the application.")
				subprocess.run("pause",shell=True)
				self.root.destroy()
				return
			else:
				return
		except Exception as e:
			self._logger.exception(e)
			return

	def read_txt_file(self,path):
		with open(path,"r",encoding="utf-8") as file:
			text = file.read()
		return text
		

	def install_git(self,install_folder_path:Path,install_pokecon_version):
		if self.system_name == "Windows":	
			git_url_file_path = self.setting_path_name.joinpath("Install_Git_For_Windows.txt")
			git_dornload_file_path = install_folder_path.joinpath("download","git_for_windows.exe")
			with open(git_url_file_path,"r",encoding="utf-8") as file:
				git_download_url = file.read()
			git_res = requests.get(git_download_url)
			if git_res.status_code == 200:
				with open(git_dornload_file_path,"wb") as file:
					file.write(git_res.content)
				subprocess.run([git_dornload_file_path,
								"/VERYSILENT", "/NORESTART",
								"/NOCANCEL", "/SP-",
								"/CLOSEAPPLICATIONS",
								"/RESTARTAPPLICATIONS",
								'/COMPONENTS="icons,ext\\reg\shellhere,assoc,assoc_sh"'])

				self._logger.info(f"Start Install {self.select_pokecon_ver.get()}")
				pokecon_txt_file_path = self.setting_path_name.joinpath("PokeCon_Versions").joinpath(f"{install_pokecon_version}.txt")
				pokecon_git = self.read_txt_file(pokecon_txt_file_path)
				self._logger.info(f"Clone {install_pokecon_version}")
				# pokecon_folder_path = install_folder_path.joinpath(install_pokecon_version)
				# pokecon_folder_path.mkdir(parents=True)
				self._logger.info("Get Branch Name")
				branch_file_path = self.setting_path_name.joinpath("Default_Branch.txt")
				branch_name = self.read_txt_file(branch_file_path)
				self._logger.info("Clone Poke-controller from Git.")
				subprocess.run(["git","clone","--recursive","-b",branch_name,pokecon_git],cwd=install_folder_path,shell=True)
				# subprocess.run(["git","pull","origin",branch_name],cwd=pokecon_folder_path,shell=True)
				self._logger.info("Poke-controller cloning is complete.")
				return True
			else:
				self._logger.error("An error occurred when cloning Poke-controller.")
				return False
		else:
			self._logger.info("Git installation and Poke-controller cloning are not supported on this OS.")
			return False

	def install_libraries(self,folder_path:Path):
		try:
			library_txt_path = self.setting_path_name.joinpath("Install_Libraries").joinpath("Default.txt")
			with open(library_txt_path, "r", encoding="utf-8") as file:
				txt_lines = file.readlines()
			library_list = [line.strip() for line in txt_lines]
			base_python_path = folder_path.joinpath("python","python.exe")
			self._logger.debug(str(base_python_path))
			site_package_path = folder_path.joinpath("python","Lib","site-packages")

			self._logger.info("Start the installation of the library")
			if self.system_name == "Windows":
				# full_venv_python_path = base_venv_path.joinpath("Scripts","python.exe") 
				subprocess.run([base_python_path,"-m","pip","install","--upgrade","pip"],cwd=folder_path.parent,shell=True)
				subprocess.run([base_python_path,"-m","pip","install","--upgrade","setuptools"],cwd=folder_path.parent,shell=True)

				for lib in library_list:
					subprocess.run([base_python_path,"-m","pip","install",f"{lib}","-t",str(site_package_path)],cwd=folder_path.parent,shell=True)
				return True

			# else:
			# 	full_venv_python_path = base_venv_path.joinpath("bin","python")
			# 	subprocess.run(f"{full_venv_python_path} -m pip install --upgrade pip",cwd=folder_path.parent,shell=True)
			# 	subprocess.run(f"{full_venv_python_path} -m pip install --upgrade setuptools",cwd=folder_path.parent,shell=True)
			# 	for lib in library_list:
			# 		subprocess.run(f"{full_venv_python_path} -m pip install {lib}",cwd=folder_path.parent,shell=True)
			# 	return True
			
		except Exception as e:
			self._logger.exception(e)
			return False


	def make_start_bat(self,install_folder_path:Path,install_pokecon_version):
		try:
			SerialController_path = install_folder_path.joinpath(install_pokecon_version,"SerialController")
			python_path = install_folder_path.joinpath("python","python.exe")
			if install_pokecon_version == "Poke-Controller-Modified-Extension":
				ext_path = install_folder_path.joinpath("Poke-Controller-Modified-Extension")
				updatechecker = SerialController_path.joinpath("PokeConUpdateChecker.py")
				txt = f"cd {str(ext_path)}\n{str(python_path)} {str(updatechecker)}\ncd {str(SerialController_path)}\nrem python Window.py --profile dragonite\n{str(python_path)} Window.py\npause"
				
				with open(install_folder_path.joinpath("start.bat"),"w",encoding="utf-8") as file:
					file.write(txt)
			else:
				txt = f"cd {str(SerialController_path)}\n{str(python_path)} Window.py\npause"
				with open(install_folder_path.joinpath("start.bat"),"w",encoding="utf-8") as file:
					file.write(txt)
				return True
		except Exception as e:
			self._logger.exception(e)
			return False
		
		


	def input_check(self,event=None):
		self._logger.info("Input Check")
		if self.install_folder_path.get() == "" or self.select_pokecon_ver.get() == "" or self.install_python_ver.get() == "":
			self.button_install.configure(state="disabled")
			return
		else:
			self.button_install.configure(state="enabled")
			self._logger.info("Input Check OK")

	
		





	def closing(self):
		res = messagebox.askyesno("終了確認","終了しますか？")
		if res:
			self.mainwindow.destroy()
			self._logger.info("Installation canceled.")
			subprocess.run("pause",shell=True)
			self.root.destroy()
		else:
			return

	def clear(self):
		self.install_folder_path.set("")
		self.select_pokecon_ver.set("")
		self.install_python_ver.set("")	
		self.button_install.configure(state="disabled")

	
		
	def run(self):
		self.mainwindow.mainloop()


if __name__ == "__main__":
	logger.info("Start Make_PokeCon_Enviroment")

	try:
		app = MainApp()
		app.run()
	except Exception as e:
		logger.exception(e)
		subprocess.run("pause",shell=True)