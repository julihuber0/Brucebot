"""

rewrite of setlist finder function, clean it up and add some better error handling
# means new step
add step to bail out if setlist empty BUT event exists, just send "no set details known"

steps in order:

#    in setlist function - set default date to latest in database

    check inputted date (passes to date_checker, makes sure date is proper "YYYY-MM-DD" format)
        if date:
            check if date is in database
                if yes, continue
                if no, exit and send "show not found" error

            loop dates returned from db
                select all in events matching date, don't need id but rest is good

                using location_url, pass to location_name_get function, return location name
                    if early/late show, append that to location string: (Early/Late/Whatever)
                    add to embed with date and url
                    set_footer with tour

#               check setlist table for url
                    if yes: continue
                    if no: send "no set details known"

                select all set_types - command sucks but its postgres fuckery (change * to just set_type)
                    for each set
                        get all songs/url/segue from setlist table matching set type
                            check if premiere (event_url matches first_played in song table)
                            check if tour debut (get first date from events with song and matching tour)

                            if premiere_date == event_date
                                check if segue
                                    append [SONG] [1] >
                                else
                                    append [SONG] [1]
                            if bustout_date == event_date
                                check if segue
                                    append [SONG] [2] >
                                else
                                    append [SONG] [2]
                            else:
                                check if segue
                                    append [SONG] >
                                else
                                    append [SONG]
                        
                        set = ", ".join(list) replace >, with >

                        check if bootleg/livedl (either 1 or 0 in events)
                            set both to "no"
                            add "yes" to Bootleg: and/or Official Release:
                                maybe add under date like JerryBase?
                
        if not date
            send incorrect date format error

    

"""