cities = {
        "san francisco": {"neighbours": {"los angeles": 100, "salt lake city": 156, "portland": 151}, "sld": 499},
        "portland": {"neighbours": {"san francisco": 151, "salt lake city": 175, "seattle": 44}, "sld": 452},
        "seattle": {"neighbours": {"portland": 44, "vancouver": 45, "calgary": 118, "helena": 189}, "sld": 434},
        "vancouver": {"neighbours": {"calgary": 100, "seattle": 45}, "sld": 432},
        "los angeles": {"neighbours": {"san francisco": 100, "las vegas": 66, "phoenix": 109, "el paso": 191}, "sld": 484},
        "las vegas": {"neighbours": {"los angeles": 66, "salt lake city": 89}, "sld": 418},
        "calgary": {"neighbours": {"vancouver": 100, "seattle": 118, "helena": 130, "winnipeg": 180}, "sld": 334},
        "salt lake city": {"neighbours": {"portland": 175, "san francisco": 156, "las vegas": 89, "denver": 101, "helena": 116}, "sld": 344},
        "phoenix": {"neighbours": {"los angeles": 109, "denver": 128, "santa fe": 85}, "sld": 396},
        "helena": {"neighbours": {"seattle": 189, "calgary": 130, "winnipeg": 137, "duluth": 150, "omaha": 174, "denver": 126, "salt lake city": 116}, "sld": 254},
        "denver": {"neighbours": {"salt lake city": 101, "helena": 126, "omaha": 130, "kansas city": 135, "santa fe": 70, "phoenix": 128}, "sld": 270},
        "santa fe": {"neighbours": {"phoenix": 85, "denver": 70, "oklahoma city": 121, "el paso": 65}, "sld": 318},
        "el paso": {"neighbours": {"los angeles": 191, "santa fe": 65, "dallas": 140}, "sld": 370},
        "winnipeg": {"neighbours": {"calgary": 180, "helena": 137, "duluth": 103, "sault ste marie": 156}, "sld": 156},
        "duluth": {"neighbours": {"helena": 150, "winnipeg": 103, "sault ste marie": 110, "chicago": 157, "omaha": 74}, "sld": 110},
        "omaha": {"neighbours": {"helena": 174, "duluth": 74, "chicago": 142, "denver": 130}, "sld": 150},
        "oklahoma city": {"neighbours": {"santa fe": 121, "kansas city": 61, "little rock": 72}, "sld": 237},
        "kansas city": {"neighbours": {"denver": 135, "saint louis": 68, "oklahoma city": 61}, "sld": 176},
        "dallas": {"neighbours": {"el paso": 140, "little rock": 74, "houston": 46}, "sld": 303},
        "houston": {"neighbours": {"dallas": 46, "new orleans": 80}, "sld": 332},
        "little rock": {"neighbours": {"oklahoma city": 72, "saint louis": 60, "nashville": 94, "new orleans": 100, "dallas": 74}, "sld": 240},
        "saint louis": {"neighbours": {"kansas city": 68, "chicago": 104, "nashville": 85, "little rock": 60}, "sld": 180},
        "sault ste marie": {"neighbours": {"winnipeg": 156, "montreal": 193, "toronto": 90, "duluth": 110}, "sld": 0},
        "new orleans": {"neighbours": {"houston": 80, "little rock": 100, "atlanta": 120, "miami": 151}, "sld": 322},
        "chicago": {"neighbours": {"omaha": 142, "duluth": 157, "pittsburgh": 81, "saint louis": 104}, "sld": 107},
        "nashville": {"neighbours": {"saint louis": 85, "raleigh": 128, "atlanta": 67, "little rock": 94}, "sld": 221},
        "toronto": {"neighbours": {"sault ste marie": 90, "montreal": 115, "pittsburgh": 80}, "sld": 90},
        "pittsburgh": {"neighbours": {"chicago": 81, "toronto": 80, "new york": 69, "washington": 85}, "sld": 152},
        "atlanta": {"neighbours": {"nashville": 67, "raleigh": 96, "charleston": 63, "miami": 116, "new orleans": 120}, "sld": 272},
        "montreal": {"neighbours": {"sault ste marie": 193, "toronto": 115, "new york": 99, "boston": 69}, "sld": 193},
        "miami": {"neighbours": {"new orleans": 151, "atlanta": 116, "charleston": 80}, "sld": 389},
        "charleston": {"neighbours": {"atlanta": 63, "raleigh": 95, "miami": 80}, "sld": 322},
        "raleigh": {"neighbours": {"nashville": 128, "washington": 47, "charleston": 95, "atlanta": 96}, "sld": 251},
        "new york": {"neighbours": {"pittsburgh": 69, "montreal": 99, "boston": 74, "washington": 76}, "sld": 195},
        "washington": {"neighbours": {"pittsburgh": 85,  "new york": 76, "raleigh": 47}, "sld": 238},
        "boston": {"neighbours": {"montreal": 69, "new york": 74}, "sld": 240},
        }