from matplotlib import pyplot as plt
import seaborn as sns
import json
import matplotlib.cm as cm


def visualize_beta():
	'''
	This function takes in the betas (correlation coefficients) from each 
	user as well as their geographic location for each tweet. Then, a 
	geographic scatter plot was made were point color was alligned on a scale 
	related to their beta value.
	'''
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
		plt.xlabel("Long")
		plt.ylabel("Lat")
		cbar = plt.colorbar()
		cbar.set_label("Beta Value", labelpad=+1)
		plt.show()


if __name__ == '__main__':
  visualize_beta()