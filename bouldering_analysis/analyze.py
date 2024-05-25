#

from datetime import datetime

import csv
import numpy as np
import statistics
from datetime import date
import matplotlib.pyplot as plt
from dateutil import parser

LOG_FILE_PATH = './2024_log.csv'

CURRENT_DATE = datetime.now()

# Extract the current year and month
CURRENT_YEAR = CURRENT_DATE.year
CURRENT_MONTH = CURRENT_DATE.month

IDX_TIMESTAMP = 0
IDX_GRADE = 1
IDX_HOLD_TYPE = 3
IDX_NUM_ATTEMPTS = 4
IDX_IS_SEND = 5
IDX_QUAL_SEND = 6
IDX_ISSUE = 7
IDX_BREATHING = 9
IDX_CLOSE = 10
IDX_SHIFTING = 11
IDX_FOOTWORK = 13
IDX_BODY_AWARENESS = 14

TARGET_GRADES = ['V5', 'V6', 'V7']
HOLD_TYPES = ['Crimp', 'Jug', 'Pinch', 'Sloper', 'Pocket', 'Undercling', 'Side-pull', 'Horn']
ISSUES = ["Beta to the next move", "Suboptimal sequence", "Lack familiarity with the move", "Cannot grab on to the hold", "Wrong body position", "Footwork issue", "Too tired", "Too nervous", "Dry fire"]
TECHNIQUES = ["Yes", "Maybe", "No"]

is_header = True

session_info = {}

def normalize(cat_data):
    eps = 10e-6
    
    sums_bin = []
    for key in cat_data[0].keys():
        sums_bin.append(0)

    for cat in cat_data:
        i = 0
        for key in cat.keys():
            sums_bin[i] += cat[key]
            i += 1

    for cat in cat_data:
        i = 0
        for key in cat.keys():
            cat[key] = round((cat[key] + eps) / (sums_bin[i] + eps * len(cat_data)), 2)
            i += 1
    
def make_stacked_bars(plot, data, CATEGORIES, label):
    keys = data[0].keys()
    bottom = np.array([0.0 for x in keys])
    for i in range(0, len(CATEGORIES)):
        plot.bar(data[i].keys(), data[i].values(), bottom=bottom, label=CATEGORIES[i])
        bottom += np.array(list(data[i].values())).flatten()
    plot.set_xlabel(label)
    plot.legend()

if __name__ == "__main__":
    with open(LOG_FILE_PATH, 'r') as log_file:
        log_reader = csv.reader(log_file, delimiter=',')
        for row in log_reader:
            if is_header:
                is_header = False
                continue

            timestamp = parser.parse(row[IDX_TIMESTAMP])
            
            date_session = timestamp.date()
            if date_session not in session_info:
                session_info[date_session] = []
            
            session_info[date_session].append(row)

    
    # total num of sessions
    print('total # of sessions so far: ', len(session_info))

    nums_tries = {}
    lengths_sessions = {}
    nums_v5_sends = {}
    qualities_sends = {}
    nums_holds = [{} for x in HOLD_TYPES]
    grades_attempted = [{} for x in TARGET_GRADES]
    attempts_per_send = {}
    issues = [{} for y in ISSUES]
    tech_breathing = [{} for z in TECHNIQUES]
    tech_shifting = [{} for z in TECHNIQUES]
    tech_footwork = [{} for z in TECHNIQUES]
    tech_awareness = [{} for z in TECHNIQUES]
    

    for date_session in session_info.keys():

        if CURRENT_YEAR + CURRENT_MONTH / 12 - (date_session.year + date_session.month / 12) >= 1:
            continue

        date_bin = str(date_session.year%100) + '-' + str(date_session.month)

        if date_bin not in nums_tries:
            nums_tries[date_bin] = []

        if date_bin not in lengths_sessions:
            lengths_sessions[date_bin] = []

        if date_bin not in nums_v5_sends:
            nums_v5_sends[date_bin] = []
            attempts_per_send[date_bin] = []

        if date_bin not in qualities_sends:
            qualities_sends[date_bin] = []

        # 
        nums_tries[date_bin].append(len(session_info[date_session]))
        # 
        ts_start = parser.parse(session_info[date_session][0][IDX_TIMESTAMP])
        ts_end = parser.parse(session_info[date_session][-1][IDX_TIMESTAMP])
        lengths_sessions[date_bin].append((ts_end - ts_start).total_seconds() / 60)
        
        # 
        _v5_sends = 0
        _v5_send_attempts = 0
        for row in session_info[date_session]:
            if row[IDX_GRADE] in TARGET_GRADES and row[IDX_IS_SEND] == 'Yes':
                _v5_sends += 1
                _v5_send_attempts += int(row[IDX_NUM_ATTEMPTS])
        nums_v5_sends[date_bin].append(_v5_sends)
        attempts_per_send[date_bin].append((_v5_send_attempts + 10e-6) / (_v5_sends + 10e-6))
       
        # 
        _quality_sends = 0
        _num_sends = 0
        for row in session_info[date_session]:
            if row[IDX_IS_SEND] == 'Yes':
                if len(row[IDX_QUAL_SEND]) > 0:
                    _quality_sends += int(row[IDX_QUAL_SEND])
                    _num_sends += 1
        if _num_sends > 0:
            qualities_sends[date_bin].append(_quality_sends / _num_sends)
        else:
            qualities_sends[date_bin].append(0)
        
        # grades attempted
        for row in session_info[date_session]:
            _grade = row[IDX_GRADE]
            for i in range(0, len(TARGET_GRADES)):
                if date_bin not in grades_attempted[i]:
                    grades_attempted[i][date_bin] = 0
                if TARGET_GRADES[i] == _grade:
                    grades_attempted[i][date_bin] += 1

        #
        for row in session_info[date_session]:
            _holds = row[IDX_HOLD_TYPE].split(',')
            for i in range(0, len(HOLD_TYPES)):
                if date_bin not in nums_holds[i]:
                    nums_holds[i][date_bin] = 0
                if HOLD_TYPES[i] in _holds:
                    nums_holds[i][date_bin] += 1
        
        # 
        for row in session_info[date_session]:
            _issues = row[IDX_ISSUE].split(',')
            for i in range(0, len(ISSUES)):
                if date_bin not in issues[i]:
                    issues[i][date_bin] = 0
                if ISSUES[i] in _issues:
                    issues[i][date_bin] += 1

        # 
        for row in session_info[date_session]:
            _breathing = row[IDX_BREATHING]
            for i in range(0, len(TECHNIQUES)): 
                if date_bin not in tech_breathing[i]:
                    tech_breathing[i][date_bin] = 0
                if _breathing == TECHNIQUES[i]:
                    tech_breathing[i][date_bin] += 1
        
        # 
        for row in session_info[date_session]:
            _shifting = row[IDX_SHIFTING]
            for i in range(0, len(TECHNIQUES)): 
                if date_bin not in tech_shifting[i]:
                    tech_shifting[i][date_bin] = 0
                if _shifting == TECHNIQUES[i]:
                    tech_shifting[i][date_bin] += 1

        # 
        for row in session_info[date_session]:
            _footwork = row[IDX_FOOTWORK]
            for i in range(0, len(TECHNIQUES)): 
                if date_bin not in tech_footwork[i]:
                    tech_footwork[i][date_bin] = 0
                if _footwork == TECHNIQUES[i]:
                    tech_footwork[i][date_bin] += 1

        # 
        for row in session_info[date_session]:
            _awareness = row[IDX_BODY_AWARENESS]
            for i in range(0, len(TECHNIQUES)): 
                if date_bin not in tech_awareness[i]:
                    tech_awareness[i][date_bin] = 0
                if _awareness == TECHNIQUES[i]:
                    tech_awareness[i][date_bin] += 1

    # 
    # data cleansing
    max_num_attempts = 0
    for date_bin in nums_tries:
        for num in nums_tries[date_bin]:
            max_num_attempts = max(max_num_attempts, num)
            if num <= 1:
                nums_tries[date_bin].remove(num)

    normalize(nums_holds)
    normalize(grades_attempted)
    normalize(issues)
    normalize(tech_breathing)
    normalize(tech_shifting)
    normalize(tech_footwork)
    normalize(tech_awareness)

    # 
    # data viz
    fig_overall, axs = plt.subplots(4, 4)
    fig_overall.set_size_inches(18, 10)

    axs_frequency = axs[0, 0]
    axs_length = axs[0, 1]
    axs_attempts = axs[0, 2]
    axs_v5_sends = axs[0, 3]
    axs_attempts_per_send = axs[1,0]
    axs_quality = axs[1, 1]
    axs_hold = axs[1, 2]
    axs_issue = axs[1, 3]
    axs_breathing = axs[2, 0]
    axs_shifting = axs[2, 1]
    axs_footwork = axs[2, 2]
    axs_awareness = axs[2, 3]
    axs_grades_attempted = axs[3, 0]

    # 
    axs_attempts.plot(nums_tries.keys(), [statistics.mean(x) for x in nums_tries.values()])
    axs_attempts.set_xlabel('# of attempts per session')
    axs_attempts.set_ylim(0, max_num_attempts)
    
    # 
    axs_length.plot(lengths_sessions.keys(), [statistics.mean(x) for x in lengths_sessions.values()])
    axs_length.set_xlabel('minutes per session')
    axs_length.set_ylim(0, 120)

    # 
    axs_v5_sends.plot(nums_v5_sends.keys(), [statistics.mean(x) for x in nums_v5_sends.values()])
    axs_v5_sends.set_xlabel('# of v5+ sends per session')
    axs_v5_sends.set_ylim(0, 6)

    # 
    axs_attempts_per_send.plot(attempts_per_send.keys(), [statistics.mean(x) for x in attempts_per_send.values()])
    axs_attempts_per_send.set_xlabel('# of attempts per v5+ send')
    axs_attempts_per_send.set_ylim(0, 5)

    # 
    axs_quality.plot(qualities_sends.keys(), [statistics.mean(x) for x in qualities_sends.values()])
    axs_quality.set_xlabel('qualities of sends')
    axs_quality.set_ylim(0, 8)
    
    # 
    make_stacked_bars(axs_hold, nums_holds, HOLD_TYPES, 'types of hold')

    # 
    axs_frequency.plot(nums_tries.keys(), [len(x) for x in nums_tries.values()])
    axs_frequency.set_xlabel('# sessions per month')
    axs_frequency.set_ylim(0, 15)

    # 
    make_stacked_bars(axs_grades_attempted, grades_attempted, TARGET_GRADES, 'grades attempted')

    # 
    make_stacked_bars(axs_issue, issues, ISSUES, 'issues')

    # 
    make_stacked_bars(axs_breathing, tech_breathing, TECHNIQUES, 'breathing?')

    # 
    make_stacked_bars(axs_shifting, tech_shifting, TECHNIQUES, 'shifting my body?')

    # 
    make_stacked_bars(axs_footwork, tech_footwork, TECHNIQUES, 'using silent feet?')

    # 
    make_stacked_bars(axs_awareness, tech_awareness, TECHNIQUES, 'maintaining body awareness?')

    plt.show()
