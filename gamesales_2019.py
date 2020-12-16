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
datos.loc[datos['Total_Shipped'].isna(),'producido']=datos.loc[datos['Total_Shipped'].isna(),'Global_Sales']

# vemos que hay regiones que tienen datos faltantes, no sabemos si es por que toman valores muy bajos
#o porque realmente faltan. Para poder calcularlos vamos a utilizar la diferencia con el global.

indJ=datos['JP_Sales'].isna()
indN=datos['NA_Sales'].isna()
indP=datos['PAL_Sales'].isna()
indO=datos['Other_Sales'].isna()

#Este paso es posible que no sea necesario, pero de estas formas nos limpiamos las manos

#Añadir zona faltante JP
datos.loc[indJ,'JP_Sales']=datos.loc[indJ,'Global_Sales']-datos.loc[indJ,'NA_Sales']-datos.loc[indJ,'PAL_Sales']-datos.loc[indJ,'Other_Sales']
datos.loc[datos['JP_Sales']<0.01,'JP_Sales']=0
#Añadir zona faltante NA
datos.loc[indN,'NA_Sales']=datos.loc[indN,'Global_Sales']-datos.loc[indN,'JP_Sales']-datos.loc[indN,'PAL_Sales']-datos.loc[indN,'Other_Sales']
datos.loc[datos['NA_Sales']<0.01,'NA_Sales']=0
#Añadir zona faltante PAL
datos.loc[indP,'PAL_Sales']=datos.loc[indP,'Global_Sales']-datos.loc[indP,'NA_Sales']-datos.loc[indP,'JP_Sales']-datos.loc[indP,'Other_Sales']
datos.loc[datos['PAL_Sales']<0.01,'PAL_Sales']=0
#Añadir zona faltante Other
datos.loc[indO,'Other_Sales']=datos.loc[indO,'Global_Sales']-datos.loc[indO,'NA_Sales']-datos.loc[indO,'PAL_Sales']-datos.loc[indO,'JP_Sales']
datos.loc[datos['Other_Sales']<0.01,'Other_Sales']=0


#Añadir indicador multiplataforma
indD=datos['Name'].duplicated(keep=False)
datos['Multiplataforma']=0
datos.loc[indD,'Multiplataforma']=1

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


#Plataformas con mayor número de juegos vendidos en los ultimos años

datos_actuales=datos[(datos['Year']>2014) &(datos['producido'].isna()==False)]
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

#Rellenamos el esbr delos juegos sin rating con SC(sin categoria)
datos_actuales['ESRB_Rating'][datos_actuales['ESRB_Rating'].isna()]='SC'


#Agrupamos los juegos identicos en distinras plataformas y reajustamos el ranking

d = {'producido':'producido', 'Multiplataforma':'Multiplataforma'}
datos_platf=datos_actuales.groupby(['Name','Genre','Publisher','ESRB_Rating']).agg({'producido':'sum','Multiplataforma':'mean'}).rename(columns=d)
datos_platf=datos_platf.reset_index()
datos_platf=datos_platf.sort_values(by=['producido'], ascending=False)
datos_platf['Rank']=np.arange(datos_platf.shape[0])+1

#Comparativa
sns.displot(datos_platf, x="Rank", col="Multiplataforma", kind="kde", fill=True)
plt.savefig('3.png')
plt.show()


#Por cada plataforma
datos_actuales_plat=datos_actuales[(datos_actuales['Platform']=='PS4')| (datos_actuales['Platform']=='PC')| (datos_actuales['Platform']=='XOne')| (datos_actuales['Platform']=='NS')]
sns.displot(datos_actuales_plat, x="Rank", hue="Multiplataforma", kind="kde",col="Platform", fill=True)
plt.savefig('4.png')
plt.show()

### Analisis por género

datos_genre = datos_actuales.groupby(by=['Genre'])['producido'].sum()
datos_genre = datos_genre.reset_index()
datos_genre['count']=datos_platf['Genre'].value_counts().reset_index().sort_values(by=['index'])['Genre'].values
datos_genre = datos_genre.sort_values(by=['producido'], ascending=False)


plt.figure(figsize=(15, 10))
sns.barplot(x="Genre", y="producido", palette="Set2",data=datos_genre)
plt.xticks(rotation=80)
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


datos_shooter=datos_platf[datos_platf['Genre']=='Shooter']

#Como afecta la clasificacion ESBR a las ventas

#shooters
datos_shooter_ESRB=datos_shooter[datos_shooter['ESRB_Rating'].isna()==False]
datos_shooter_nESRB=datos_shooter[datos_shooter['ESRB_Rating'].isna()]
sns.displot(datos_shooter_ESRB, x="Rank", col='ESRB_Rating', kind="kde", fill=True)
plt.savefig('14.png')
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



#criterio de seleccion para tener la mayor probabilidad de ventas

#shooter
datos_shooter_final=datos_shooter_ESRB[((datos_shooter_ESRB['Publisher']=='Activision')|(datos_shooter_ESRB['Publisher']=='Electronic Arts'))&(datos_shooter_ESRB['ESRB_Rating']=='M')]

#valor medio shooter
print(datos_shooter_final['producido'].mean())

#esstimacion no parametrica de la funcion de densidad

sns.displot(datos_shooter_final, x="Rank", kind="kde", fill=True)
plt.savefig('18.png')
plt.show()

#Ventas

sns.displot(datos_shooter_final, x="producido", kind="kde", fill=True)
plt.savefig('19.png')
plt.show()