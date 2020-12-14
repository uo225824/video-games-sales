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

### Analisis por género

datos_genre = datos_actuales.groupby(by=['Genre'])['producido'].sum()
datos_actuales['Genre'].value_counts()
datos_genre = datos_genre.reset_index()
datos_genre['count']=datos_actuales['Genre'].value_counts().reset_index().sort_values(by=['index'])['Genre'].values
datos_genre = datos_genre.sort_values(by=['producido'], ascending=False)


plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", palette="Set2",data=datos_genre)
plt.xticks(rotation=90)
plt.savefig('5.png')
plt.show()


#Ventas medias por genero
datos_genre['producido']=datos_genre['producido']/datos_genre['count']
datos_genre = datos_genre.sort_values(by=['producido'], ascending=False)

plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", palette="Set2",data=datos_genre)
plt.xticks(rotation=90)
plt.savefig('6.png')
plt.show()

# Analisis por cada una de las cuatro consolas principales por genero

datos_ps4=datos_actuales[datos_actuales['Platform']=='PS4']
datos_pc=datos_actuales[datos_actuales['Platform']=='PC']
datos_xone=datos_actuales[datos_actuales['Platform']=='XOne']
datos_ns=datos_actuales[datos_actuales['Platform']=='NS']

#PS4
datos_genre_ps4 = datos_ps4.groupby(by=['Genre'])['producido'].sum()
datos_genre_ps4 = datos_genre_ps4.reset_index()
datos_genre_ps4 = datos_genre_ps4.sort_values(by=['producido'], ascending=False)
#PS4
datos_genre_pc = datos_pc.groupby(by=['Genre'])['producido'].sum()
datos_genre_pc = datos_genre_pc.reset_index()
datos_genre_pc = datos_genre_pc.sort_values(by=['producido'], ascending=False)
#PS4
datos_genre_xone = datos_xone.groupby(by=['Genre'])['producido'].sum()
datos_genre_xone = datos_genre_xone.reset_index()
datos_genre_xone = datos_genre_xone.sort_values(by=['producido'], ascending=False)
#PS4
datos_genre_ns = datos_ns.groupby(by=['Genre'])['producido'].sum()
datos_genre_ns = datos_genre_ns.reset_index()
datos_genre_ns = datos_genre_ns.sort_values(by=['producido'], ascending=False)


plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", data=datos_genre_ps4)
plt.xticks(rotation=90)
plt.savefig('7.png')
plt.show()

plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", data=datos_genre_pc)
plt.xticks(rotation=90)
plt.savefig('8.png')
plt.show()

plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", data=datos_genre_xone)
plt.xticks(rotation=90)
plt.savefig('9.png')
plt.show()

plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", data=datos_genre_ns)
plt.xticks(rotation=90)
plt.savefig('10.png')
plt.show()



### Analisis por mercado


datos_actuales_genre = datos_actuales[['Genre', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']]
# comp_genre
comp_map = datos_actuales_genre.groupby(by=['Genre']).sum()
comp_map=comp_map.sort_values(by=['NA_Sales'], ascending=False)
comp_table = comp_map.reset_index()
comp_table = pd.melt(comp_table, id_vars=['Genre'], value_vars=['NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales'], var_name='Sale_Area', value_name='Sale_Price')
a=comp_table.groupby(by=['Sale_Area']).sum().reset_index()
a=a.sort_values(by=['Sale_Price'], ascending=False)
plt.figure(figsize=(15, 10))
sns.barplot( y='Sale_Price', x='Sale_Area', data=a)
plt.xticks(rotation=70)
plt.savefig('11.png')
plt.show()


#analisis de mercado por genero (mapa de calor)

plt.figure(figsize=(15, 10))
sns.set(font_scale=1)
sns.heatmap(comp_map, annot=True, fmt = '.1f')

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig('12.png')
plt.show()

#analisis de mercado por genero (grafico barras)
plt.figure(figsize=(15, 10))
sns.barplot(x='Genre', y='Sale_Price', hue='Sale_Area', palette="Set2", data=comp_table)
plt.xticks(rotation=70)
plt.savefig('13.png')
plt.show()


### Analisis top ventas


datos_shooter=datos_actuales[datos_actuales['Genre']=='Shooter']
datos_sport=datos_actuales[datos_actuales['Genre']=='Sports']

#Como afecta la clasificacion ESBR a las ventas

#shooters
datos_shooter_ESRB=datos_shooter[datos_shooter['ESRB_Rating'].isna()==False]
datos_shooter_nESRB=datos_shooter[datos_shooter['ESRB_Rating'].isna()]
sns.displot(datos_shooter_ESRB, x="Rank", col='ESRB_Rating', kind="kde", fill=True)
plt.savefig('14.png')
plt.show()

#sport

datos_sport_ESRB=datos_sport[datos_sport['ESRB_Rating'].isna()==False]
datos_sport_nESRB=datos_sport[datos_sport['ESRB_Rating'].isna()]

sns.displot(datos_sport_ESRB, x="Rank", col='ESRB_Rating', kind="kde", fill=True)
plt.savefig('15.png')
plt.show()


#Las distribuidoras con más ventas

#shooter
datos_shooter_ESRB_pu = datos_shooter_ESRB.groupby(by=['Publisher'])['producido'].sum()
datos_shooter_ESRB_pu= datos_shooter_ESRB_pu.reset_index()
datos_shooter_ESRB_pu = datos_shooter_ESRB_pu.sort_values(by=['producido'], ascending=False)
plt.figure(figsize=(15, 10))
sns.barplot(x="Publisher", y="producido", data=datos_shooter_ESRB_pu.iloc[0:15,:],ci=None)
plt.xticks(rotation=90)
plt.savefig('16.png')
plt.show()

#sport
datos_sport_ESRB_pu = datos_sport_ESRB.groupby(by=['Publisher'])['producido'].sum()
datos_sport_ESRB_pu= datos_sport_ESRB_pu.reset_index()
datos_sport_ESRB_pu = datos_sport_ESRB_pu.sort_values(by=['producido'], ascending=False)
plt.figure(figsize=(15, 10))
sns.barplot(x="Publisher", y="producido", data=datos_sport_ESRB_pu.iloc[0:15,:],ci=None)
plt.xticks(rotation=90)
plt.savefig('17.png')
plt.show()


#criterio de seleccion para tener la mayor probabilidad de ventas

#shooter
datos_shooter_final=datos_shooter_ESRB[((datos_shooter_ESRB['Publisher']=='Activision')|(datos_shooter_ESRB['Publisher']=='Electronic Arts'))&(datos_shooter_ESRB['ESRB_Rating']=='M')]

#valor medio shooter
datos_shooter_final['producido'].mean()

#esstimacion no parametrica de la funcion de densidad

sns.displot(datos_shooter_final, x="Rank", kind="kde", fill=True)
plt.savefig('18.png')
plt.show()

#Sport

datos_sport_final=datos_sport_ESRB[(datos_sport_ESRB['Publisher']=='EA Sports')|(datos_sport_ESRB['Publisher']=='Electronic Arts')|(datos_sport_ESRB['Publisher']=='2K Sports')]

#media
datos_sport_final['producido'].mean()

sns.displot(datos_sport_final, x="Rank", kind="kde", fill=True)
plt.savefig('19.png')
plt.show()