from operator import le
import re
import os
import unicodedata
from numpy.__config__ import show
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

text = ""

with os.scandir('./fb_scraping/') as folder:
    for file in folder:
        if file.is_file() and file.name.endswith('.txt'):
            with open(file=file.path, encoding='utf-8') as f:
                text += f.read().strip()

text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
text = re.sub(r'[^A-Za-z\s]', '', text)
text = re.findall(r'\b[A-Za-z]{4,}', text)
print(f'N. Palabras: {len(text)}')
text = ' '.join(text)

x, y = np.ogrid[:800, :800]
mask = (x - 400) ** 2 + (y - 400) ** 2 > 130 ** 2
mask = 255 * mask.astype(int)

wordcloud = WordCloud(width=1366, height=968, background_color='white', max_words=500, colormap="inferno", collocations=False).generate(text)

plt.figure(figsize=(10, 10))
plt.imshow(wordcloud, interpolation='spline36')
plt.axis('off')  
plt.show()

