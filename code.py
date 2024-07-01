# Cargar librerías
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML
import matplotlib.pyplot as plt
import numpy as np

# Cargar datos
url = 'https://github.com/serhrnz/TTDI/raw/main/TTDI_2021.xlsx'
df = pd.read_excel(url)

# Definir la lista de países para comparación
economies = df['Economy'].to_list()

# Crear una lista con las columnas de Score
score_columns = ['Economy'] + \
    [col for col in df.columns if any(suffix in col for suffix in ['-SCORE', '-Score'])] + \
    [
        "International tourist arrivals, thousands-Value",
        "International tourism inbound receipts  (inbound US$, millions)-Value",
        "T&T industry GDP, US$ million-Value",
        "T&T industry Employment, 1,000 jobs-Value",
        "T&T industry Share of GDP, % of total GDP-Value",
        "T&T industry Share of Employment, % of total employment-Value",
        "Domestic T&T spending, % of internal T&T spending-Value"
    ]

# Filtrar el DataFrame para conservar solo las columnas con '-Score'
df = df[score_columns].copy()

# Eliminar el sufijo '-Score' de todas las columnas en df_score
df.columns = df.columns.str.replace('-Score', '', case=False)
df.columns = df.columns.str.replace('-Value', ' (Value)', case=False)

df.index = df['Economy']
df.drop(columns=['Economy'], inplace=True)

df = df.transpose()

# Iniciar grupos para comparación
group1 = []
group2 = []
group1_name = "Grupo 1"
group2_name = "Grupo 2"

# Preguntar al usuario cuántos elementos contendrá el grupo 1
num_elements_label = widgets.Label("¿Cuántos elementos tendrá el grupo 1?")
num_elements_input = widgets.BoundedIntText(min=1, max=len(economies), step=1, value=1)

# Contenedor para los desplegables
dropdown_container = widgets.VBox()

# Contenedor para el nombre del grupo
group_name_input = widgets.Text(description="Nombre del grupo:", layout=widgets.Layout(display='flex', flex_flow='column', align_items='stretch'))

# Botón para guardar la selección
save_button = widgets.Button(description="Guardar selección")

# Contenedor combinado para el nombre del grupo y el botón de guardar
group_name_and_save_container = widgets.VBox([group_name_input, save_button])

# Función para generar los desplegables
def generate_dropdowns(num_elements):
    dropdowns = []
    for i in range(num_elements):
        dropdown = widgets.Dropdown(options=economies, description=f'Elemento {i + 1}:')
        dropdowns.append(dropdown)
    dropdown_container.children = dropdowns
    display(group_name_and_save_container)

# Botón para generar los desplegables
generate_button = widgets.Button(description="Aceptar")

# Acción del botón para generar los desplegables
def on_generate_button_click(b):
    generate_dropdowns(num_elements_input.value)

generate_button.on_click(on_generate_button_click)

# Contenedor para la segunda selección de grupo
dropdown_container2 = widgets.VBox()

# Contenedor para el nombre del segundo grupo
group_name_input2 = widgets.Text(description="Nombre del grupo:", layout=widgets.Layout(display='flex', flex_flow='column', align_items='stretch'))

# Botón para guardar la selección del segundo grupo
save_button2 = widgets.Button(description="Guardar selección")

# Contenedor combinado para el nombre del segundo grupo y el botón de guardar
group_name_and_save_container2 = widgets.VBox([group_name_input2, save_button2])

# Función para generar los desplegables del segundo grupo
def generate_dropdowns2(num_elements):
    dropdowns = []
    for i in range(num_elements):
        dropdown = widgets.Dropdown(options=economies, description=f'Elemento {i + 1}:')
        dropdowns.append(dropdown)
    dropdown_container2.children = dropdowns
    display(group_name_and_save_container2)

# Acción del botón para guardar la selección y mostrar el segundo grupo
def on_save_button_click(b):
    global group1, group1_name
    new_selection = [dropdown.value for dropdown in dropdown_container.children]
    
    # Verificar duplicados en la selección actual
    if len(set(new_selection)) != len(new_selection):
        message = HTML("<span style='color: red;'>¡Error! No puedes seleccionar la misma economía más de una vez.</span>")
        display(message)
        return
    
    group1 = new_selection
    group1_name = group_name_input.value
    message = HTML("<span style='color: green;'>¡Selección del Grupo 1 guardada con éxito!</span>")
    selected_items = HTML(f"<b>Elementos seleccionados del Grupo '{group1_name}':</b> {', '.join(group1)}")
    display(message, selected_items)
    
    # Preguntar al usuario cuántos elementos contendrá el grupo 2
    num_elements_label2 = widgets.Label("¿Cuántos elementos tendrá el grupo 2?")
    num_elements_input2 = widgets.BoundedIntText(min=1, max=len(economies), step=1, value=1)
    
    # Botón para generar los desplegables del segundo grupo
    generate_button2 = widgets.Button(description="Aceptar")
    
    # Acción del botón para generar los desplegables del segundo grupo
    def on_generate_button2_click(b):
        generate_dropdowns2(num_elements_input2.value)
    
    generate_button2.on_click(on_generate_button2_click)
    
    # Acción del botón para guardar la selección del segundo grupo
    def on_save_button2_click(b):
        global group2, group2_name
        new_selection = [dropdown.value for dropdown in dropdown_container2.children]
        
        # Verificar duplicados en la selección actual
        if len(set(new_selection)) != len(new_selection):
            message = HTML("<span style='color: red;'>¡Error! No puedes seleccionar la misma economía más de una vez.</span>")
            display(message)
            return
        
        group2 = new_selection
        group2_name = group_name_input2.value
        message = HTML("<span style='color: green;'>¡Selección del Grupo 2 guardada con éxito!</span>")
        selected_items = HTML(f"<b>Elementos seleccionados del Grupo '{group2_name}':</b> {', '.join(group2)}")
        display(message, selected_items)
        
        # Botón para realizar la comparación
        compare_button = widgets.Button(description="Realizar comparación")
        
        # Acción del botón para realizar la comparación
        def on_compare_button_click(b):
            # Calcular promedios para cada grupo
            avg_group1 = df[group1].mean(axis=1)
            avg_group2 = df[group2].mean(axis=1)

            # Crear el DataFrame de comparación y redondear a 2 decimales
            df_comparison = pd.DataFrame({
                f'Score {group1_name}': avg_group1,
                f'Score {group2_name}': avg_group2,
                'Difference Score %': round(abs((abs(avg_group1 - avg_group2) / ((avg_group1 + avg_group2) / 2)) * 100), 2)
            })

            # Guardar el DataFrame como archivo Excel
            df_comparison.to_excel(f'TTDI_{group1_name}_{group2_name}.xlsx', float_format="%.2f", index_label='Indicator')

            # Mostrar mensaje de confirmación
            print(f"Se ha generado el archivo Excel con la tabla comparativa entre '{group1_name}' y '{group2_name}'.\n"
                  f"Para descargarlo, revise la sección 'Archivos' a la izquierda de la pantalla haciendo clic en el icono "
                  f"en forma de folder.\nDespués, de clic en los tres puntos en el archivo y luego en 'Descargar'.")

            # Plotear el gráfico de radar
            plot_radar_chart(df_comparison, group1_name, group2_name)

        compare_button.on_click(on_compare_button_click)

        # Mostrar el botón de comparación
        display(compare_button)

    save_button2.on_click(on_save_button2_click)

    # Mostrar widgets para el segundo grupo
    display(num_elements_label2, num_elements_input2, generate_button2, dropdown_container2)

save_button.on_click(on_save_button_click)

# Función para plotear el gráfico de radar
def plot_radar_chart(data, group1_name, group2_name):
    keywords = [
        "Business Environment",
        "Prioritization of Travel and Tourism",
        "International Openness",
        "Price Competitiveness",
        "Safety and Security",
        "Health and Hygiene",
        "Human Resources and Labour Market",
        "ICT Readiness",
        "Air Transport Infrastructure",
        "Ground and Port Infrastructure",
        "Tourist Service Infrastructure",
        "Natural Resources",
        "Cultural Resources",
        "Non-Leisure Resources",
        "Environmental Sustainability",
        "Socioeconomic Resilience and Conditions",
        "Demand Pressure and Impact"
    ]
    
    # Filtrar las columnas por los índices que contienen al menos una parte de los strings en 'keywords'
    filtered_labels = data.index[data.index.str.contains('|'.join(keywords),case=False)]

    num_vars = len(filtered_labels)

    # Obtener las etiquetas de los índices sin modificar
    original_labels = data.loc[filtered_labels].index.tolist()
    original_labels = [label.split(', ')[0] for label in original_labels]

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, data.loc[filtered_labels, f'Score {group1_name}'], alpha=0.1, color='blue')
    ax.fill(angles, data.loc[filtered_labels, f'Score {group2_name}'], alpha=0.1, color='red')

    # Trazar líneas de los datos
    ax.plot(angles, data.loc[filtered_labels, f'Score {group1_name}'], color='blue', linewidth=2, linestyle='solid')
    ax.plot(angles, data.loc[filtered_labels, f'Score {group2_name}'], color='red', linewidth=2, linestyle='solid')

    ax.set_ylim(0, 7)  # Ajustar el rango del eje radial según tus datos específicos

    ax.set_thetagrids(np.degrees(angles), original_labels)
    ax.set_title(f'Comparación de los pilares del Travel & Tourism Development Index entre {group1_name} y {group2_name}', y=1.08)  # Ajustar 'y' para espacio entre título y gráfico

    ax.legend([group1_name, group2_name], loc='upper right', bbox_to_anchor=(1.3, 1))

    plt.show()



# Mostrar widgets con nombres por defecto
group_name_input.value = group1_name
group_name_input2.value = group2_name
display(num_elements_label, num_elements_input, generate_button, dropdown_container)
