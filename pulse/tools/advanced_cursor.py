import numpy as np
import matplotlib.pyplot as plt

class AdvancedCursor(object):
    def __init__(self, ax, x, y, show_cursor, show_legend=False, number_vertLines=12):

        self.ax = ax
        self.x = x
        self.y = y
        self.show_cursor = show_cursor
        self.show_legend = show_legend
        self.number_vertLines = number_vertLines

        self.x_data_labels = []
        self.vertical_lines = []

        for _ in range(self.number_vertLines):
            # vertical lines
            self.vertical_lines.append(ax.axvline(ax.get_xbound()[0], visible=True, color='k', alpha=0.3, label='_nolegend_')) 
            # text labels of vertical lines
            self.x_data_labels.append(ax.text(1, 1, '', fontsize=6))
            
        # horizontal line 
        self.hl = self.ax.axhline(y=y[0], color='k', alpha=0.3, label='_nolegend_')  
        self.marker, = ax.plot(x[0], y[0], markersize=4, marker="s", color=[0,0,0], zorder=3)
        # self.marker.set_label("x: %1.2f // y: %4.2e" % (self.x[0], self.y[0]))

    def mouse_move(self, event):
            
        if not event.inaxes: 
            return
        
        x, y = event.xdata, event.ydata
        if x>=np.max(self.x): 
            return

        y_min, y_max = self.ax.get_ybound()
        dy = (y_max-y_min)/50
        y_pos = y_max - dy

        indx = np.searchsorted(self.x, [x])[0]
        
        x = self.x[indx]
        y = self.y[indx]
        for i in range(self.number_vertLines):
            if x*(i+1) > np.max(self.x):
                self.vertical_lines[i].set_visible(False)
                self.x_data_labels[i].set_visible(False)
            else:
                self.vertical_lines[i].set_xdata(x*(i + 1))
                if self.number_vertLines != 1:
                    self.x_data_labels[i].set_text(f'{i+1}x')
                    self.x_data_labels[i].set_position((x*(i+1), y_pos))
                    self.x_data_labels[i].set_visible(True)
                    self.vertical_lines[i].set_visible(True)
        
        # self.vl.set_xdata(x)
        self.hl.set_ydata(y)
        self.marker.set_data([x],[y])
        self.marker.set_label("x: %1.2f // y: %1.2f" % (x, y))

        if self.show_legend:
            plt.legend(handles=[self.marker], loc='lower left', title=r'$\bf{Cursor}$ $\bf{coordinates:}$')

        self.ax.figure.canvas.draw_idle()