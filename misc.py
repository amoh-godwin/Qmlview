

class Split():


    """
    Split Qml into different components
    """


    def __init__(self, filename, pick_comp=False):
        self.filename = filename
        self.pick_comp = pick_comp

        self.wind_user_props = {'title': 'title: qsTr("Qmlview")',
                                    'color': 'color: "white"'}
        self.orig_lines = []
        self.orig_imp_stats = []
        self.orig_bottom_lines = []

        self.prop_lines = []
        self.menubar_lines = []
        self.header_lines = []
        self.footer_lines = []

        self.split()

    def split(self):
        with open(self.filename, 'r') as orig_file:
            self.orig_lines = orig_file.readlines()

        # get import statements so we can add them
        self.orig_imp_stats = [n for n in self.orig_lines if n.startswith('import')]
        # last index of the import stats for the original files
        orig_imp_last_ind = self.orig_lines.index(self.orig_imp_stats[-1]) + 1
        self.orig_bottom_lines = self.orig_lines[orig_imp_last_ind:]

        # Delete ApplicationWindow
        self.orig_bottom_lines = self._del_parts(
                'ApplicationWindow {', self.orig_bottom_lines)

        # Pick all properties and comps in ApplicationWindow
        self.prop_lines, self.orig_bottom_lines = self._pick_parent_props(self.orig_bottom_lines)

        self.menubar_lines, self.orig_bottom_lines = self._find_part('menuBar:',
                                                          self.orig_bottom_lines)

        self.header_lines, self.orig_bottom_lines = self._find_part('header:',
                                                          self.orig_bottom_lines)

        self.footer_lines, self.orig_bottom_lines = self._find_part('footer:',
                                                          self.orig_bottom_lines)

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
                    # save the title and color
                    # then delete them
                    if 'title' in line:
                        self.wind_user_props['title'] = line.strip()
                    elif 'color' in line:
                        self.wind_user_props['color'] = line.strip()
                    elif 'width' in line:
                        self.wind_user_props['width'] = line.strip()
                    elif 'height' in line:
                        self.wind_user_props['height'] = line.strip()

                    lines[ind] = '***'
                else:
                    pass

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
                    pass

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
        keep_going = False
        cont = False
        ind = -1
        for line in lines:
            ind += 1
            if 'Component' in line:
                if self.pick_comp:
                    go = True
                    found.append(line)
                    lines[ind] = "****"
                else:
                    if '}' in line:
                        continue
                    else:
                        cont = True
                        continue
            elif 'on' in line and ':' in line:
                go = True
                found.append(line)
                lines[ind] = "****"
            elif '{' in line and '(' in line:
                # this is a statement inside an a signal handler
                keep_going = True
                found.append(line)
                lines[ind] = '****'
            elif '}' in line and '{' in line and keep_going:
                # an else statement in a signal handler
                found.append(line)
                lines[ind] = '****'
            elif '}' in line and keep_going:
                # This is probably an end statement in the stat in handler
                found.append(line)
                lines[ind] = '****'
                keep_going = False
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

    def pick_comp(self, lines):
        """
            Pick components found in ApplicationWindow
            i.e:
                Component functions
        """

        found = []
        go = False
        keep_going = False
        cont = False
        ind = -1
        for line in lines:
            ind += 1
            if 'Component' in line and ':' in line:
                go = True
                found.append(line)
                lines[ind] = "****"
            elif 'on' in line and ':' in line:
                go = True
                found.append(line)
                lines[ind] = "****"
            elif '{' in line and '(' in line:
                # this is a statement inside an a signal handler
                keep_going = True
                found.append(line)
                lines[ind] = '****'
            elif '}' in line and '{' in line and keep_going:
                # an else statement in a signal handler
                found.append(line)
                lines[ind] = '****'
            elif '}' in line and keep_going:
                # This is probably an end statement in the stat in handler
                found.append(line)
                lines[ind] = '****'
                keep_going = False
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
