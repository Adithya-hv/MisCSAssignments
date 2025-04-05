import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('./output/results.csv')

for size in data['Matrix Size'].unique():
    subset = data[data['Matrix Size'] == size]
    plt.plot(subset['Block Size'],
             subset['Blocked Time (ms)'], label=f"Size {size}")

plt.xlabel('Block Size')
plt.ylabel('Average Time (ms)')
plt.title('Blocked Transpose Performance')
plt.legend()
block_sizes = data['Block Size'].unique()
powers_of_2 = [
    2**i for i in range(int(np.log2(min(block_sizes))), int(np.log2(max(block_sizes))) + 1)]
plt.xticks(powers_of_2, labels=[f"{x}" for x in powers_of_2])

plt.show()
