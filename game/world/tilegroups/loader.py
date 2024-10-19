import json
import os

GROUPS_FILE = os.path.join("game", "world", "tilegroups", "groups.json")

def initialiseTileGroups():
    with open(GROUPS_FILE) as file:
        GROUP_MANAGER.setFileData(json.load(file))

class GroupManager:
    def __init__(self):
        self.group_data = {}

    def getGroup(self, name):
        return self.group_data.get(name)

    def setGroup(self, name, type, tiles, extras={}):
        self.group_data[name] = {"type": type,
                                 "tiles": tiles,
                                 "extras": extras}

    def setFileData(self, json_parsing):
        self.group_data = json_parsing

    def getGroupsOfType(self, type):
        for group_name in self.group_data.keys():
            if self.group_data[group_name]["type"] == type:
                yield group_name

        return []

    def getGroupsWithTile(self, tile):
        for group_name in self.group_data.keys():
            if tile in self.group_data[group_name]["tiles"]:
                yield group_name

        return []

    def getExtras(self, group):
        return group.get("extras")

GROUP_MANAGER = GroupManager()
