#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from enum import Enum
import string

__author__ = 'ociepkam'

SampleTypes = {
    'letters': 'letters',
    'figures': 'figures',
    'NamesHeightRelations': 'NamesHeightRelations',
    'NamesAgeRelations': 'NamesAgeRelations',
    'symbols': 'symbols',
    'numbers': 'numbers',
    'greek_letters': 'greek_letters'
}

# General relations types.
Relations = {
    'major': '>',
    'minor': '<'
}


# Age relations types for name samples.
class NamesAgeRelations(Enum):
    major_M = ' starszy niż '
    major_F = ' starsza niż '
    minor_M = ' młodszy niż '
    minor_F = ' młodsza niż '


# Height relations types for name samples.
class NamesHeightRelations(Enum):
    major_M = ' wyższy niż '
    major_F = ' wyższa niż '
    minor_M = ' niższy niż '
    minor_F = ' niższa niż '


# Dictonary for name samples.
names_types = {
    'NamesAgeRelations': NamesAgeRelations,
    'NamesHeightRelations': NamesHeightRelations
}

names = (
    {'name': 'Tomek', 'sex': 'M'},
    {'name': 'Lech', 'sex': 'M'},
    {'name': 'Jan', 'sex': 'M'},
    {'name': 'Roch', 'sex': 'M'},
    {'name': 'Piotr', 'sex': 'M'},
    {'name': 'Adam', 'sex': 'M'},
    {'name': 'Filip', 'sex': 'M'},
    {'name': 'Igor', 'sex': 'M'},
    {'name': 'Jacek', 'sex': 'M'},
    {'name': 'Wit', 'sex': 'M'},

    {'name': 'Ewa', 'sex': 'F'},
    {'name': 'Anna', 'sex': 'F'},
    {'name': 'Iga', 'sex': 'F'},
    {'name': 'Magda', 'sex': 'F'},
    {'name': 'Ada', 'sex': 'F'},
    {'name': 'Ola', 'sex': 'F'},
    {'name': 'Łucja', 'sex': 'F'},
    {'name': 'Maja', 'sex': 'F'},
    {'name': 'Klara', 'sex': 'F'},
    {'name': 'Ida', 'sex': 'F'},
)

# List of stimulus for letters samples. Only consonants letters.
letters = list(set(string.ascii_uppercase) - set("AEIOUY"))

figures = (
    'square',
    'triangle',
    'circle',
    'trapeze',
    'diamond',
    'ellipse',
    'rectangle',
    'hexagon'
)

symbols = list(set("~!@#%&*?|"))

numbers = list(set("0123456789"))

greek_letters = [u'\u0391', u'\u0392', u'\u0393', u'\u0394', u'\u0395', u'\u0396', u'\u0397', u'\u0398', u'\u0399',
                 u'\u039A', u'\u039B', u'\u039C', u'\u039D', u'\u039E', u'\u039F', u'\u03A0', u'\u03A1', u'\u03A2',
                 u'\u03A3', u'\u03A4', u'\u03A5', u'\u03A6', u'\u03A7', u'\u03A8', u'\u03A9']


class Trial:
    def __init__(self, sample_type, n, nr, stim_time, resp_time, feedb, feedb_time, wait, exp, bin, trial_type):
        """
        :param sample_type: kind of stimulus. All possibilities in SampleTypes class.
        :param n: number of relations in trial. n+1 number od elements in relation chain
        :param nr: Trial index. Different for each Trial.
        :param stim_time: how long participant can see each relations.
        :param resp_time: time between trials
        :param feedb:
            0 - doesn't show result for this Trial.
            1 - show result for this Trial.
            2 - doesn't show result for this Trial but show percent result at the end of test.
        :param wait: break time after Trial. 0 - wait until participant doesn't press button.
        :param exp:
            (exp == 1) => Experiment Trial.
            (exp == 0) => Test Trail.
        :param bin:
            0 - generate four answers
            1 - generate two answers
        :param trial_type:
            1 - ask about relation
            2 - ask about relation with changed "<" symbol
            3 - ask about relation with distance 1
            4 - ask about relation with distance 2
        :return:
        """
        self.sample_type = sample_type
        self.n = n
        self.nr = nr
        self.stim_time = stim_time
        self.resp_time = resp_time
        self.feedb = feedb
        self.feedb_time = feedb_time
        self.wait = wait
        self.exp = int(exp)
        self.relations_list = None
        self.task = None
        self.answer = None
        self.type = 'trial'
        self.bin = bin
        self.trial_type = trial_type

    def create_sample_letters(self):
        """
        From n+1 random letters generate chain of pair of relations.
        There are two types of relations "<" and ">"
        :return: Chain of pair of relations.
        """

        relations_list = []
        chain_of_letters = []

        if self.sample_type == "letters":
            stimulus_nr = random.sample(range(len(letters)), self.n + 1)
            for idx in stimulus_nr:
                chain_of_letters.append(letters[idx])
        elif self.sample_type == "numbers":
            stimulus_nr = random.sample(range(len(numbers)), self.n + 1)
            for idx in stimulus_nr:
                chain_of_letters.append(numbers[idx])
        elif self.sample_type == "greek_letters":
            stimulus_nr = random.sample(range(len(greek_letters)), self.n + 1)
            for idx in stimulus_nr:
                chain_of_letters.append(greek_letters[idx])
        else:
            stimulus_nr = random.sample(range(len(figures)), self.n + 1)
            for idx in stimulus_nr:
                chain_of_letters.append(symbols[idx])

        for idx in range(0, self.n):
            stimulus_type = random.choice([Relations['major'], Relations['minor']])
            stimulus_1 = chain_of_letters[idx]
            stimulus_2 = chain_of_letters[idx + 1]

            if stimulus_type == Relations['minor']:
                relation = stimulus_1 + stimulus_type + stimulus_2
                relations_list.append(relation)
            else:
                relation = stimulus_2 + stimulus_type + stimulus_1
                relations_list.append(relation)

        # Generate task and answer
        def good_bad_relation(relations_list, relations_chain):
            if self.trial_type == 1:
                first_task = random.choice(relations_list)
                if first_task[1] == Relations['minor']:
                    second_task = first_task[0] + Relations['major'] + first_task[2]
                else:
                    second_task = first_task[0] + Relations['minor'] + first_task[2]
                return [first_task, second_task]
            elif self.trial_type == 2:
                second_task = random.choice(relations_list)[::-1]
                if second_task[1] == Relations['minor']:
                    first_task = second_task[0] + Relations['major'] + second_task[2]
                else:
                    first_task = second_task[0] + Relations['minor'] + second_task[2]
                return [first_task, second_task]
            elif self.trial_type == 3:
                first = random.randint(0, self.n - 2)
                second = first + 2
            else:
                first = random.randint(0, self.n - 3)
                second = first + 3
            if random.randint(0, 1):
                first_task = relations_chain[first] + Relations['minor'] + relations_chain[second]
                second_task = relations_chain[first] + Relations['major'] + relations_chain[second]
            else:
                first_task = relations_chain[second] + Relations['major'] + relations_chain[first]
                second_task = relations_chain[second] + Relations['minor'] + relations_chain[first]

            return [first_task, second_task]

        # Creating task and answer
        if self.bin:
            task = good_bad_relation(relations_list, chain_of_letters)
        else:
            task = [good_bad_relation(relations_list, chain_of_letters)[0]]
            while len(task) < 4:
                new_task = good_bad_relation(relations_list, chain_of_letters)[1]
                if new_task not in task:
                    task.append(new_task)

        answer = task[0]
        random.shuffle(task)

        return relations_list, task, answer

    def create_sample_names(self, sample_type):
        """
        From n+1 random letters generate chain of pair of relations.
        There are two types of relations "<" and ">"
        :param sample_type: decide with of two NamesAgeRelations or NamesHeightRelations we need to generate
        :return: Chain of pair of relations.
        """
        stimulus_nr = random.sample(range(0, 8), self.n + 1)
        relations_list = []

        chain_of_names = []
        for idx in stimulus_nr:
            chain_of_names.append(names[idx])

        for idx in range(0, self.n):
            stimulus_type = random.choice([Relations['major'], Relations['minor']])
            stimulus_1 = chain_of_names[idx]
            stimulus_2 = chain_of_names[idx + 1]

            if stimulus_type == Relations['minor']:
                if stimulus_1['sex'] == 'F':
                    stimulus_type = sample_type.minor_F
                else:
                    stimulus_type = sample_type.minor_M

                relation = stimulus_1['name'] + stimulus_type + stimulus_2['name']
                relations_list.append(relation)
            else:
                if stimulus_2['sex'] == 'F':
                    stimulus_type = sample_type.major_F
                else:
                    stimulus_type = sample_type.major_M

                relation = stimulus_2['name'] + stimulus_type + stimulus_1['name']
                relations_list.append(relation)

        task, answer = self.create_task(chain_of_names)

        return relations_list, task, answer

    def create_sample_figures(self):
        """
        From n+1 random figures generate chain of pair of relations.
        :return: Chain of pair of relations.
        """

        stimulus_nr = random.sample(range(0, 8), self.n + 1)
        chain_of_figures = []
        for idx in stimulus_nr:
            chain_of_figures.append(figures[idx])

        relations_list = []
        for idx in range(0, self.n):
            stimulus_1 = chain_of_figures[idx]
            stimulus_2 = chain_of_figures[idx + 1]
            relations_list.append([stimulus_1, stimulus_2])

        # Creating task and answer

        def good_bad_relation(relations_chain, relations_list):
            if self.trial_type == 1 or self.trial_type == 2:
                rel = random.choice(relations_list)
                first_task = rel
                second_task = rel[::-1]
                return [first_task, second_task]
            elif self.trial_type == 3:
                first = random.randint(0, self.n - 2)
                second = first + 2
            else:
                first = random.randint(0, self.n - 3)
                second = first + 3

            first_task = [relations_chain[first], relations_chain[second]]
            second_task = [relations_chain[second], relations_chain[first]]
            return [first_task, second_task]

        # Creating task and answer
        if self.bin:
            task = good_bad_relation(chain_of_figures, relations_list)
        else:
            task = [good_bad_relation(chain_of_figures, relations_list)[0]]
            while len(task) < 4:
                new_task = good_bad_relation(chain_of_figures, relations_list)[1]
                if (new_task not in task) or (self.trial_type >= self.n):
                    task.append(new_task)

        answer = task[0]
        random.shuffle(task)
        return relations_list, task, answer

    def create_sample(self):
        """
        Allow to choose task type.
        :return: Chain of pair of relations.
        """
        if self.sample_type == "letters" or self.sample_type == "symbols" or self.sample_type == 'numbers' or \
                        self.sample_type == 'greek_letters':
            relations_list, task, answer = self.create_sample_letters()
        elif self.sample_type == "NamesHeightRelations":
            relations_list, task, answer = self.create_sample_names(names_types["NamesHeightRelations"])
        elif self.sample_type == "NamesAgeRelations":
            relations_list, task, answer = self.create_sample_names(names_types["NamesAgeRelations"])
        else:
            relations_list, task, answer = self.create_sample_figures()

        self.shuffle_sample(relations_list)

        self.relations_list = relations_list
        self.task = task
        self.answer = answer

    def shuffle_sample(self, relations_list):
        """
        :param relations_list: List of all relations in trial. Generated by create_sample.
        :return: Shuffled list of relations in order with will see participant.

        Firs relation is random. Each next must contain one of the parameters with was show before.
        """
        # choosing first relation
        first_stimulus = random.randint(0, self.n - 1)
        relations_shuffled_list = [relations_list[first_stimulus]]

        next_elem = first_stimulus + 1
        previous_elem = first_stimulus - 1

        # As long as exist relations before or after chose relations find new one before or after already choose.
        while next_elem <= self.n and previous_elem >= -1:
            # No not chose elements at the end of relations chain
            if next_elem == self.n:
                relations_shuffled_list.append(relations_list[previous_elem])
                previous_elem -= 1
            # No not chose elements at the beginning of relations chain
            elif previous_elem == -1:
                relations_shuffled_list.append(relations_list[next_elem])
                next_elem += 1
            # Choose element before or after created chain
            else:
                if random.choice(['next', 'previous']) == next_elem:
                    relations_shuffled_list.append(relations_list[next_elem])
                    next_elem += 1
                else:
                    relations_shuffled_list.append(relations_list[previous_elem])
                    previous_elem -= 1

        return relations_shuffled_list

    def create_task(self, relations_chain):
        """
        :param relations_chain: chain of all samples in trial
        :return: Task and answer for trial
        """

        def good_bad_relation():
            if self.trial_type == 1 or self.relations_list == 2:
                first = random.randint(0, self.n - 1)
                second = first + 1
            elif self.trial_type == 3:
                first = random.randint(0, self.n - 2)
                second = first + 2
            else:
                first = random.randint(0, self.n - 3)
                second = first + 3

            if self.sample_type == SampleTypes['figures']:
                first_task = [relations_chain[first], relations_chain[second]]
                second_task = [relations_chain[second], relations_chain[first]]

            elif self.sample_type == SampleTypes['letters'] or self.sample_type == SampleTypes['symbols']:
                first_task = relations_chain[first] + Relations['minor'] + relations_chain[second]
                second_task = relations_chain[second] + Relations['minor'] + relations_chain[first]
            else:
                if self.sample_type == SampleTypes['NamesAgeRelations']:
                    if relations_chain[first]['sex'] == 'M':
                        first_relation = NamesAgeRelations.minor_M
                    else:
                        first_relation = NamesAgeRelations.minor_F
                    if relations_chain[second]['sex'] == 'M':
                        second_relation = NamesAgeRelations.minor_M
                    else:
                        second_relation = NamesAgeRelations.minor_F
                else:
                    if relations_chain[first]['sex'] == 'M':
                        first_relation = NamesHeightRelations.minor_M
                    else:
                        first_relation = NamesHeightRelations.minor_F
                    if relations_chain[second]['sex'] == 'M':
                        second_relation = NamesHeightRelations.minor_M
                    else:
                        second_relation = NamesHeightRelations.minor_F
                first_task = relations_chain[first]['name'] + first_relation + relations_chain[second]['name']
                second_task = relations_chain[second]['name'] + second_relation + relations_chain[first]['name']
            return [first_task, second_task]

        # Creating task and answer
        if self.bin:
            task = good_bad_relation()
        else:
            task = [good_bad_relation()[0]]
            while len(task) < 4:
                new_task = good_bad_relation()[1]
                if new_task not in task:
                    task.append(new_task)

        answer = task[0]
        random.shuffle(task)
        return task, answer

    def prepare_general(self):
        trial = {
            "TYPE": self.type,
            'SAMPLE_TYPE': self.sample_type,
            'N': self.n,
            'NR': self.nr,
            'STIMTIME': self.stim_time,
            'RESPTIME': self.resp_time,
            'FEEDB': self.feedb,
            'FEEDB_TIME': self.feedb_time,
            'WAIT': self.wait,
            'EXP': self.exp,
            'BIN': self.bin,
            'TRIAL_TYPE': self.trial_type
        }

        return trial

    def prepare_concrete(self):
        trial = self.prepare_general()
        trial['RELATIONS_LIST'] = self.relations_list
        trial['TASK'] = self.task
        trial['ANSWER'] = self.answer

        return trial
