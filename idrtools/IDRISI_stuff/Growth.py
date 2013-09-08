import win32com.client
api   = win32com.client.Dispatch('idrisi32.IdrisiAPIServer')
name  = 'residential91.rst'
times = 5
for i in range(1, times):
    api.RunModule('FILTER',  name + '*proximity.rst*7*Filter2.fil*1', 1, '', '', '', '', 1)
    api.RunModule('RANDOM',  'ramdom seed.rst*1*2*landuse91.rst*2*0.02*0.01', 1, '', '', '', '', 1)
    api.RunModule('RECLASS', 'I*' + name + '*non-residential.rst*3*Reverse.rcl', 1, '', '', '', '', 1)
    api.RunModule('OVERLAY', '3*ldressuit.rst*proximity.rst*downweight.rst', 1, '', '', '', '', 1)
    api.RunModule('OVERLAY', '9*downweight.rst*random seed.rst*combined suit.rst', 1, '', '', '', '', 1)
    api.RunModule('OVERLAY', '3*combined suit.rst*forest91.rst*suit within forest.rst', 1, '', '', '', '', 1)
    api.RunModule('OVERLAY', '3*non-residential.rst*suit within forest.rst*final suitability.rst', 1, '', '', '', '', 1)
    api.RunModule('STRETCH', 'final suitability.rst*rescaled.rst*1*min*max*N*256*unspecified', 1, '', '', '', '', 1)
    api.RunModule('RANK',    'rescaled.rst*none*ranked suitability.rst*D', 1, '', '', '', '', 1)
    api.RunModule('RECLASS', 'I*ranked suitability.rst*best areas.rst*3*Growth.rcl', 1, '', '', '', '', 1)
    name = 'rew resid_' + str(i) + '.rst'
    api.RunModule('OVERLAY', '7*best areas.rst*residential91.rst*' + name , 1, '', '', '', '', 1)
    api.RunModule('OVERLAY', '1*' + name + '*residential91.rst*growth_' + str(i) + '.rst', 1, '', '', '', '', 1)
api.DisplayFile('growth_' + str(i) + '.rst', 'idris256');
