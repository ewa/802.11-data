import pandas as pd
import StringIO

class MCS_Table(object):

    def __init__(self, text, phy_type, chan_width, N_SS, N_ES, EQM):
        self.phy_type = phy_type
        self.chan_width_MHz = chan_width
        self.N_SS = N_SS
        self.N_ES = N_ES
        self.EQM = EQM
        self.text = text
        self.tab = self._panda()

    def __str__(self):
        return "{} PHY, {} MHz, {} SS, {} ES, EQM={}".format(
            self.phy_type,
            self.chan_width_MHz,
            self.N_SS,
            self.N_ES,
            self.EQM) ##+ "\n" + self.text

    def _panda(self):
        tab = pd.io.parsers.read_table(StringIO.StringIO(self.text))

        # Sanity checks
        ## Expect mod stream columns for each SS in UEQM
        if not self.EQM:
            for i_ss in range(self.N_SS):
                expected_col_name = "Mod. Stream {}".format(i_ss+1)
                if not expected_col_name in tab.columns:
                    raise ValueError("Table has UEQM, but no column '{}'".format(expected_col_name))
        else:
        ## Expect single modulation column if EQM
            if not "Mod." in tab.columns:
                raise ValueError("Table has EQM, but no column 'Mod.'")

        ## Expect N_ES if not specified for whole table
        if self.N_ES is None:
            if not "N_ES" in tab.columns:
                raise ValueError("Table has no defined N_ES, and no N_ES column")
        ## "Extend" with object-supplied attributes
        for (attr, name) in [(self.phy_type, 'PHY'),
                             (self.chan_width_MHz, 'Chan MHz'),
                             (self.N_SS, 'N_SS'),
                             (self.N_ES, 'N_ES')]:
            if attr is not None:
                tab[name]=attr
                
        return tab
