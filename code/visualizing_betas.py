from matplotlib import pyplot as plt
import seaborn as sns
import json
import matplotlib.cm as cm

# help from: https://matplotlib.org/3.1.0/tutorials/colors/colormaps.html
# cmaps = OrderedDict()
# cmaps['Diverging'] = [
#             'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
#             'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']


def visualize_beta():
	x = []
	y = []
	z = []

	with open('june4test.json') as f:
		for l in f:
			line = json.loads(l)
			for user_id, vals in line.items():
				if vals['beta'] != 'No beta can be calculated' and abs(vals['beta']) < 10 :
					for i in range(len(vals['lats'])):
						lat = vals['lats'][i]
						lon = vals['lons'][i]
						b = vals['beta']

						y.append(lat)
						x.append(lon)
						z.append(b)

		plt.scatter(x, y, marker='o', c=z)
		plt.title("Beta Distribution")
		plt.xlabel("Lat")
		plt.ylabel("Long")
		cbar = plt.colorbar()
		cbar.set_label("Beta Value", labelpad=+1)
		plt.show()

if __name__ == '__main__':
  visualize_beta()