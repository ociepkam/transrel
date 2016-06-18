import yaml


class Experiment:
    def __init__(self, list_of_blocks, id, sex, age, eeg, nirs):
        self.name = str(id) + sex + str(age)
        self.list_of_blocks = list_of_blocks
        self.eeg = eeg
        self.nirs = nirs

    def prepare_concrete(self):
        elements_list = []
        for element in self.list_of_blocks:
            elements_list.append(element.prepare_concrete())
        info = {
            "NAME": self.name,
            "LIST_OF_BLOCKS": elements_list,
            "EEG": self.eeg,
            "NIRS": self.nirs
        }
        return info

    def randomize(self):
        for block in self.list_of_blocks:
            block.randomize()

    def save(self):
        info = self.prepare_concrete()
        with open("data/" + self.name + ".yaml", 'w') as save_file:
            save_file.write(yaml.dump(info))
