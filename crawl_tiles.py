"""
Writes names of all tiles into a CSV file.
"""
import os
import pandas as pd

TILE_PATH = 'stonesoup'

data = []
for path, _, fnames in os.walk(TILE_PATH):
    if 'unused' in path:
        continue
    for fn in fnames:
        if fn.endswith('.png'):
            rec = (fn[:-4], os.path.join(path, fn), 0, 0, 32, 32)
            data.append(rec)

df = pd.DataFrame(data, columns=['name', 'file', 'x', 'y', 'w', 'h'])
print(df.shape)
print(len(df['name'].unique()))
df.to_csv('stonesoup.csv', index=False)
