#!pip install seaborn --upgrade
#trabajamos con seaborn 0.11

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#Cargamos los dos set de datos disponibles
datos=pd.read_csv('vgsales-12-4-2019.csv')
datos_short=pd.read_csv('vgsales-12-4-2019-short.csv')

#En principio ambos set de datos tienen la misma información
#con la diferencia de que datos es mas completo

#Convinamos las variables shipped y global sale para formar una nueva variable "producido

#Nueva variable
datos['producido']=datos['Total_Shipped']
datos['producido'][datos['Total_Shipped'].isna()]=datos['Global_Sales'][datos['Total_Shipped'].isna()]

#Rellenemos con ceros los datos faltantes. Estos valores se corresponden a ventas menores a los 0.01 millones
datos['producido'][datos['producido'].isna()]=0

# vemos que hay regiones que tienen datos faltantes, no sabemos si es por que toman valores muy bajos
#o porque realmente faltan. Para poder calcularlos vamos a utilizar la diferencia con el global.

indJ=datos['JP_Sales'].isna()
indN=datos['NA_Sales'].isna()
indP=datos['PAL_Sales'].isna()
indO=datos['Other_Sales'].isna()
datos['JP_Sales'][indJ]=0
datos['NA_Sales'][indN]=0
datos['PAL_Sales'][indP]=0
datos['Other_Sales'][indO]=0

#Este paso es posible que no sea necesario, pero de estas formas nos limpiamos las manos

#Añadir zona faltante JP
datos['JP_Sales'][indJ]=datos['Global_Sales'][indJ]-datos['NA_Sales'][indJ]-datos['PAL_Sales'][indJ]-datos['Other_Sales'][indJ]
datos['JP_Sales'][datos['JP_Sales']<0.01]=0
#Añadir zona faltante NA
datos['NA_Sales'][indN]=datos['Global_Sales'][indN]-datos['JP_Sales'][indN]-datos['PAL_Sales'][indN]-datos['Other_Sales'][indN]
datos['NA_Sales'][datos['NA_Sales']<0.01]=0
#Añadir zona faltante PAL
datos['PAL_Sales'][indP]=datos['Global_Sales'][indP]-datos['NA_Sales'][indP]-datos['JP_Sales'][indP]-datos['Other_Sales'][indP]
datos['PAL_Sales'][datos['PAL_Sales']<0.01]=0
#Añadir zona faltante Other
datos['Other_Sales'][indO]=datos['Global_Sales'][indO]-datos['NA_Sales'][indO]-datos['PAL_Sales'][indO]-datos['JP_Sales'][indO]
datos['Other_Sales'][datos['Other_Sales']<0.01]=0


#Añadir indicador multiplataforma
indD=datos['Name'].duplicated(keep=False)
datos['Multiplataforma']=0
datos['Multiplataforma'][indD]=1

### Plataformas con mayor número de juegos vendidos

b=datos.groupby(by=['Platform'])['producido'].sum().sort_values(ascending=False).to_frame()
b_others=b[18:].sum()
b.reset_index(inplace=True)
b['Platform'][18]='Others'
b['producido'][18]=b_others
plt.figure(figsize=(10, 8))
plt.pie(b['producido'][:19], labels=b['Platform'][:19], autopct='%1.1f%%', shadow=True, startangle=90)
plt.savefig('1.png')
plt.show()


# Plataformas con mayor número de juegos vendidos en los ultimos años

datos_actuales=datos[datos['Year']>2014]
b=datos_actuales.groupby(by=['Platform'])['producido'].sum().sort_values(ascending=False).to_frame()
b_others=b[7:].sum()
b.reset_index(inplace=True)
b['Platform'][7]='Others'
b['producido'][7]=b_others
plt.figure(figsize=(10, 8))
plt.pie(b['producido'][:8], labels=b['Platform'][:8], autopct='%1.1f%%', shadow=True, startangle=90)
plt.savefig('2.png')
plt.show()


#Comparativa de juegos plataforma vs multiplataforma

sns.displot(datos_actuales, x="Rank", col="Multiplataforma", kind="kde", fill=True)
plt.savefig('3.png')
plt.show()


#Por cada plataforma
datos_actuales_plat=datos_actuales[(datos_actuales['Platform']=='PS4')| (datos_actuales['Platform']=='PC')| (datos_actuales['Platform']=='XOne')| (datos_actuales['Platform']=='NS')]
sns.displot(datos_actuales_plat, x="Rank", hue="Multiplataforma", kind="kde",col="Platform", fill=True)
plt.savefig('4.png')
plt.show()

