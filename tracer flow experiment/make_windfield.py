import climt
import pickle

### climt setup ###

dycore = climt.GfsDynamicalCore(number_of_longitudes=198,
                                number_of_latitudes=198,
                                dry_pressure=1e5,
                                number_of_damped_levels=5,
                                number_of_tracers=1)

my_state = climt.get_default_state([dycore], x=dycore.grid_definition['x'],
                                   y=dycore.grid_definition['y'],
                                   mid_levels=dycore.grid_definition['mid_levels'],
                                   interface_levels=dycore.grid_definition['interface_levels'])


### Initial state ###

t = my_state['gfs_tracers'][dict(tracer_number=4, mid_levels=0)]
t[(t['longitude']>150) & (t['longitude']<160), (t['latitude']>55) & (t['latitude']<60)] = 1e-2
t[(t['longitude']>250) & (t['longitude']<260), (t['latitude']>30) & (t['latitude']<40)] = 1e-2
t[(t['longitude']>150) & (t['longitude']<160), (t['latitude']>-15) & (t['latitude']<0)] = 1e-2

my_state['northward_wind'].values[:] = 1e-15
my_state['eastward_wind'].values[:] = 1e-15

s = 150

n = my_state['northward_wind']
n[(n['longitude']>100) & (n['longitude']<101), (n['latitude']>-30) & (n['latitude']<30)] = s
n[(n['longitude']>150) & (n['longitude']<151), (n['latitude']>-30) & (n['latitude']<30)] = -s
n[(n['longitude']>200) & (n['longitude']<201), (n['latitude']>-30) & (n['latitude']<30)] = s
n[(n['longitude']>100) & (n['longitude']<201), (n['latitude']>40) & (n['latitude']<41)] = 0
n[(n['longitude']>100) & (n['longitude']<201), (n['latitude']>-41) & (n['latitude']<-40)] = 0

e = my_state['eastward_wind']
e[(e['longitude']>100) & (e['longitude']<150), (e['latitude']>40) & (e['latitude']<41)] = s
e[(e['longitude']>150) & (e['longitude']<201), (e['latitude']>40) & (e['latitude']<41)] = -s
e[(e['longitude']>100) & (e['longitude']<150), (e['latitude']>-41) & (e['latitude']<-40)] = -s
e[(e['longitude']>150) & (e['longitude']<201), (e['latitude']>-41) & (e['latitude']<-40)] = s


### Run the model ###

for i in range(400):
    output, diag = dycore(my_state)
    my_state.update(output)
    my_state.update(diag)


### Pickle the wind fields ###
    
east = my_state['eastward_wind']
north = my_state['northward_wind']

with open('./north.pickle', 'wb') as f:
    pickle.dump(north, f)
    
with open('./east.pickle', 'wb') as f:
    pickle.dump(east, f)