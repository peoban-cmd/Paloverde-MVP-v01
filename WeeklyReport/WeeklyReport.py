import re
import sys

import numpy as np

from pylatex import Document, Section, Subsection, Command, Package # Tabular, NewPage
from pylatex import Math, TikZ, Axis, Plot, Figure, SubFigure, NoEscape, Matrix, Alignat
from pylatex.utils import italic
import os


debug = False
if debug:
	figPath = '/home/pedro/Documents/ThermalComfort/Output/Figures/Castelfranco_[45.67,11.92]_2023'
else:
	figPath = sys.argv[1]

locationName = re.sub('.*\/','',figPath)
locationName = re.sub('_.*','',locationName)
Two_Figs_Width = 0.49

if __name__ == '__main__':
	# image_filename = os.path.join(os.path.dirname(__file__), 'kitten.jpg')

	geometry_options = {"tmargin": "2cm","bmargin": "2cm", "lmargin": "2cm"}
	doc = Document(geometry_options=geometry_options)
	# doc.packages.append(Package('hyperref'))
	# doc.preamble.append(NoEscape(r'''
	# \hypersetup{
	#     colorlinks=true,  % Enable colored links
	#     linkcolor=blue,   % Color for section links
	#     urlcolor=blue,    % Color for external links
	#     bookmarks=true,   % Enable PDF bookmarks (outline)
	#     pdfpagemode=UseOutlines  % Show outline on open
	# }
	# '''))

	with doc.create(Section(f'Summary')):
		doc.append(f'This document presents the main results of the simplified UTCI analysis for {locationName}.')
	with doc.create(Section(f'Thermal comfort maps for {locationName}')):
		# doc.append(f'Thermal comfort maps for {locationName}.')
		figure1 = {'name': 'utci_heatMap_Copernicus','caption':'UTCI heat map.'}
		figure2 = {'name': 'utci_Categories_Copernicus', 'caption': 'UTCI categories.'}
		figureNames = [figure1,figure2]
		for figureName in figureNames:
			with doc.create(Figure(position='!htb')) as utci_maps_fig:
				utci_maps_fig.add_image(f'{figPath}/Time[0,23]/{figureName["name"]}', width="18cm")
				utci_maps_fig.add_caption(f'{figureName["caption"]}')

		doc.append(Command('newpage'))
	with doc.create(Section(f'Thermal stress distribution for {locationName}')):
		figure2 = {'name': 'thermal_stress_distributionCopernicus','path':'[8,20]', 'caption': 'Thermal stress distribution from '}
		figure3 = {'name': 'thermal_stress_distributionCopernicus', 'path': '[0,23]','caption': 'Thermal stress distribution from '}
		figureNames = [figure2,figure3]
		for figureName in figureNames:
			with doc.create(Figure(position='!htb')) as utci_maps_fig:
				utci_maps_fig.add_image(f'{figPath}/Time{figureName["path"]}/{figureName["name"]}', width="17cm")
				utci_maps_fig.add_caption(f'{figureName["caption"]}{figureName["path"]} h')

		subFig_left = {'path': 'Time[8,20]', 'caption': '[8,20] h'}
		subFig_right = {'path': 'Time[0,23]', 'caption': 'All day'}
		figure1 = {'name': 'annual_thermal_stress_acceptable_Copernicus','caption':'Acceptable annual thermal stress.'}
		figureNames = [figure1]
		for figureName in figureNames:
			with doc.create(Figure(position='!htb')) as main_figure:
				with doc.create(SubFigure(width=NoEscape(f'{Two_Figs_Width}\linewidth'))) as left_fig:
					left_fig.add_image(f'{figPath}/{subFig_left["path"]}/{figureName["name"]}',
									   width=NoEscape(r'\linewidth'))
					left_fig.add_caption(f'{subFig_left["caption"]}')

				with doc.create(SubFigure(width=NoEscape(f'{Two_Figs_Width}\linewidth'))) as right_fig:
					right_fig.add_image(f'{figPath}/{subFig_right["path"]}/{figureName["name"]}',
										width=NoEscape(r'\linewidth'))
					right_fig.add_caption(f'{subFig_right["caption"]}')
				main_figure.add_caption(f'{figureName["caption"]}')

		doc.append(Command('newpage'))
	with doc.create(Section(f'Mitigation strategies for {locationName}')):
		timePath = 'Time[0,23]'

		figure1 = {'name': 'Wind and sun exposure','caption': 'Wind and sun exposure'}
		figure2 = {'name': 'Wind protection', 'caption': 'Wind protection'}
		figure3 = {'name': 'Sun protection', 'caption': 'Sun protection'}
		figure4 = {'name': 'Wind and sun protection', 'caption': 'Wind and sun protection'}
		figureNames = [figure1, figure2, figure3, figure4]
		doc.append(f'Effect of {len(figureNames)} different mitigation strategies on the annual thermal stress considering the whole day.')
		leftFigWidth = 0.43
		for figureName in figureNames:
			with doc.create(Figure(position='!htb')) as main_figure:
				with doc.create(SubFigure(width=NoEscape(f'{leftFigWidth}\linewidth'))) as left_fig:
					left_fig.add_image(f'{figPath}/{timePath}/annual_thermal_stress_analysis_{figureName["name"]}',
									   width=NoEscape(r'\linewidth'))  # Replace with your image path
					# left_fig.add_caption(f'{subFig_left["caption"]}')

				with doc.create(SubFigure(width=NoEscape(f'{1-leftFigWidth}\linewidth'))) as right_fig:
					right_fig.add_image(f'{figPath}/{timePath}/utci_Categories_{figureName["name"]}NoColorBar',
										width=NoEscape(r'\linewidth'))  # Replace with your image path
					# right_fig.add_caption(f'{subFig_right["caption"]}')
			main_figure.add_caption(f'{figureName["caption"]}')

		timePath = 'Time[8,20]'
		leftFigWidth = 0.49
		doc.append(Command('newpage'))
		# doc.append(
		# 	f'Effect of {len(figureNames)} different mitigation strategies on the annual thermal stress considering from [8,20] h.')

		with doc.create(Figure(position='!htb')) as main_figure:
			for counter, figureName in enumerate(figureNames):
				with doc.create(SubFigure(width=NoEscape(f'{Two_Figs_Width}\linewidth'))) as sub_fig:
					sub_fig.add_image(f'{figPath}/{timePath}/annual_thermal_stress_acceptable_{figureName["name"]}',
									   width=NoEscape(r'\linewidth'))
					sub_fig.add_caption(f'{figureName["caption"]}')
				if counter == 1:
					doc.append(NoEscape(r'\\'))
			main_figure.add_caption(f'Effect of {len(figureNames)} different mitigation strategies on the acceptable thermal stress from [8,20] h.')

	# Creating a pdf
	doc.generate_pdf(f'{figPath}/{locationName} Report', clean_tex=False)
