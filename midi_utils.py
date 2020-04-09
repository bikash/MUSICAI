import pretty_midi
import collections
import pandas as pd
import bokeh
import bokeh.plotting
from IPython import display
import numpy as np

def plot_noteSequence(filename, show_figure=True):
    midi = pretty_midi.PrettyMIDI(filename)
    pd_dict = collections.defaultdict(list)
    for instrument in midi.instruments:
        program = instrument.program
        name = instrument.name
        if instrument.is_drum:
            for note in instrument.notes:
                pd_dict['start_time'].append(note.start)
                pd_dict['end_time'].append(note.end)
                pd_dict['duration'].append(note.end - note.start)
                pd_dict['pitch'].append(note.pitch)
                pd_dict['bottom'].append(note.pitch - 0.4)
                pd_dict['top'].append(note.pitch + 0.4)
                pd_dict['velocity'].append(note.velocity)
                pd_dict['fill_alpha'].append(note.velocity / 128.0)
                pd_dict['instrument'].append(name)
                pd_dict['program'].append(program)
    # If no velocity differences are found, set alpha to 1.0.
    if np.max(pd_dict['velocity']) == np.min(pd_dict['velocity']):
        pd_dict['fill_alpha'] = [1.0] * len(pd_dict['fill_alpha'])
    dataframe=pd.DataFrame(pd_dict)
    # These are hard-coded reasonable values, but the user can override them
    # by updating the figure if need be.
    fig = bokeh.plotting.figure(tools='hover,pan,box_zoom,reset,previewsave')
    fig.plot_width = 800
    fig.plot_height = 500
    fig.xaxis.axis_label = 'time (sec)'
    fig.yaxis.axis_label = 'pitch (MIDI)'
    spectral_color_indexes = [7, 0, 6, 1, 5, 2, 3]
    instruments = sorted(set(dataframe['instrument']))
    grouped_dataframe = dataframe.groupby('instrument')
    for counter, instrument in enumerate(instruments):
        instrument_df = grouped_dataframe.get_group(instrument)
        color_idx = spectral_color_indexes[counter % len(spectral_color_indexes)]
        color = bokeh.palettes.Spectral8[color_idx]
        source = bokeh.plotting.ColumnDataSource(instrument_df)
        fig.quad(top='top', bottom='bottom', left='start_time', right='end_time',
                 line_color='black', fill_color=color,
                 fill_alpha='fill_alpha', source=source)
    fig.select(dict(type=bokeh.models.HoverTool)).tooltips = (
          {'pitch': '@pitch',
           'duration': '@duration',
           'start_time': '@start_time',
           'end_time': '@end_time',
           'velocity': '@velocity'})

    if show_figure:
        bokeh.plotting.output_notebook()
        bokeh.plotting.show(fig)
        return None
    return fig