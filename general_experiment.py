#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gooey import Gooey, GooeyParser
from openpyxl import Workbook

__author__ = 'ociepkam'


def save_to_xlsx(tab, filename):
    wb = Workbook()

    # grab the active worksheet
    ws = wb.active

    # Data can be assigned directly to cells
    ws.append(
        ['BLOCK_NUMBER', 'SAMPLE_TYPE', 'N', 'NR', 'STIMTIME', 'RESPTIME', 'FEEDB',
         'FEEDB_TIME', 'WAIT', 'EXP', 'BIN', 'TRAIL_TYPE', 'INSTRUCTION'])

    for idx, trial in enumerate(tab):
        if trial[1] == "instruction":
            trial_with_verification = trial[0:2] + [''] * 2 + [trial[2]] + [''] * 7 + [trial[-1]]
        else:
            trial_with_verification = trial
        ws.append(trial_with_verification)

    # Save the file
    wb.save(filename + ".xlsx")


@Gooey(language='english',  # Translations configurable via json
       default_size=(650, 600),  # starting size of the GUI
       required_cols=1,  # number of columns in the "Required" section
       optional_cols=3,  # number of columns in the "Optional" section
       )
def generate_trials_gui():
    # General information
    parser = GooeyParser(description='Create_general_experiment')
    parser.add_argument('Number_of_blocks', default=1, action='store', type=int, help='Number')
    parser.add_argument('Number_of_training_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('Number_of_experiment_trials', default=4, action='store', type=int, help='Number')
    parser.add_argument('File_name', default='experiment', type=str, help='Name of file with not personalized data')

    parser.add_argument('--Instruction', widget='FileChooser', help='Choose instruction file')
    parser.add_argument('--Instruction_show_time', default=5, action='store', type=int, help='Number')

    # Information about training
    parser.add_argument('--Training_task', default='letters',
                        choices=['letters', 'figures', 'symbols', 'numbers', 'greek_letters'],
                        help='Choose trial type')
    parser.add_argument('--Training_number', default=1, action='store', type=int, help='Number of relations')
    parser.add_argument('--Training_stim_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_resp_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_feedback_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Training_bin', default='1', choices=['1', '0'], help='Choose view type')
    parser.add_argument('--Training_trial_type', default='1', choices=['1', '2', '3', '4'], help='Choose view type')

    # Information about experiment
    parser.add_argument('--Experiment_task', default='letters',
                        choices=['letters', 'figures', 'symbols', 'numbers', 'greek_letters'],
                        help='Choose trial type')
    parser.add_argument('--Experiment_number', default=1, action='store', type=int, help='Number of relations')
    parser.add_argument('--Experiment_stim_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_resp_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_feedback', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_feedback_time', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_wait', default=1, action='store', type=int, help='Number')
    parser.add_argument('--Experiment_bin', default='1', choices=['1', '0'], help='Choose view type')
    parser.add_argument('--Experiment_trial_type', default='1', choices=['1', '2', '3', '4'], help='Choose view type')

    args = parser.parse_args()
    experiment = []

    name = args.Instruction.split('/')[-1]

    for block in range(args.Number_of_blocks):
        instruction = [block + 1, 'instruction', args.Instruction_show_time, name]
        experiment.append(instruction)
        for idx in range(0, args.Number_of_training_trials):
            trial = [block + 1, args.Training_task, args.Training_number, idx + 1, args.Training_stim_time,
                     args.Training_resp_time, args.Training_feedback, args.Training_feedback_time,
                     args.Training_wait, 0, int(args.Training_bin), int(args.Training_trial_type)]
            experiment.append(trial)
        for idx in range(0, args.Number_of_experiment_trials):
            trial = [block + 1, args.Experiment_task, args.Experiment_number, idx + 1, args.Experiment_stim_time,
                     args.Experiment_resp_time, args.Experiment_feedback, args.Experiment_feedback_time,
                     args.Experiment_wait, 1, int(args.Experiment_bin), int(args.Experiment_trial_type)]
            experiment.append(trial)

    save_to_xlsx(experiment, args.File_name)


def main():
    generate_trials_gui()


if __name__ == '__main__':
    main()
