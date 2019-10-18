# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 12:04:47 2019

@author: Amoh - Gyebi Ampofo
"""
from PyQt5.QtCore import QFile, QResource, QIODevice
QResource.registerResource("resource.rcc")

class PhoneFrame():


    def __init__(self, filename):

        self.original_file = filename
        self.frame_qml = ":/qml/phone_replacement_qml.qml"

    def parentised_handling(self):

        pass

    def unparentised_handling(self):

        with open(self.original_file, 'r') as orig_file:
            orig_lines = orig_file.readlines()

        # Open with QFile
        replace_file = QFile(self.frame_qml)
        replace_file.open(QIODevice.ReadOnly)
        rep_data = replace_file.readAll()
        replace_data = str(rep_data, 'utf-8')

        frame_lines = replace_data.splitlines()

        # get import statements so we can add them
        orig_imp_stats = [n for n in orig_lines if n.startswith('import')]
        # last index of the import stats for the original files
        orig_imp_last_ind = orig_lines.index(orig_imp_stats[-1]) + 1
        orig_bottom_lines = orig_lines[orig_imp_last_ind:]
        
        frame_imps = frame_lines[:3]
        frame_body = frame_lines[3:]

        print('orig: ', orig_imp_stats)
        print('frame: ', frame_imps)
        
        frame_imp_s = {}
        for imp_s in frame_imps:
            ss = imp_s.split(' ')
            ss_w = ss[1]
            ss_num = ss[2].replace('.', '')
            frame_imp_s[ss_w] = int(ss_num)

        orig_imp_s = {}
        for o_imp_s in orig_imp_stats:
            ss = o_imp_s.split(' ')
            ss_w = ss[1]
            ss_num = ss[2].replace('.', '')
            orig_imp_s[ss_w] = int(ss_num)

        no = 0
        for imps in orig_imp_s:
            if imps in frame_imp_s:
                if orig_imp_s[imps] > frame_imp_s[imps]:
                    frame_imps.remove(frame_imps[no]) # remove
                    frame_imps.append(orig_imp_stats[no]) # add
            else:
                frame_imps.append(orig_imp_stats[no])
            no += 1

        n_frame_lines = frame_imps
        n_frame_lines.extend(frame_body)

        indent = "                "
        query_stat = "                " + 'objectName: "ContentItem"'
        begining_ind = n_frame_lines.index(query_stat) + 1

        # Add the original content
        no = begining_ind
        for line in orig_bottom_lines:
            no += 1
            nline = indent + line
            n_frame_lines.insert(no, nline)

        final_body = ""
        for line in n_frame_lines:

            final_body += line + '\r\n'

        return final_body
