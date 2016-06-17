#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gooey import Gooey, GooeyParser
from openpyxl import load_workbook

from classes.experiment import Experiment
from classes.block import Block
from classes.trial import Trial
from classes.instruction import Instruction

__author__ = 'ociepkam'


def load_info(filename):
    experiment_file = load_workbook(filename)
    sheet = experiment_file.get_active_sheet()

    experiment = []
    for row_idx in range(len(sheet.columns[0]) - 1):
        trial = {}
        for column_idx, column in enumerate(sheet.columns):
            if column_idx == 20:
                break
            if isinstance(column[row_idx + 1].value, (str, unicode)):
                trial.update({str(column[0].value): str(column[row_idx + 1].value)})
            elif not isinstance(column[row_idx + 1].value, type(None)):
                trial.update({str(column[0].value): int(column[row_idx + 1].value)})

        experiment.append(trial)

    number_of_blocks = max([int(x.value) for x in sheet.columns[0][1:]])
    return number_of_blocks, experiment


@Gooey(language='english',  # Translations configurable via json
       default_size=(450, 500),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def main():
    parser = GooeyParser(description='Create_concrete_experiment')
    parser.add_argument('Experiment_file_name', widget='FileChooser', help='Choose experiment file with general info')
    parser.add_argument('Participant_ID', type=str)
    parser.add_argument('Participant_Age', default=0, type=int)
    parser.add_argument('Participant_Sex', default='M', choices=['M', 'F'])
    parser.add_argument('Random', default='True', choices=['True', 'False'], help="Present trials in random order")
    parser.add_argument('EEG_connected', default='1', choices=['1', '0'], help='Choice')

    args = parser.parse_args()

    number_of_blocks, data = load_info(args.Experiment_file_name)

    experiment = Experiment([], args.Participant_ID, args.Participant_Sex, args.Participant_Age, int(args.EEG_connected))

    for idx in range(number_of_blocks):
        block = Block([])
        experiment.list_of_blocks.append(block)

    for idx in range(len(data)):
        trial_info = data[idx]
        block_number = trial_info['BLOCK_NUMBER']
        if trial_info['SAMPLE_TYPE'] == 'instruction':
            if trial_info['INSTRUCTION'][-3:] == 'txt':
                instruction_type = 'text'
            elif trial_info['INSTRUCTION'][-3:] == 'bmp' or trial_info['INSTRUCTION'][-3:] == 'jpg':
                instruction_type = 'image'
            else:
                raise AssertionError("wrong instruction file type")
            trial = Instruction(trial_info['INSTRUCTION'], instruction_type, trial_info['SHOW_TIME'])
        else:
            trial = Trial(trial_info['SAMPLE_TYPE'], trial_info['N'], trial_info['NR'], trial_info['MEMORY'],
                          trial_info['INTEGR'], trial_info['SHOW_TIME'], trial_info['RESP_TIME'], trial_info['MAX_TIME'],
                          trial_info['FEEDB'], trial_info['FEEDB_TIME'], trial_info['WAIT'], trial_info['EXP'],
                          trial_info['FIX_TIME'], trial_info['LIST_VIEW'], trial_info['BIN'], trial_info['TRAIL_TYPE'])
            trial.create_sample()
        experiment.list_of_blocks[block_number - 1].list_of_trials.append(trial)

    if args.Random:
        experiment.randomize()
    experiment.save()


if __name__ == '__main__':
    main()
