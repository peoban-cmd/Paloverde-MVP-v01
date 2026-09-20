import re, sys
import pandas as pd
from pathlib import Path
from datetime import date


import numpy as np
from pylatex import Table, Tabular, MultiColumn
from pylatex import Document, Section, Subsection, Command, Package # Tabular, NewPage
from pylatex import Math, TikZ, Axis, Plot, Figure, SubFigure, NoEscape, Matrix, Alignat
from pylatex.utils import italic
import os

debug = True
if debug:
    project_path = Path("/home/pedro/Documents/PaloVerde/Project")
else:
    project_path = Path(sys.argv[1])

figPath = project_path / "Results" / "WeeklyReport"
Two_Figs_Width = 0.49

figPath.mkdir(parents=True, exist_ok=True)
report_date = date.today().strftime('%d-%b-%Y')

if __name__ == '__main__':
	# image_filename = os.path.join(os.path.dirname(__file__), 'kitten.jpg')

	geometry_options = {"tmargin": "1cm","bmargin": "2cm", "lmargin": "2cm","landscape":True}
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

	with doc.create(Section(f'Resumen producción de leche al día {report_date}')):
		# doc.append(f'Thermal comfort maps for {locationName}.')
		figure_rows = []
		# figure1 = {'name': 'ProduccionLeche','caption':'Producción total de leche.'}
		figure1 = {'name': 'ProduccionTotalLeche', 'caption': 'Producción total de leche.'}
		figure2 = {'name': 'LecheQueso', 'caption': 'Producción total de leche.'}
		figure3 = {'name': 'PromedioLechePorVaca', 'caption': 'Promedio leche por vaca.'}
		figure4 = {'name': 'VacasOrdenadas', 'caption': 'Vacas ordeñadas.'}

		figureNames = [figure1,figure2,figure3]
		# for figureName in figureNames:
		# 	with doc.create(Figure(position='!htb')) as new_fig:
		# 		new_fig.add_image(f'{project_path}/Results/milk_production/{figureName["name"]}', width="10cm")
		# 		new_fig.add_caption(f'{figureName["caption"]}')
		#
		leftFigWidth = 0.5
		row1 = {'left':figure1 , 'right':figure2}
		row2 = {'left': figure3, 'right': figure4}
		figure_rows = [row1,row2]
		for figure_row in figure_rows:
			with doc.create(Figure(position='!htb')) as main_figure:
				with doc.create(SubFigure(width=NoEscape(fr'{leftFigWidth}\linewidth'))) as left_fig:
					left_fig.add_image(f'{project_path}/Results/milk_production/{figure_row['left']["name"]}',
									   width=NoEscape(r'\linewidth'))
					# left_fig.add_caption(f'{subFig_left["caption"]}')

				with doc.create(SubFigure(width=NoEscape(fr'{1-leftFigWidth}\linewidth'))) as right_fig:
					right_fig.add_image(f'{project_path}/Results/milk_production/{figure_row['right']["name"]}',
										width=NoEscape(r'\linewidth'))
					# right_fig.add_caption(f'{subFig_right["caption"]}')
			# main_figure.add_caption(f'{figureName["caption"]}')

		doc.append(Command('newpage'))
		# Add table

		# 1. Create a sample Pandas DataFrame
		df = pd.DataFrame({
			"ID": [101, 102, 103],
			"Product": ["Widget A", "Widget B", "Widget C"],
			"Price ($)": [29.99, 49.50, 15.00]
		})


		with doc.create(Section("Pandas to PyLaTeX")):
			with doc.create(Table(position="h!")) as table:
				table.add_caption("Data Populated from Pandas DataFrame")

				# Define tabular alignment matching number of columns (3 columns)
				with doc.create(Tabular("|c|l|c|")) as tabular:
					tabular.add_hline()

					# Add column names as the header row
					tabular.add_row(list(df.columns))
					tabular.add_hline()
					tabular.add_hline()

					# Fill table row-by-row directly from DataFrame values
					for row in df.itertuples(index=False):
						tabular.add_row(list(row))
						tabular.add_hline()


	# with doc.create(Section(f'Thermal stress distribution for {locationName}')):
	# 	figure2 = {'name': 'thermal_stress_distributionCopernicus','path':'[8,20]', 'caption': 'Thermal stress distribution from '}
	# 	figure3 = {'name': 'thermal_stress_distributionCopernicus', 'path': '[0,23]','caption': 'Thermal stress distribution from '}
	# 	figureNames = [figure2,figure3]
	# 	for figureName in figureNames:
	# 		with doc.create(Figure(position='!htb')) as utci_maps_fig:
	# 			utci_maps_fig.add_image(f'{figPath}/Time{figureName["path"]}/{figureName["name"]}', width="17cm")
	# 			utci_maps_fig.add_caption(f'{figureName["caption"]}{figureName["path"]} h')
	#
	# 	subFig_left = {'path': 'Time[8,20]', 'caption': '[8,20] h'}
	# 	subFig_right = {'path': 'Time[0,23]', 'caption': 'All day'}
	# 	figure1 = {'name': 'annual_thermal_stress_acceptable_Copernicus','caption':'Acceptable annual thermal stress.'}
	# 	figureNames = [figure1]
	# 	for figureName in figureNames:
	# 		with doc.create(Figure(position='!htb')) as main_figure:
	# 			with doc.create(SubFigure(width=NoEscape(f'{Two_Figs_Width}\linewidth'))) as left_fig:
	# 				left_fig.add_image(f'{figPath}/{subFig_left["path"]}/{figureName["name"]}',
	# 								   width=NoEscape(r'\linewidth'))
	# 				left_fig.add_caption(f'{subFig_left["caption"]}')
	#
	# 			with doc.create(SubFigure(width=NoEscape(f'{Two_Figs_Width}\linewidth'))) as right_fig:
	# 				right_fig.add_image(f'{figPath}/{subFig_right["path"]}/{figureName["name"]}',
	# 									width=NoEscape(r'\linewidth'))
	# 				right_fig.add_caption(f'{subFig_right["caption"]}')
	# 			main_figure.add_caption(f'{figureName["caption"]}')
	#
	# 	doc.append(Command('newpage'))
	# with doc.create(Section(f'Mitigation strategies for {locationName}')):
	# 	timePath = 'Time[0,23]'
	#
	# 	figure1 = {'name': 'Wind and sun exposure','caption': 'Wind and sun exposure'}
	# 	figure2 = {'name': 'Wind protection', 'caption': 'Wind protection'}
	# 	figure3 = {'name': 'Sun protection', 'caption': 'Sun protection'}
	# 	figure4 = {'name': 'Wind and sun protection', 'caption': 'Wind and sun protection'}
	# 	figureNames = [figure1, figure2, figure3, figure4]
	# 	doc.append(f'Effect of {len(figureNames)} different mitigation strategies on the annual thermal stress considering the whole day.')
	# 	leftFigWidth = 0.43
	# 	for figureName in figureNames:
	# 		with doc.create(Figure(position='!htb')) as main_figure:
	# 			with doc.create(SubFigure(width=NoEscape(f'{leftFigWidth}\linewidth'))) as left_fig:
	# 				left_fig.add_image(f'{figPath}/{timePath}/annual_thermal_stress_analysis_{figureName["name"]}',
	# 								   width=NoEscape(r'\linewidth'))  # Replace with your image path
	# 				# left_fig.add_caption(f'{subFig_left["caption"]}')
	#
	# 			with doc.create(SubFigure(width=NoEscape(f'{1-leftFigWidth}\linewidth'))) as right_fig:
	# 				right_fig.add_image(f'{figPath}/{timePath}/utci_Categories_{figureName["name"]}NoColorBar',
	# 									width=NoEscape(r'\linewidth'))  # Replace with your image path
	# 				# right_fig.add_caption(f'{subFig_right["caption"]}')
	# 		main_figure.add_caption(f'{figureName["caption"]}')
	#
	# 	timePath = 'Time[8,20]'
	# 	leftFigWidth = 0.49
	# 	doc.append(Command('newpage'))
	# 	# doc.append(
	# 	# 	f'Effect of {len(figureNames)} different mitigation strategies on the annual thermal stress considering from [8,20] h.')
	#
	# 	with doc.create(Figure(position='!htb')) as main_figure:
	# 		for counter, figureName in enumerate(figureNames):
	# 			with doc.create(SubFigure(width=NoEscape(f'{Two_Figs_Width}\linewidth'))) as sub_fig:
	# 				sub_fig.add_image(f'{figPath}/{timePath}/annual_thermal_stress_acceptable_{figureName["name"]}',
	# 								   width=NoEscape(r'\linewidth'))
	# 				sub_fig.add_caption(f'{figureName["caption"]}')
	# 			if counter == 1:
	# 				doc.append(NoEscape(r'\\'))
	# 		main_figure.add_caption(f'Effect of {len(figureNames)} different mitigation strategies on the acceptable thermal stress from [8,20] h.')

	# Creating a pdf
	doc.generate_pdf(f'{figPath}/Report{report_date}', clean_tex=False)

print(f'Report generated successfully!')