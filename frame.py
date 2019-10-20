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

        # split import stats into the name and the version number for comparing
        frame_imp_s = {}
        for imp_s in frame_imps:
            ss = imp_s.split(' ')
            ss_w = ss[1]
            ss_num = ss[2].replace('.', '')
            frame_imp_s[ss_w] = int(ss_num)

        # split import stats into the name and the version number for comparing
        orig_imp_s = {}
        for o_imp_s in orig_imp_stats:
            ss = o_imp_s.split(' ')
            ss_w = ss[1]
            # if import is an imported folder
            # it does not contain a number
            if '"' in ss_w or "'" in ss_w:
                orig_imp_s[ss_w] = 1
            else:
                ss_num = ss[2].replace('.', '')
                orig_imp_s[ss_w] = int(ss_num)

        # Finally compare and insert or remove lower import version
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

        # Delete ApplicationWindow
        orig_bottom_lines = self._del_parts(
                'ApplicationWindow {', orig_bottom_lines)

        # Pick all properties and comps in ApplicationWindow
        prop_lines, orig_bottom_lines = self._pick_parent_props(orig_bottom_lines)

        menubar_lines, orig_bottom_lines = self._find_part('menuBar:',
                                                          orig_bottom_lines)

        header_lines, orig_bottom_lines = self._find_part('header:',
                                                          orig_bottom_lines)

        footer_lines, orig_bottom_lines = self._find_part('footer:',
                                                          orig_bottom_lines)

        # Accept the remaining as content Lines
        # Todo properties and signal handlers should be handled as well
        content_lines = orig_bottom_lines

        ### Start the insertion
        # properties
        n_frame_lines = self._put_into_place(4,
                                          'objectName: "MainWindowItem"',
                                          prop_lines,
                                          n_frame_lines)
        # menubar
        n_frame_lines = self._put_into_place(16,
                                          'objectName: "menuBarContainerItem"',
                                          menubar_lines,
                                          n_frame_lines)
        # header
        n_frame_lines = self._put_into_place(16,
                                          'objectName: "headerItem"',
                                          header_lines,
                                          n_frame_lines)
        # footer
        n_frame_lines = self._put_into_place(16,
                                          'objectName: "footerItem"',
                                          footer_lines,
                                          n_frame_lines)
        # contentItem ( Remaining content)
        n_frame_lines = self._put_into_place(16,
                                          'objectName: "ContentItem"',
                                          content_lines,
                                          n_frame_lines)

        final_body = ""
        for line in n_frame_lines:

            final_body += line + '\r\n'

        print(final_body)
        return final_body

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

        # split import stats into the name and the version number for comparing
        frame_imp_s = {}
        for imp_s in frame_imps:
            ss = imp_s.split(' ')
            ss_w = ss[1]
            ss_num = ss[2].replace('.', '')
            frame_imp_s[ss_w] = int(ss_num)

        # split import stats into the name and the version number for comparing
        orig_imp_s = {}
        for o_imp_s in orig_imp_stats:
            ss = o_imp_s.split(' ')
            ss_w = ss[1]
            # if import is an imported folder
            # it does not contain a number
            if '"' in ss_w or "'" in ss_w:
                orig_imp_s[ss_w] = 1
            else:
                ss_num = ss[2].replace('.', '')
                orig_imp_s[ss_w] = int(ss_num)

        # Finally compare and insert or remove lower import version
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

        # Start the search for the contentItem where we'll insert the users qml
        n_frame_lines = self._put_in_part(16,
                                          'objectName: "ContentItem"',
                                          orig_bottom_lines,
                                          n_frame_lines)

        final_body = ""
        for line in n_frame_lines:

            final_body += line + '\r\n'

        return final_body

    def _del_parts(self, query, lines):

        cc = []
        bracks = 1
        ind = -1
        for line in lines:
            ind += 1
            if query in line:
                lines[ind] = '***'
                continue
            elif '{' in line and '}' in line:
                continue
            elif '{' in line:
                bracks += 1
            elif '}' in line:
                if bracks == 1:
                    lines[ind] = '***'
                    break
                else:
                    bracks -= 1
            elif 'Component' in line:
                continue
            elif 'property' in line:
                continue
            elif 'signal' in line:
                continue
            else:
                if bracks == 1:
                    lines[ind] = '***'
                else:
                    print('')

        cc = [c for c in lines if c != '***']
        return cc

    def _find_part(self, query, lines):

        found = []
        bracks = 0
        ind = -1
        for line in lines:
            ind += 1
            if query in line:
                bracks += 1
                found.append(line.replace(query, ''))
                lines[ind] = '***'
                continue
            elif '{' in line and bracks > 0:
                found.append(line)
                bracks += 1
            elif '}' in line:
                if bracks > 0:
                    found.append(line)
                    lines[ind] = '***'
                    break
                else:
                    continue
            else:
                if bracks > 0:
                    found.append(line)
                    lines[ind] = '***'
                else:
                    print('')

        lines = [d for d in lines if d != '***']
        return found, lines

    def _pick_parent_props(self, lines):

        """
            Pick all components found in ApplicationWindow
            i.e:
                property
                signal
                onSignal
                Component functions
        """

        found = []
        go = False
        cont = False
        ind = -1
        for line in lines:
            ind += 1
            if 'Component' in line:
                if '}' in line:
                    continue
                else:
                    cont = True
                    continue
            elif 'on' in line and ':' in line:
                go = True
                found.append(line)
                lines[ind] = "****"
            elif '}' in line:
                if cont:
                    cont = False
                    continue
                elif go:
                    found.append(line)
                    lines[ind] = '****'
                    go = False
            elif '{' in line:
                break
            else:
                if cont:
                    continue
                else:
                    found.append(line)
                    lines[ind] = '****'

        lines = [n for n in lines if n != '****']
        return found, lines

    def _put_into_place(self, indent_len, query, bottom_lines, frame_lines):

        indent = " " * indent_len
        query_stat = indent + query
        begining_ind = frame_lines.index(query_stat) + 1

        no = begining_ind
        for line in bottom_lines:
            no += 1
            nline = indent + line
            frame_lines.insert(no, nline)

        return frame_lines

    def _put_in_part(self, indent_len, query, bottom_lines, frame_lines):

        # Start the search for the contentItem where we'll insert the users qml
        indent = " " * indent_len
        query_stat = indent + query
        begining_ind = frame_lines.index(query_stat) + 1

        no = begining_ind
        for line in bottom_lines:
            no += 1
            nline = indent + line
            frame_lines.insert(no, nline)

        return frame_lines
