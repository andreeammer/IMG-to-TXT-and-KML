import os
import subprocess

#https://exiftool.org or
#https://oliverbetz.de/pages/Artikel/ExifTool-for-Windows#toc-3
#Find the neccesary kml.fmt file for the geolocation tool (somewhere on GitHub)

#Header
header = 'Failinimi;Laiuskraad;Pikkuskraad;Kõrgus\n'

# Get the current working directory
current_directory = os.getcwd()

# Change directory command
change_directory_cmd = f'cd /d {current_directory}'

# Run the change directory command
subprocess.run(change_directory_cmd, shell=True)

# Command to create KML file using Exiftool
exiftool_cmd = 'exiftool -E -p kml.fmt Images > ImagesGeoLocation.kml'

# Run the Exiftool command to create the KML file
subprocess.run(exiftool_cmd, shell=True)

# Command to extract GPS coordinates using Exiftool and output formatted coordinates to a text file
extract_coordinates_cmd = 'exiftool -T -c "%.6f" -p "${Filepath};${GPSLatitude};${GPSLongitude};${GPSAltitude}" Images > coordinates.txt'

# Run the command to extract GPS coordinates and save them to a text file
subprocess.run(extract_coordinates_cmd, shell=True)

# Read the contents of the txt file
with open('coordinates.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Process each line and remove 'N' from Latitude and 'E' from Longitude
for i in range(1, len(lines)):
    parts = lines[i].split(';')
    latitude = parts[1].replace(' N', '')
    longitude = parts[2].replace(' E', '')
    altitude = parts[3].replace(' m Above Sea Level', '')
    lines[i] = f'{parts[0]};{latitude};{longitude};{altitude}'

# Insert the header at the beginning of the file
lines.insert(0, header)

# Write the updated lines back to the txt file
with open('coordinates.txt', 'w', encoding='utf-8') as file:
    file.writelines(lines)

    
