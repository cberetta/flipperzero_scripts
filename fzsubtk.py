#!/bin/python

# Imports
import argparse
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MaxNLocator

class fzsubtk():

    # Some class params
    select_from  = 0
    select_to    = 0
    grid_step    = 0
    timing_as_ticks = False
    timing_num_as_ticks = False
    keep_all_ticks = False

    _sub_data = []
    _sub_header = []

    _xx=[0]
    _yy=[0]
    _tt=[0]
    _tl1=['']
    _tl2=['']

    # === Load .sub file
    def LoadSubFile(self, filename):
        self._sub_data = []
        with open(filename, "r") as f:
            for line in f:
                if "RAW_Data:" in line:
                    for timing in line[9:].split():
                        self._sub_data.append(int(timing.strip()))
                else:
                    self._sub_header.append(line)


    # === Cut .sub file
    def CutSubFile(self, filename):

        # Load .sub file
        self.LoadSubFile(filename)

        # Cut data
        MAX_TIMINGS_PER_LINE = 512
        with open(self.output, "w") as f:
            for line in self._sub_header:
                f.write(line)
            line = "RAW_Data:"
            for cnt, val in enumerate(self._sub_data):
                if (cnt >= self.select_from) and ((cnt <= self.select_to) or (self.select_to == 0)):
                    line = "{} {}".format(line, val)
                    if cnt % MAX_TIMINGS_PER_LINE == 0:
                        f.write("{}\n".format(line))
                        line = "RAW_Data:"
            # Write last line if necessary
            if (line != "RAW_Data:"):
                f.write("{}\n".format(line))

        # Some infos
        print("Total timings in .sub file...: {}".format(len(self._sub_data)))
        print("Timings cutted to {}".format(self.output))


    # === Plot .sub file
    def PlotSubFile(self, filename):
        x=0

        # Load .sub file
        self.LoadSubFile(filename)

        # Build array for plotting
        for cnt, val in enumerate(self._sub_data):
            if (cnt >= self.select_from) and ((cnt <= self.select_to) or (self.select_to == 0)):
                x = x + abs(val)
                #print("cnt:{:6} - val:{:6} - x:{:6}".format(cnt, val, x))
                self._xx.append(x)
                self._tt.append(x)
                self._tl1.append(cnt)
                self._tl2.append(abs(val))
                if val > 0:
                    self._yy.append(1)
                else:
                    self._yy.append(0)

        # Some info
        print("Total timings in .sub file...: {}".format(len(self._sub_data)))
        print("Total timings plotted........: {}".format(len(self._xx)))
        print("Total time...................: {}".format(x))

        # Keep only some of the ticks (i do not like this, TODO: rewrite)
        if not self.keep_all_ticks:
            tick_step = int(len(self._tl1) / 25)
            if tick_step == 0:
                tick_step = 1
            for cnt, val in reversed(list(enumerate(self._tl1[:-1]))):
                if (cnt % tick_step) != 0:
                    del self._tt[cnt]
                    del self._tl1[cnt]
                    del self._tl2[cnt]

        # Plot
        fig = plt.figure()
        fig.set_size_inches(10, 2)
        ax = fig.add_subplot(1, 1, 1)

        # Set x grid step
        if self.grid_step > 0:
            major_ticks = np.arange(0, (x + self.grid_step), self.grid_step)
            ax.set_xticks(major_ticks)

        # Some axis config
        ax.grid(which='both', axis='x', alpha=0.75, color='red')
        ax.yaxis.set_visible(False)
        ax.tick_params(axis='both', labelsize='6')

        # Use timing as ticks
        if self.timing_as_ticks:
            ax.set_xticks(self._tt)
            ax.set_xticklabels(self._tl2)
        # Use timing num as ticks
        if self.timing_num_as_ticks:
            ax.set_xticks(self._tt)
            ax.set_xticklabels(self._tl1)

        # Some plt config
        plt.tight_layout()
        plt.ylim([-0.5, 1.5])

        # Plot a step-plot
        plt.step(self._xx, self._yy, where='pre')

        # Show the plot
        plt.show()



# -----
if __name__ == '__main__':

    # Create parser for arguments
    parser = argparse.ArgumentParser(description="FlipperZero .sub ToolKit")

    # Add arguments to parser
    parser.add_argument('-f', '--select-from',
        required=False,
        type=int,
        action='store',
        default=0,
        help="Select FROM")

    parser.add_argument('-t', '--select-to',
        required=False,
        type=int,
        action='store',
        default=0,
        help="Select TO")

    parser.add_argument('-g', '--grid-step',
        required=False,
        type=int,
        action='store',
        default=0,
        help="Grid step")

    parser.add_argument('-s', '--subfile',
        required=True,
        action='store',
        default='',
        help="sub file to work on")

    parser.add_argument('-m', '--timing-as-ticks',
        required=False,
        action='store_true',
        default=False,
        help="use timing for x axis ticks")

    parser.add_argument('-n', '--timing-num-as-ticks',
        required=False,
        action='store_true',
        default=False,
        help="use timing number for x axis ticks")

    parser.add_argument('-k', '--keep-all-ticks',
        required=False,
        action='store_true',
        default=False,
        help="keep ALL ticks on the axis")

    parser.add_argument('-o', '--output',
        required=False,
        action='store',
        default='cutted.sub',
        help="destination sub file [default:cutted.sub]")

    parser.add_argument('-p', '--plot',
        required=False,
        action='store_true',
        default=True,
        help="plot the .sub file")

    parser.add_argument('-c', '--cut',
        required=False,
        action='store_true',
        default=False,
        help="cut the .sub file")

    # Parse arguments
    args = parser.parse_args()

    # Create object
    subtk = fzsubtk()
    # Setup params
    subtk.select_from = args.select_from
    subtk.select_to = args.select_to
    subtk.grid_step = args.grid_step
    subtk.timing_as_ticks = args.timing_as_ticks
    subtk.timing_num_as_ticks = args.timing_num_as_ticks
    subtk.keep_all_ticks = args.keep_all_ticks
    subtk.output = args.output

    if args.cut:
        subtk.CutSubFile(args.subfile)
    elif args.plot:
        subtk.PlotSubFile(args.subfile)



