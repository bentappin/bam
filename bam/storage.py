# encoding: utf-8
import json
import os


class DataStore(object):
    data = None

    def __init__(self):
        self.data_dir = os.path.join(os.path.expanduser('~'), '.bam/')
        self.data_path = os.path.join(
            self.data_dir,
            'data.json'
        )
        self._setup()

    def _setup(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        try:
            with open(self.data_path, 'r') as f:
                self.data = json.load(f)
        except IOError, ValueError:
            self.data = {}

    def save(self):
        with open(self.data_path, 'w+') as f:
            json.dump(self.data, f, indent=2)

    def get_item(self, key, list_name=None):
        if not list_name:
            for k, v in self.data.iteritems():
                for x, y in v.iteritems():
                    if x == key:
                        return y
        try:
            return self.data[list_name][key]
        except KeyError:
            return

    def get_values(self):
        d = self.data
        return [value for dd in d.itervalues() for value in dd.itervalues()]

    def add_item(self, list_name, key, value):
        self.data[list_name][key] = value
        self.save()

    def delete_item(self, list_name, key):
        if self.list_exists(list_name):
            the_list = self.data[list_name]
            if key in the_list:
                del self.data[list_name][key]
                self.save()

    def list_exists(self, list_name):
        return list_name in self.data

    def item_exists(self, item_name):
        return self.get_item(item_name)

    def create_list(self, list_name):
        if not self.list_exists(list_name):
            self.data[list_name] = {}
            self.save()

    def get_list(self, list_name):
        if self.list_exists(list_name):
            return self.data[list_name]

    def get_all_lists(self):
        return self.data

    def delete_list(self, list_name):
        if self.list_exists(list_name):
            del self.data[list_name]
            self.save()
