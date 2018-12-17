# Cura-Tools

## Cura Profile Modifier ##

-----------------------------------------------------
### INSTRUCTIONS ###

1. Run CuraProfileModification.py

2. Copy and paste directory (this will not appear if there is a Cura_Directory file in the Cura-Tools folder)

   This window will ask you to put the directory of the Cura software that you use. In order to get this information:

	* Open up Cura
	* Click on the "help" tab on the top left of the screen
	* Click on "show configuration folder"
	* The directory of your Cura files is in the bar in the upper right area. Click on it, and copy and paste it into the entry
		(eg. C:\Users\Students\AppData\Roaming\cura\3.6)
	* A Cura_Directory file should appear in the folder, this is for the program to easily access the directory without needing
		to ask every time the program is run. Deleting this file will only make you input the information once again.

-----------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------
## Cura Importer ##

This program will allow you to import large amounts of materials and profiles at once to Cura from the folder produced by 
CuraExporter.exe. In addition, this program is capable of importing newer versions of materials and profiles, and importing them into
older versions of Cura. This document will show you the details of how to use this program properly, and presenting important details
to notice.


Notes:
* You will need to close Cura for Cura to display the changes on the program. No errors will arise from not closing Cura, it just will not update.
* This program cannot read exported Cura files, it can only make use of folders which contain files organized into "profiles" and "materials", which CuraExporter.exe generates. Implementing the ability to read Cura files would be next to impossible
* This program is not as simple as putting the exported files from CuraExporter.exe into the Cura directory, as doing so is very likely to not work or even lead to corruption when bringing newer files to older versions of Cura, and it will not be able to cope with overlapping names or file names.
* This program can only read files that are placed in the folder where this program is, in Cura-Tools. Please place exported files into the Cura-Tools folder so that they can be properly used.
		
-----------------------------------------------------------------------------------------------------------------------------------

### INSTRUCTIONS ###

1. Run CuraImporter.py

2. Copy and paste directory (this will not appear if there is a Cura_Directory file in the Cura-Tools folder)

   * *the same instructions apply here as in step 2 in Cura Profile Modifier.*

3. Please input the name of the folder you would like to import.

	* Put the EXPORTED CuraFiles #N folder (or whatever the exported folder has been named to) into the Cura-Tools folder
	* Input the name of the folder, eg. EXPORTED CuraFiles #0
	* Pressing import, will close the program, make sure that the folder contains the right files

If Cura is already closed, you may open it Cura should display the changes. If Cura has been open the whole time, restart Cura and
the same will happen.

-----------------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------------
## Cura Exporter ##

The goal of this program is that it allows you to easily export large amounts of files at once, and with CuraImporter.exe, can get
those files to any computer. This document will show you the details of how to use this program properly, and presenting important
details to notice.


Notes:
* Cura itself cannot import files exported by this program, that is what the CuraImporter.exe is for
* If you have a Cura_directory file in this folder, do not modify it for safety. If you have changed Cura versions or if you have changed the Cura location, please delete the file and you can input the new information when you next run one of the three programs
* Changing options by pressing "Back" is always an option, so there is no need to exit out of the program if you inputted something wrong.

-----------------------------------------------------------------------------------------------------------------------------------

### INSTRUCTIONS ###

1. Run CuraExporter.py

2. Copy and paste directory

   * *the same instructions apply here as in step 2 in Cura Profile Modifier.*
   
3. Export Material or profile settings?

	* Check of whether you want to export materials, profiles or both.

4. Select which profile you would like to export (if you did not click on the "profile" option in the previous window, you will not
	see this window)

	* Check off all of the profiles you want to export
	* The entries beside each of the check boxes are there if you want to rename a profile. Checking off a profile and inputting
		a name in the entry directly to the right of it will, when imported, change the name of the profile
	* Any entry whose check box has not been selected will be ignored

5. Select which materials you would like to export (if you did not click on the "materials" option in window 4, you will not see this
	window)

	* The same instructions apply as above, in step 4

6. Please input the directory where you want to export

	* If you have a USB or a specific directory, such as a location on a sever, which you want to export these files to, input
		the directory here. (eg. N:\Co-op Students)
	* Inputting nothing into the entry will create a file in the Cura-Tools folder, where this is.

The exported file will be named "EXPORTED CuraFiles #N", where N changes so that the folders do not have the same name. You may 
change the name of this folder if needed, as in CuraImporter.exe you will be prompted to input the name of this folder.

-----------------------------------------------------------------------------------------------------------------------------------

If you have any questions or if you have a problem or recommmendation to the program, contact me at jekambulow1819@gmail.com .

