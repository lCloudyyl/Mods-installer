import os
import zipfile
import shutil
import requests
from colorama import init, Fore, Back
import datetime
import time

init(autoreset=True)

zip_url = "https://github.com/lCloudyyl/Mod-pack/releases/latest/download/mods.zip"
mod_folder = os.path.expandvars(r'%appdata%\.minecraft\mods')
zip_file = os.path.join(mod_folder, "mods.zip")
backup_folder = os.path.expandvars(r'%appdata%\.minecraft')
installer_path = os.path.expandvars(r"%userprofile%\Downloads\fabric-installer-1.0.1.exe")
installer_link = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.1/fabric-installer-1.0.1.exe"


def file_downloading(link, path, name):
    r = requests.get(link, stream=True, timeout=30)
    r.raise_for_status()

    total_size = int(r.headers.get('content-length', 0))
    downloaded_size = 0

    try:
        print(f"{Fore.GREEN}Downloading {link}{Fore.WHITE} to {Fore.GREEN}{path}")
        with open(path, 'wb') as file:
            for chunk in r.iter_content(chunk_size=2048):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    percent_done = (downloaded_size / total_size) * 100 if total_size else 0
                    print(f"Progress for {name}: {percent_done:.2f}%", end="\r")
        print(f"\n Done downloading {name}.")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file: {e}")
    except IOError as e:
        print(f"Failed to write {name} to disk: {e}. Check for user perms, run mods_installer as admin if needed.")

    except Exception as e:
        print(f"Honestly, I don't know how you managed to get here...: {e}")
    return False


def folder_check():

    try:
        if os.path.isdir(mod_folder):
            shutil.rmtree(mod_folder)
        os.mkdir(mod_folder)
        print(f"Mods folder reset.")

    except Exception as e:
        print(f"Failed clear folder. {e}")


def extraction():
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(mod_folder)
            print("Mods extracted.")
    except FileNotFoundError:
        print("The mods file did not download properly.")
    except zipfile.BadZipFile:
        print("Zipfile corrupted.")
        delete()
    return False


def delete():
    if os.path.exists(zip_file):
        os.remove(zip_file)


def user_choice():
    print("Choose an option:")
    print("1. Update your mods (If you've already played modded)")
    print("2. Full installation (If you've never played the modded version.)")
    print("3. Change links or paths.")
    print(Fore.GREEN+"4. Reset menu")
    print(Fore.RED+"5. Exit")

    choice = input("What would you like to do? (Type '1','2', etc then press enter.) \n >>")
    return choice


def open_installer():
    if os.path.isfile(installer_path):
        os.startfile(installer_path)
    else:
        print("The fabric installer did not install properly...")


def full_install():
    link = installer_link
    path = installer_path
    name = "Fabric Installer"

    file_downloading(link, path, name)
    mods_only()
    open_installer()


def mods_only():
    link = zip_url
    path = zip_file
    name = "Mods"

    file_downloading(link, path, name)

    extraction()

def backup_path():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_zip = os.path.join(backup_folder, f"old_mods_{timestamp}.zip")
    print(Back.GREEN + f"Backing up old mods to: {backup_zip}")
    return backup_zip

def backup_mods():
    while True:
        choice = input(f"Would you like to create a backup of your current mods folder? {Fore.CYAN}(Type {Fore.WHITE}'yes'/'no'{Fore.CYAN}) \n {Fore.WHITE}>>")

        if choice.lower() == 'yes' or choice.lower() == 'y':
            if os.path.isdir(mod_folder):
                backup_zip = backup_path()
                try:
                    with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for root, dirs, files in os.walk(mod_folder):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, start=mod_folder)
                                zipf.write(file_path, arcname)
                    print("Backup finished.")
                    break
                except Exception as e:
                    print(f"Error occurred, send to my dms: {e}")
            else:
                print("No mods folder to back up...")
                break
        elif choice.lower() == 'no' or choice.lower() == 'n':
            print("Backup canceled.")
            break
        else:
            reset_program()
            print(Fore.RED + "Invalid input. Type 'yes' or 'no'.")
            continue


def mods_folder_safety():
    folder_check()


def reset_program():
    os.system('clear')

def listing_consts():
    print(f"1. Mods url = {zip_url}")
    print(f"2. Mods folder = {mod_folder}")
    print(f"3. Backup folder = {backup_folder}")
    print(f"4. Installer save location = {installer_path}")
    print(f"5. Installer link = {installer_link}")
    print(Fore.GREEN+"6. Go back.")

    edit_const = input("What would you like to edit? (Type '1','2', etc then press enter.) \n >> ")

    return edit_const

def const_editing():
    global zip_url, mod_folder, backup_folder, installer_path, installer_link

    edit_const = listing_consts()

    while True:
        try:
            if edit_const == "1":
                new_url = input("Send the new URL for mods. \n >> ")
                zip_url = new_url
                break
            elif edit_const == "2":
                new_mod_folder = input("Send the new mods folder path. \n >> ")
                mod_folder = new_mod_folder
                break
            elif edit_const == "3":
                new_backup_folder = input("Send the new backup folder path. \n >> ")
                backup_folder = new_backup_folder
                break
            elif edit_const == "4":
                new_installer_path = input("Send the new installer save location. \n >> ")
                installer_path = new_installer_path
                break
            elif edit_const == "5":
                new_installer_link = input("Send the new installer link. \n >> ")
                installer_link = new_installer_link
                break
            elif edit_const == "6":
                reset_program()
                print("Exiting...")
                break
        except Exception as e:
            print(f"an error occured: {e}")

    return zip_url, mod_folder, backup_folder, installer_path, installer_link

def main():
    try:
        while True:
            choice = user_choice()

            if choice == "1" or choice == "2":
                reset_program()
                backup_mods()


                if choice == "1":
                    mods_folder_safety()
                    mods_only()
                    delete()
                    reset_program()
                elif choice == "2":
                    mods_folder_safety()
                    full_install()
                    delete()
                    reset_program()
                    print(Back.RED + "On the installer change version to 1.20.1, then 'install' DONT CHANGE SHIT ELSE")
                    print("")

            elif choice == "3":
                reset_program()
                const_editing()

            elif choice == "4":
                reset_program()

            elif choice == "5":
                break

            else:
                reset_program()
                print(Fore.RED+"option does not exist.")

    except KeyboardInterrupt:
        print("\n dont do that")
        return
    except Exception as e:
        print(f"I dont know what you did but: {e}")
        return
        


if __name__ == "__main__":
    main()

