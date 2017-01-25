# -*- coding: utf-8 -*-


from itertools import cycle
import sys
from time import sleep


class ProgressBar(object):
    """Visualize a status bar on the console."""

    def __init__(self, max_width, label):
        """Prepare the visualization."""
        self.max_width = max_width
        self.spin = next(cycle(r'-\|/'))
        self.tpl = '%-' + str(max_width) + 's ] %c %5.1f%%'
        show(label)
        show(' [ ')
        self.last_output_length = 0

    def update(self, percent):
        """Update the visualization."""
        # Remove last state.
        show('\b' * self.last_output_length)

        # Generate new state.
        width = int(percent / 100.0 * self.max_width)
        output = self.tpl % ('-' * width, self.spin, percent)

        # Show the new state and store its length.
        show(output)
        self.last_output_length = len(output)


def show(string):
    """Show a string instantly on STDOUT."""
    sys.stdout.write(string)
    sys.stdout.flush()


def percentize(steps):
    """Generate percental values."""
    for i in range(steps + 1):
        yield i * 100.0 / steps

if __name__ == '__main__':
    # An example progress bar with 40 segments,
    # filled in 20 steps, updated every 0.1 seconds.
    sb = ProgressBar(40, 'processing')
    for percent in percentize(20):
        sb.update(percent)
        sleep(0.1)
    show('\n')
