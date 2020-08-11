import os


class SettingsLoader:

    def __init__(self, sl):

        self.sl = sl
        self._load_file()

    def _load_file(self):
        if os.path.isfile("settings.sf"):
            settings = open("settings.sf").read().split("\n")
            for line in settings:
                if len(line) > 0:
                    line_content = line.split("=")
                    if len(line_content) > 0:
                        if line_content[0] == "volume":
                            self.sl.set_se_volume(float(line_content[1]))

    def write_setting_volume(self, value):

        out_file = open("settings.sf", "w")
        out_file.write("volume="+str(value))
