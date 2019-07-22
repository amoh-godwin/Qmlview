import re


class FixQml():


    def __init__(self, filename):
        self.original_file = filename
        self.replacement_qml = "resources/replacement_qml.qml"
        self.search_keywords = ("ApplicationWindow", "Window")
        self.found_entry = ""


    def handle(self):

        # does the main
        if self.check_for_parent():
            return True, "0"
        else:
            data = self.put_in_parent()
            return False, data

    def check_for_parent(self):
        
        # find parent
        with open(self.original_file, 'r') as orig_file:
            data = orig_file.read(1024)
            info = re.findall('[A-Z].*?.*?.*? {', data)
        
        self.found_entry = info[0]
        clean_pat = info[0][:-2]
        
        if clean_pat in self.search_keywords:
            return True
        else:
            return False

    def put_in_parent(self):

        # put in a parent
        with open(self.original_file, 'r') as orig_file:
            ori_data = orig_file.read()
            
            splits = ori_data.split(self.found_entry, 1)
            top_data = splits[0]
            bottom_data = self.found_entry + splits[1]
        
        with open(self.replacement_qml, 'r') as replace_file:
            replace_data = replace_file.read()
            
        final_data = top_data + replace_data + "\n" + bottom_data + "\n" + "}"
        
        return final_data
