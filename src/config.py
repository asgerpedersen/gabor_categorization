'''
Configuration file for Gabor categorization experiment
Kristoffersen & Pedersen
'''

# ==================== EXPERIMENTAL DESIGN ====================
# Parameters
CATEGORIES = ["narrow", "broad"]
CONTRASTS  = [0.018, 0.03, 0.05, 0.082, 0.135, 0.223]
CATEGORY_DIST = {
    "narrow": {"mean": 0.0, "sd": 3.0},
    "broad":  {"mean": 0.0, "sd": 12.0},
}
KEYS = {
    # Category 1 (narrow)
    "q": {"responseCat": "1", "confidence rating": "4"},
    "w": {"responseCat": "1", "confidence rating": "3"},
    "e": {"responseCat": "1", "confidence rating": "2"},
    "r": {"responseCat": "1", "confidence rating": "1"},
    # Category 2 (broad)
    "u": {"responseCat": "2", "confidence rating": "1"},
    "i": {"responseCat": "2", "confidence rating": "2"},
    "o": {"responseCat": "2", "confidence rating": "3"},
    "p": {"responseCat": "2", "confidence rating": "4"},
}

# ==================== DISPLAY SETTINGS ====================
# Monitor configuration
monDistance = 70                                    # Distance from subject eyes to monitor (in cm)
monWidth = 30                                       # Width of monitor display (in cm)
fullscr = True                                     # Run in fullscreen mode (set to True for experiments)
framerate = 60                                      # Framerate of monitor (in Hz)

# Visual appearance
textSize = 0.8                                      # Size of text in degrees
stimSize = 1.2                                      # Size of cross...
gaborSize = 300                                     # Size of Gabor :)

# ==================== INPUT SETTINGS ====================
# Key mappings
ansKeys = ['q','w','e','r','u','i','o','p']
quitKeys = ['esc','escape']



# ==================== DATA SETTINGS ====================
# Data containers for each trial
dataCategories = ['trueCat', 'contrast', 'orientation', 'responseCat', 'confRating', 'RT', 'congruentResponse']
dialogueCategories = ['subjectID', 'age', 'gender', 'dominant_hand', 'glasses_status']

# File paths
saveFolder = 'data'