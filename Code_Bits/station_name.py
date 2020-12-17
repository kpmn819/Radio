def station_name():
    white = (255,255,255)
    green = (0,255,0)
    red = (255,0,0)
    ##### display the station name and split it into 2 parts : 
    lines = subprocess.check_output("mpc current", shell=True).split("-")
    if len(lines)==1:
        line1 = lines[0]
        line1 = line1[:-1]
        line2 = " No additional info: "
    else:
        line1 = lines[0]
        line2 = lines[1]

    line1 = line1[:38]
    line2 = line2[1:38]
    line2 = line2[:-1]
    #trap no station data
    if line1 =="":
        line2 = "Press PLAY"
        station_status = "Stopped"
        status_font = red
    else:
        station_status = "Playing"
        status_font = green

    station_name=station_font.render(line1, 1, (white))
    additional_data=station_font.render(line2, 1, (white))
    station_label=font.render(station_status, 1, (status_font))
    screen.blit(station_label,(250,190)) #playing
    screen.blit(station_name,(70,350))
    screen.blit(additional_data,(70,287))