import psychopy 
from random import shuffle, randint, uniform, gauss
from config import CATEGORIES, CONTRASTS, CATEGORY_DIST

def generate_trials(total_trials):
    n_conditions = len(CATEGORIES) * len(CONTRASTS)
    
    n_per_condition = total_trials // n_conditions
    trials = []
    
    for trueCat in CATEGORIES:
        dist = CATEGORY_DIST[trueCat]
        for contrast in CONTRASTS:
            for _ in range(n_per_condition):
                    orientation = gauss(dist["mean"], dist["sd"]) 
                    trial = {
                        "trueCat": trueCat,
                        "contrast": contrast,
                        "orientation": orientation
                    }
                    trials.append(trial)
    shuffle(trials)
    return trials

print(generate_trials(216))