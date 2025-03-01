#! /usr/bin/env python3
from setup import *

# Read ini file
config = configparser.ConfigParser()
config.read(src_user_config)


class BACKUP:
    def __init__(self):
        ################################################################################
        ## Commands
        ################################################################################
        self.createCmd = "mkdir"
        self.createFile = "touch"

        try:
            ################################################################################
            ## Get hour, minute
            ################################################################################
            self.dateTime = datetime.now()
            self.dateDay = self.dateTime.strftime("%d")
            self.dateMonth = self.dateTime.strftime("%m")
            self.dateYear = self.dateTime.strftime("%y")
            self.dayName = self.dateTime.strftime("%a")
            self.currentHour = self.dateTime.strftime("%H")
            self.currentMinute = self.dateTime.strftime("%M")

            ################################################################################
            ## Get user.ini
            ################################################################################
            self.getExternalLocation = config['EXTERNAL']['hd']
            self.getHDName = config['EXTERNAL']['name']
            self.getIniFolders = config.options('FOLDER')
            self.backupNowChecker = config['BACKUP']['backup_now']
            self.oneTimeMode = config['MODE']['one_time_mode']

            ################################################################################
            ## Create folders
            ################################################################################
            self.createTMB = f"{self.getExternalLocation}/{folderName}"
            self.dateFolder = f"{self.createTMB}/{self.dateDay}-{self.dateMonth}-{self.dateYear}"
            self.timeFolder = f"{self.createTMB}/{self.dateDay}-{self.dateMonth}-{self.dateYear}/{self.currentHour}-{self.currentMinute}"

            ################################################################################
            ## Apt txt file
            ################################################################################
            # self.apt_txt = f"{self.getExternalLocation}/{folderName}/apt.txt"

            ################################################################################
            ## Flatpak txt file
            ################################################################################
            # self.flatpak_txt = f"{self.getExternalLocation}/{folderName}/flatpak.txt"

            self.create_TMB()

        except KeyError:
            ################################################################################
            ## Set notification_id to 5
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "5")
                config.write(configfile)

            print("Error trying to read user.ini!")
            sub.run(f"python3 {src_notification}", shell=True)  # Call notification

            exit()

    def create_TMB(self):
        ################################################################################
        ## Create TMB
        ################################################################################
        if self.backupNowChecker == "true":  # Read user.ini
            try:
                if os.path.exists(self.createTMB):
                    print("TMB folders inside external, already exist.")
                else:
                    print("TMB folder inside external, was created.")
                    sub.run(f"{self.createCmd} {self.createTMB}", shell=True)

            except FileNotFoundError:
                ################################################################################
                ## Set notification_id to 4
                ################################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'notification_id', "4")
                    config.write(configfile)

                print("Error trying to create TMB...")
                sub.run(f"python3 {src_notification}", shell=True)  # Call notification

                exit()
        else:
            print("Nothing to do right now...")
            exit()

        # self.create_apt_file()

        # def create_apt_file(self):
        #     ################################################################################
        #     ## Create file txt
        #     ################################################################################
        #     try:
        #         if os.path.exists(self.apt_txt):
        #             print("Apt file already exist.")
        #         else:
        #             print("Apt file was created.")
        #             sub.run(f"{self.createFile} {self.apt_txt}", shell=True)    # Create tmb folder
        #
        #     except FileNotFoundError:
        #         print("Error trying to create Apt file...")
        #         error_backup()  # Notification
        #         exit()
        #
        #     self.create_flatpak_file()

        # def create_flatpak_file(self):
        #     ################################################################################
        #     ## Create file txt
        #     ################################################################################
        #     try:
        #         # TMB folders
        #         if os.path.exists(self.flatpak_txt):
        #             print("Flatpak file already exist.")
        #         else:
        #             print("Flatpak file was created.")
        #             sub.run(f"{self.createFile} {self.flatpak_txt}", shell=True)    # Create tmb folder
        #
        #     except FileNotFoundError:
        #         print("Error trying to create Flatpak file...")
        #         error_backup()  # Notification
        #         exit()

        # self.save_apt_file()

        # def save_apt_file(self):
        #     ################################################################################
        #     ## Commands
        #     ################################################################################
        #     x = os.popen("apt-mark showmanual")
        #
        #     ################################################################################
        #     ## Save to file
        #     ################################################################################
        #     list = []
        #     for _ in x:
        #         list.append(x.readline())
        #
        #     try:
        #         with open(f"{self.getExternalLocation}/{folderName}/apt.txt", "w") as write_file:
        #             for i in list:
        #                 if not i.startswith(exclude):
        #                     write_file.write(i)
        #
        #         ################################################################################
        #         ## Read to file
        #         ################################################################################
        #         with open(f"{self.getExternalLocation}/{folderName}/apt.txt", "r") as read_file:
        #             try:
        #                 for i in read_file:
        #                     print(i.strip())
        #             except:
        #                 pass  # Add do error list to install
        #     except:
        #         print("Error tying to save apt list of apps to the file!")
        #         exit()
        #
        #     self.save_flatpak_file()

        # def save_flatpak_file(self):
        #     ################################################################################
        #     ## Commands
        #     ################################################################################
        #     x = os.popen("flatpak list -a --columns=application --app")
        #
        #     ################################################################################
        #     ## Save to file
        #     ################################################################################
        #     list = []
        #     for _ in x:
        #         list.append(x.readline())
        #
        #     try:
        #         with open(f"{self.getExternalLocation}/{folderName}/flatpak.txt", "w") as write_file:
        #             for i in list:
        #                 if not i.startswith(exclude):
        #                     write_file.write(i)
        #
        #         ################################################################################
        #         ## Read to file
        #         ################################################################################
        #         with open(f"{self.getExternalLocation}/{folderName}/flatpak.txt", "r") as read_file:
        #             try:
        #                 for i in read_file:
        #                     print(i.strip())
        #             except:
        #                 pass  # Add do error list to install
        #     except:
        #         print("Error trying to save flatpak list of apps to the file!")
        #         exit()

        self.check_size()

    def check_size(self):
        print("Checking size of folders...")
        ################################################################################
        ## Get folders size
        ################################################################################
        checkSizeList = []
        for output in self.getIniFolders:  # Get folders size before back up to external
            output = output.title()  # Capitalize first letter. ex: '/Desktop'
            print(f"Check this folder size: {output}")

            # getSize = os.popen(f"df --output=size {home_user}/{output}")
            # getSize = getSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
            #     "\n", "").replace(" ", "")
            # getSize = int(getSize)
            # print(getSize)
            # checkSizeList.append(getSize)  # Add to list

            getSize = os.popen(f"du -s {homeUser}/{output}")
            getSize = getSize.read().strip("\t").strip("\n").replace(f"{homeUser}/{output}", "").replace("\t", "")
            print(getSize)
            getSize = int(getSize)
            checkSizeList.append(getSize)  # Add to list

        totalFoldersSize = sum(checkSizeList)  # Sum of all folders (size)
        print(checkSizeList)

        ################################################################################
        ## Get external maximum size
        ################################################################################
        externalMaxSize = os.popen(f"df --output=size {self.getExternalLocation}")
        externalMaxSize = externalMaxSize.read().strip().replace("1K-blocks", "").replace("Size", "").replace(
            "\n", "").replace(" ", "")
        externalMaxSize = int(externalMaxSize)

        ################################################################################
        ## Get external used space
        ################################################################################
        usedSpace = os.popen(f"df --output=used {self.getExternalLocation}")
        usedSpace = usedSpace.read().strip().replace("1K-blocks", "").replace("Used", "").replace(
            "\n", "").replace(" ", "")
        usedSpace = int(usedSpace)

        freeSpace = int(externalMaxSize - usedSpace)
        print("All folders size sum : ", totalFoldersSize)
        print("External maximum size:   ", externalMaxSize)
        print(f"External used space:   ", usedSpace)
        print("External free size:   ", freeSpace)

        ################################################################################
        ## Condition
        ################################################################################
        if totalFoldersSize >= freeSpace:
            print("Not enough space for new backup!")
            print("Old files will be deleted, to make space for the new ones.")
            print("Please wait...")

            ################################################################################
            ## Get available dates inside TMB
            ################################################################################
            try:
                dateFolders = []
                for output in os.listdir(f"{self.getExternalLocation}/{folderName}"):
                    if not "." in output:
                        dateFolders.append(output)
                        dateFolders.sort(reverse=True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

                print(f"Date available: {dateFolders}")

                ################################################################################
                ## Delete oldest folders
                ################################################################################
                if len(dateFolders) > 1:  # Only deletes if exist more than one date folder inside
                    print(f"Deleting {self.getExternalLocation}/{folderName}/{dateFolders[-1]}...")
                    sub.run(f"rm -rf {self.getExternalLocation}/{folderName}/{dateFolders[-1]}", shell=True)

                    if totalFoldersSize >= freeSpace:  # Return if free space is still not enough to continue
                        self.check_size()

                    else:
                        self.create_folder_date()

                else:  # Only delete if one or more date folder is inside
                    ################################################################################
                    ## Set notification_id to 7
                    ################################################################################
                    with open(src_user_config, 'w') as configfile:
                        config.set('INFO', 'notification_id', "7")
                        config.write(configfile)

                    print("Please, manual delete file(s)/folder(s) inside your external HD/SSD, to make space for Time Machine's backup!")
                    sub.run(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification

                    exit()

            except FileNotFoundError:
                ################################################################################
                ## Set notification_id to 6
                ################################################################################
                with open(src_user_config, 'w') as configfile:
                    config.set('INFO', 'notification_id', "6")
                    config.write(configfile)

                print("Error trying to delete old backups!")
                sub.run(f"python3 {src_notification}", shell=True)  # Call notificationnot_available_notification()  # Call not available notification

                exit()

        else:
            print("External has space enough to continue.")
            self.create_folder_date()

    def create_folder_date(self):
        print("Creating folders with dates...")
        ################################################################################
        ## Create folder with date
        ################################################################################
        try:
            if os.path.exists(self.dateFolder):
                pass
            else:
                sub.run(f"{self.createCmd} {self.dateFolder}", shell=True)  # Create folder with date

        except FileNotFoundError:
            ################################################################################
            ## Set notification_id to 4
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "4")
                config.write(configfile)

            print("Error trying to create TMB...")
            sub.run(f"python3 {src_notification}", shell=True)  # Call notification

            exit()

        self.create_folder_time()

    def create_folder_time(self):
        print("Creating folders with time...")
        ################################################################################
        ## Create folder with time
        ################################################################################
        try:
            if os.path.exists(self.timeFolder):
                pass
            else:
                sub.run(f"{self.createCmd} {self.timeFolder}", shell=True)

        except FileNotFoundError:
            ################################################################################
            ## Set notification_id to 4
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "4")
                config.write(configfile)

            print("Error trying to create TMB...")
            sub.run(f"python3 {src_notification}", shell=True)  # Call notification

            exit()

        self.start_backup()

    def start_backup(self):
        print("Starting backup...")
        ################################################################################
        ## Start with the backup
        ## One Time Mode
        ################################################################################
        try:
            if self.oneTimeMode == "true":
                print("One mode activated!")

            ################################################################################
            ## More Time Mode
            ################################################################################
            else:
                print("More mode activated!")
                sub.run(f"{self.createCmd} {self.timeFolder}", shell=True)  # Create folder with date and time

            ################################################################################
            ## Start with the backup
            ################################################################################
            for output in self.getIniFolders:  # Backup all (user.ini true folders)
                output = output.title()  # Capitalize first letter. ex: '/Desktop'
                print(f"Backing up: {output}")
                sub.run(f"{copyCmd} {homeUser}/{output} {self.timeFolder}", shell=True)  # Ex: TMB/date/time/Desktop
                print("")

        except FileNotFoundError:
            ################################################################################
            ## Set notification_id to 4
            ################################################################################
            with open(src_user_config, 'w') as configfile:
                config.set('INFO', 'notification_id', "4")
                config.write(configfile)

            print("Error trying to back up folders to external location...")
            sub.run(f"python3 {src_notification}", shell=True)  # Call notification

            exit()

        self.end_backup()

    def end_backup(self):
        print("Ending backup...")
        ################################################################################
        ## Set backup_now to "false", backup_running to "false" and Update "last backup"
        ################################################################################
        with open(src_user_config, 'w') as configfile:
            config.set('BACKUP', 'backup_now', 'false')
            config.set('BACKUP', 'checker_running', 'false')
            config.set('INFO', 'latest', f'{self.dayName}, {self.currentHour}:{self.currentMinute}')
            config.set('INFO', 'notification_id', "2")
            config.write(configfile)

        ################################################################################
        ## After backup is done
        ################################################################################
        sub.run(f"python3 {src_notification}", shell=True)
        print("Backup is done!")

        print("Waiting 60 seconds...")
        time.sleep(60)  # Wait 60, so if finish fast, won't repeat the backup :D

        sub.Popen(f"python3 {src_backup_check_py}", shell=True)

        exit()


main = BACKUP()
