import matplotlib
import matplotlib.transforms as transforms
from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt

matplotlib.rc('font', size=11)

fname = './siesta.bands.gnu.dat'
fstring= './siesta.bands'

energies = [[]]
bands = [[]]

fermi = 0  # In case it is not found in file
with open(fname, 'r') as _file:
    for line in _file:
        if "E_F" in line:
            fermi = float(line.split()[-1])
            break

with open(fname) as _file:
    for i in range(15):
        next(_file)
    for line in _file:
        if not line.strip():
            energies.append([])
            bands.append([])

            continue
        line_parse = [float(i) for i in line.split()]
        energies[-1].append(line_parse[0])
        bands[-1].append(line_parse[1] - fermi)

fig, axes = plt.subplots(figsize=(10, 6))
for energy, band in zip(energies, bands):
    axes.plot(energy, band, 'k')

high_symetry = []
point_label = []
with open(fstring, 'r') as file:
    for line in file:
        if "'" in line:
            point_label.append(line.split()[-1])
            high_symetry.append(float(line.split()[0]))
          
for i in range(len(point_label)):
    point_label[i] = point_label[i].replace("'","")
point_label = [i if i != 'Gamma' else r'$\Gamma$' for i in point_label]


trans = transforms.blended_transform_factory(axes.transData, axes.transAxes)

for point, point_label in zip(high_symetry, point_label):
    axes.text(point, -0.05, point_label, transform=trans,
              horizontalalignment='center')

for point in high_symetry[1:-1]:
    axes.vlines(point, 0, 1, colors='k', transform=trans)

axes.hlines(0, high_symetry[0], high_symetry[-1],
            linestyle='dashed', colors='k')

axes.set_xlim((high_symetry[0], high_symetry[-1]))
Ei = float(input("Enter the lower limit of enery interval:"))
Ef = float(input("Enter the upper limit of enery interval:"))
axes.set_ylim((Ei, Ef))

axes.yaxis.set_minor_locator(AutoMinorLocator(2))

axes.tick_params(axis='x', which='both', bottom=False, top=False,
                 labelbottom=False)

axes.tick_params(axis='y', which='both', direction='in', left=True,
                 right=True, labelbottom=False)

axes.set_ylabel('Energy (eV)')

plt.savefig('band.pdf', bbox_inches='tight', transparent=True)
plt.show()
