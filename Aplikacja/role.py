

CHAMPION_WHITELIST = {
    'TOP': [
        "Aatrox", "Akali", "Briar", "Camille", "ChoGath", "Darius", "DrMundo", "Fiora", 
        "Gangplank", "Garen", "Gnar", "Gragas", "Gwen", "Illaoi", "Irelia", 
        "Jax", "Jayce", "Kayle", "Kennen", "Kled", "KSante", "Malphite", 
        "Maokai", "Mordekaiser", "Nasus", "Olaf", "Ornn", "Pantheon", "Poppy", 
        "Quinn", "Renekton", "Riven", "Rumble", "Sett", "Shen", "Singed", 
        "Sion", "TahmKench", "Teemo", "Tryndamere", "Urgot", "Vayne", 
        "Volibear", "Warwick", "Wukong", "Yasuo", "Yone", "Yorick"
    ],
    
    'JNG': [
        "Amumu", "BelVeth", "Briar", "Diana", "Ekko", "Elise", "Evelynn", 
        "Fiddlesticks", "Graves", "Hecarim", "Ivern", "JarvanIV", "Karthus", 
        "Kayn", "KhaZix", "Kindred", "LeeSin", "Lillia", "MasterYi", 
        "Nidalee", "Nocturne", "Nunu", "Olaf", "Rammus", "RekSai", "Rengar", 
        "Sejuani", "Shaco", "Shyvana", "Skarner", "Taliyah", "Trundle", 
        "Udyr", "Vi", "Viego", "Volibear", "Warwick", "XinZhao", "Zac"
    ],
    
    'MID': [
        "Ahri", "Akali", "Akshan", "Anivia", "Annie", "AurelionSol", "Azir", 
        "Cassiopeia", "Corki", "Diana", "Ekko", "Fizz", "Galio", "Gangplank", 
        "Hwei", "Irelia", "Jayce", "Kassadin", "Katarina", "LeBlanc", "Lissandra", 
        "Lux", "Malzahar", "Naafiri", "Neeko", "Orianna", "Qiyana", "Ryze", 
        "Swain", "Sylas", "Syndra", "Taliyah", "Talon", "TwistedFate", "Veigar", 
        "Vex", "Viktor", "Vladimir", "Xerath", "Yasuo", "Yone", "Zed", "Ziggs", "Zoe"
    ],
    
    'BOT': [
        "Aphelios", "Ashe", "Caitlyn", "Draven", "Ezreal", "Jhin", "Jinx", 
        "KaiSa", "Kalista", "KogMaw", "Lucian", "MissFortune", "Nilah", 
        "Samira", "Senna", "Swain", "Sivir", "Smolder", "Tristana", "Twitch", "Varus", "Vayne", 
        "Xayah", "Yasuo", "Zeri", "Ziggs"
    ],
    
    'SUP': [
        "Alistar", "Amumu", "Bard", "Blitzcrank", "Brand", "Braum", "Janna", 
        "Karma", "Leona", "Lulu", "Lux", "Maokai", "Milio", "Morgana", 
        "Nami", "Nautilus", "Neeko", "Pantheon", "Pyke", "Rakan", "Rell", 
        "RenataGlasc", "Senna", "Seraphine", "Sona", "Soraka", "Swain", 
        "Taric", "Thresh", "VelKoz", "Xerath", "Yuumi", "Zilean", "Zyra"
    ]
}


NORMALIZED_WHITELIST = {}
for role, champs in CHAMPION_WHITELIST.items():
    NORMALIZED_WHITELIST[role] = set(champs)