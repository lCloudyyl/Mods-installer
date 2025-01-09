import os
import zipfile
import shutil
import requests
from colorama import init, Fore, Back
import datetime
import re
from tqdm import tqdm


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

            with tqdm(total=total_size, unit='B', unit_scale=True, desc=name) as pbar:
                for chunk in r.iter_content(chunk_size=2048):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk)) 
                        
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


def backup_choice():
    while True:
        choice = input(
            f"Would you like to create a backup of your current mods folder? {Fore.CYAN}(Type {Fore.WHITE}'yes'/'no'{Fore.CYAN}) \n {Fore.WHITE}>>"
        ).lower()
        if choice in ('yes', 'y'):
            return True
        elif choice in ('no', 'n'):
            return False
        else:
            reset_program()
            print(Fore.RED + "Invalid input. Type 'yes' or 'no'.")


def create_backup(mod_folder, backup_zip):
    try:
        with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(mod_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    name = os.path.relpath(file_path, start=mod_folder)
                    zipf.write(file_path, name)
        print("Backup finished.")
    except Exception as e:
        print(f"Error occurred during backup: {e}")


def backup_mods():
    if backup_choice():
        if os.path.isdir(mod_folder):
            backup_zip = backup_path()
            create_backup(mod_folder, backup_zip)
        else:
            print("No mods folder to back up...")
    else:
        print("Backup canceled.")


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

def path_check(new_path, task):
    if os.path.isdir(new_path):
        reset_program()
        print(f"{Fore.GREEN}{task} changed to {new_path}")
        return True
    else:
        reset_program
        print(f"{Fore.RED}You sent an invalid path: {new_path}")
        new_path_q = input(f"Would you like to create {new_path} \n >> ")

        if path_creation(new_path, new_path_q):  
            reset_program()
            print(f"{Fore.CYAN}Created path: {new_path}")
            print(f"{Fore.GREEN}{task} changed to {new_path}")
            return True
        else:
            print(f"{Fore.YELLOW}Path creation canceled.")
            return False

def path_creation(new_path, new_path_q):
    if new_path_q.lower() in ('yes', 'y'):
        try:
            os.mkdir(new_path)
            return True
        except OSError as e:
            print(f"{Fore.RED}OS error while creating directory(ERR:{e})")
            return False

    elif new_path_q.lower() in ('no', 'n'):
        return False

    else:
        print(f"{Fore.YELLOW}Invalid input. Path creation canceled.")
        return False


def file_info(headers):

    cd = headers.get('content-disposition')

    if not cd:
        return None, 0
    
    fname_match = re.findall(r'filename="?([^";]+)"?', cd)
    filename = fname_match[0].strip() if fname_match else None

    if not filename:
        return None, 0

    size = int(headers.get('Content-Length', 0))

    return filename, size


def link_valid(link):
    pattern = re.compile(
        r'^(https?:\/\/)?'
        r'(www\.)?'
        r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        r'(\/[^\s]*)?$'
    )
    return bool(pattern.match(link))


def link_request(link, task):
    print("Checking link")

    try:
        response = requests.get(link)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()

            if 'application/' in content_type:
                filename, size = file_info(response.headers)
                reset_program()
                print(f"{Fore.GREEN} Found the download! \n {Fore.WHITE}File_name: {filename} \n Size: {round((size/1000000), 2)} MB")
                choice = input(f"Would you like to change {task} to {link} \n >> ")

                if choice.lower() in ('yes', 'y'):
                    reset_program()
                    print(f"{Fore.GREEN}URL updated to: {Fore.WHITE}{link}")
                    return True
                else:
                    reset_program()
                    print(f"{Fore.RED}Canceled. {task} unchanged.")
                    return False
            else:
                reset_program()
                print(f"{Fore.RED} You sent an invalid link. {task} unchanged.")
        else:
            reset_program()
            print(f"{Fore.RED}Download link is accessible, but something is not right (ERR: {response.status_code})  {task} unchanged.")

    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        reset_program()
        print(f"{Fore.RED}Failed to access download link (ERR: {e})  {task} unchanged.")
    except Exception as e:
        reset_program()
        print(f"{Fore.RED}Unexpected error (ERR:{e})  {task} unchanged.")    
    return False

def link_check(new_link, task):
    if link_valid(new_link):
        if link_request(new_link, task):
            return True
        else:
            return False
    else:
        reset_program()
        print(f"{Fore.RED}{task} UNCHANGED: Invalid link sent: {Fore.WHITE}{new_link}")
        return False


def const_editing():
    global zip_url, mod_folder, backup_folder, installer_path, installer_link

    def inputs(task):
        reset_program()
        edit = input(f"Send the new {task}")
        return edit
    
    while True:
        try:
            edit_const = listing_consts()

            if edit_const == "1":
                task = "Mods URL"
                edit = inputs(task)
                if link_check(edit, task):
                    zip_url = edit
                break

            elif edit_const == "2":
                task = "Mods folder"
                edit = inputs(task)
                if path_check(edit, task):
                    mod_folder = edit
                break

            elif edit_const == "3":
                task = "Backup folder"
                edit = inputs(task)
                if path_check(edit, task):
                    backup_folder = edit
                break

            elif edit_const == "4":
                task = "Installer location"
                edit = inputs(task)
                if path_check(edit, task):
                    installer_path = edit
                break

            elif edit_const == "5":
                task = "Installer link"
                edit = inputs(task)
                if link_check(edit, task):
                    installer_link = edit
                break

            elif edit_const == "6":
                reset_program()
                print("Exiting...")
                break

            else:
                reset_program()
                print("Invalid option. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")

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
                    print(Back.RED + "On the installer change version to 1.20.1, then 'install' DONT CHANGE SHIT ELSE \n")

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

