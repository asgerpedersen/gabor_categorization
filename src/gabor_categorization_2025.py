from psychopy import core, visual, sound, event, gui, monitors
from random import shuffle, randint, uniform, gauss
import os, csv
from scripts.instructions import instructions, introduction

#-------------------- CONFIGURATION --------------------
#-------------------------------------------------------
# Import all settings from config file
try:
    from config import *
except ImportError:
    print("ERROR: Could not import config.py. Please ensure config.py exists in the same directory.")
    core.quit()

# Set monitor variables
myMon = monitors.Monitor('testMonitor')
myMon.setDistance(monDistance)
myMon.setWidth(monWidth)


# Intro dialogue
dialogue = gui.Dlg()
dialogue.addField('subjectID*')
dialogue.show()
if dialogue.OK:
    if dialogue.data[0].isdigit(): 
        subjectID = dialogue.data[0]
    else: 
        print('SUBJECT SHOULD BE DIGIT')
        core.quit()
else: core.quit()

saveFolder = 'data'
if not os.path.isdir(saveFolder): 
    os.makedirs(saveFolder)
    
#-------------------- STIMULI ----------------------
#---------------------------------------------------
win = visual.Window(monitor=myMon, size=myMon.getSizePix(), fullscr=fullscr, allowGUI=False, color='black', units='deg')   # Change fullscreen here: " fullscr=True/False "

mainText = visual.TextStim(win=win, height=textSize, color='white')
questionText = visual.TextStim(win=win, pos=(0, 2), height=textSize, color='white')
fixation = visual.TextStim(win, text='+', color='white', height=stimSize, antialias=False)

response_text = visual.TextStim(win, text="RESPONS", color="white", height=textSize)

#for feedback 
green_cross = visual.TextStim(win, text='+', color='green', height=stimSize)
red_cross = visual.TextStim(win, text='+', color='red', height=stimSize)

#-------------------- FUNCTIONS ----------------------
#-----------------------------------------------------
class CatTask:
    def __init__(self, win, subject_id):
        self.win = win
        self.subject_id = subject_id
        self.results = []

        self.correct_count = 0 
        # self.trials = self.generate_trials()
        self.examples = self.generate_examples()

        self.xpos = 0
        self.ypos = 0

    def generate_trials(self, size):
        total_trials = size
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

    def generate_examples(self):
        x_positions = [-9, -3, 3, 9]
        y_positions = [4, -4]

        narrow_orientations = [-2.5, 0.8, 0, 4.6]
        broad_orientations = [5.5, -7.8, -18.4, 15.3]

        stimuli = []  # List to hold all stimuli

        # Header
        header = visual.TextStim(
            win,
            text="Category Examples",
            pos=(0, 8),
            height=0.8,
            wrapWidth=20,
            color="white"
        )
        stimuli.append(header)

        # Category labels
        left_label_x = min(x_positions) - 5
        cat1_label = visual.TextStim(
            win,
            text="Category 1",
            pos=(left_label_x, y_positions[0]),
            height=0.8,
            color="blue",
            units="deg"
        )
        cat2_label = visual.TextStim(
            win,
            text="Category 2",
            pos=(left_label_x, y_positions[1]),
            height=0.8,
            color="red",
            units="deg"
        )
        stimuli.append(cat1_label)
        stimuli.append(cat2_label)

        # Press Space label
        pressSpace = visual.TextStim(
                win,
                text="[press SPACE to continue]",
                pos=(0.0, -9.0),
                height=0.6,
                color="white"
            )

        stimuli.append(pressSpace)

        # Narrow patches
        for i in range(4):
            x, y = x_positions[i], y_positions[0]
            gabor = visual.GratingStim(
                win,
                tex="sin",
                mask="gauss",
                size=5,
                sf=2,
                ori=(narrow_orientations[i] + 90),
                contrast=1,
                pos=(x, y),
                units="deg"
            )
            label = visual.TextStim(
                win,
                text=f"{narrow_orientations[i]}°",
                pos=(x, y - 2.5),
                height=0.6,
                color="white"
            )
            stimuli.append(gabor)
            stimuli.append(label)

        # Broad patches
        for i in range(4):
            x, y = x_positions[i], y_positions[1]
            gabor = visual.GratingStim(
                win,
                tex="sin",
                mask="gauss",
                size=5,
                sf=2,
                ori=(broad_orientations[i] + 90),
                contrast=1,
                pos=(x, y),
                units="deg"
            )
            label = visual.TextStim(
                win,
                text=f"{broad_orientations[i]}°",
                pos=(x, y - 2.5),
                height=0.6,
                color="white"
            )
            stimuli.append(gabor)
            stimuli.append(label)

        return stimuli  # Return the list of stimuli

    def feedback(self, congruent):
        if congruent:
            green_cross.draw()
        else:
            red_cross.draw()
        win.flip()
        core.wait(0.8)

    def show_instructions(self):
        questionText.setText(introduction['Welcome']) 
        questionText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
        
        questionText.setText(introduction['PresentStim']) 
        questionText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

        for stim in self.generate_examples():
            stim.draw()
        win.flip()
        event.waitKeys(keyList=['space'])


        questionText.setText(introduction['YourTask']) 
        questionText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
    
        questionText.setText(introduction['TrainingBlocks']) 
        questionText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

    def generate_gabor(self, ori_deg, contrast): # Trial is of type dictionary and includes category, contrast and orientation.
        gabor = visual.GratingStim(
            win,
            tex="sin",
            mask="gauss",
            size=gaborSize,      
            sf=0.04,       
            ori=(ori_deg+90),                           # +90 to make it horizontal
            contrast=contrast,    
            pos=(self.xpos, self.ypos),
            texRes=256,
            units="pix",
        )

        return gabor

    def run_trial(self, trial, training):
        #Get orientation and contrast from trial
        ori_deg = trial['orientation']
        c = trial['contrast']

        #Set contrast and stimulus duration by training
        contrast_show = 1 if training else c
        stim_dur = 0.3 if training else 0.05
        
        #Draw fixation cross and wait
        fixation.draw()
        win.flip()
        core.wait(0.8)
       
        #Draw gabor patch
        self.generate_gabor(ori_deg, contrast_show).draw()
        win.flip()
        core.wait(stim_dur)

        # Record press
        win.flip()
        clock = core.Clock()
        response = event.waitKeys(keyList=ansKeys+quitKeys, timeStamped=clock)

        if response:
            # Save key press and RT in variables
            key_pressed, response_time = response[0]
            
            # Manage escape
            if key_pressed == 'escape':
                self.win.close()
                self.save_results()
                core.quit()

            # Update trial dictionary
            trial['RT'] = response_time
            trial["responseCat"] = KEYS[key_pressed].get("responseCat")
            trial["confRating"] = KEYS[key_pressed].get("confidence rating")
            # Determine congruent response
            trueCat = "1" if trial["trueCat"] == "narrow" else "2"
            trial["congruentResponse"] = (trial["responseCat"] == trueCat)

            # Count number of correct trials 
            if trial["congruentResponse"]: 
                self.correct_count +=1
        
        else:               # If no response, trial is updated as follows.
            trial["RT"] = None
            trial["responseCat"] = None
            trial["confRating"] = None
            trial["congruentResponse"] = False

        # Feedback when during traing
        if training:
            self.feedback(trial["congruentResponse"])

        # Append trial result to restults list
        if not training:
            self.results.append(trial)

    def show_break(self, duration=55):
        questionText.setText('1-Minute break \n\n Message will appear right before break is over.') 
        questionText.draw()
        win.flip()
        core.wait(duration)
      
        questionText.setText("Get ready. The next block will begin in a few seconds.") 
        questionText.draw()
        win.flip()
        core.wait(5.0)

    def run_block(self, size, block_number):                         # Size is the number of trials in a given block
        # Reset correct count
        self.correct_count = 0
        
        # Determine whether current block is traing block
        training = True if block_number in [1,3,5,7] else False
        
        # Generate list of trials
        trials = self.generate_trials(size)     

        # Show block progress 
        showBlockType = '(TRAINING)' if training else '(TESTING)'

        mainText.setText('Beginning experiment Block ' + str(block_number) + ' / 8 ' + showBlockType + ' \n\n \n\n [press SPACE to continue...]')
        mainText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

        # Show instruction
        mainText.setText(instructions['main_training'] if training else instructions['main_testing'])
        mainText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

        # Show examples
        for stim in self.generate_examples():
            stim.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

        # Run trials
        for trial in trials:
            self.run_trial(trial, training)

        # summary of accuracy 
        percent_correct = (self.correct_count / size)*100
        summary_text = 'Block is over! Your accuracy was: \n\n' + f'Accuracy: {percent_correct:.1f}%' + '\n\n [press SPACE to continue]'
        mainText.setText(summary_text)
        mainText.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
    
    def run_experiment(self):
        self.run_block(72, 1)         # Training 
        self.run_block(216, 2)          # Testing
        self.show_break()               # 1 min break
        self.run_block(48, 3)           # Training
        self.run_block(216, 4)          # Testing
        self.show_break()               # 1 min break
        self.run_block(48, 5)           # Training
        self.run_block(216, 6)          # Testing
        self.show_break()               # 1 min break
        self.run_block(48, 7)           # Training
        self.run_block(216, 8)          # Testing

    def save_results(self): 
        #Set up save .csv function
        saveFile = saveFolder+'/subject_' +str(subjectID)+'.csv'              # Filename for save-data
        csvWriter = csv.writer(open(saveFile, 'w', newline=''), delimiter=';').writerow     # The writer function to csv
        csvWriter(dataCategories) 

        for trial in self.results:
            csvWriter([trial[category] for category in dataCategories])

    def ThankYou(self):
        questionText.setText('The experiment is over now! \n\nThank You for participating :)')                                      # !!!!!! Set text
        questionText.draw()
        win.flip()
        core.wait(5.0)

    
#--------------- RUN EXPERIMENT ------------------
#-------------------------------------------------

#Running the experiment
exp = CatTask(win, subjectID)
exp.show_instructions()
exp.run_experiment()
exp.save_results()
exp.ThankYou()

core.quit()

    
    
