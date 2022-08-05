#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd


# ### Cargar datos del excel a un dataFrame
# #### Uso convertes para no modificar la columna CUE Anexo y que me mantenga el 0 a la izquierda

# In[6]:


mae = pd.read_excel("mae.xlsx", header=[0, 1], converters={(' ', 'CUE Anexo'): lambda x: str(x)})


# ## Cantidad de establecimiento por sector

# In[7]:


mae[[(' ', 'Nombre'), (' ', 'Sector')]].groupby((" ", "Sector")).agg(cant_sectores=((' ', 'Nombre'), 'count'))


# In[8]:


mae.info()


# ### Establecimientos erroneos

# In[11]:


mae = mae.append({(' ', 'CUE Anexo'): '20444'}, ignore_index=True)
est_erroneos = mae[mae[(" ", "CUE Anexo")].astype(str).str.len() != 9]
est_erroneos


# ### Cargar datos de la tabla alumnos a un dataframe

# In[12]:


alumnos = pd.read_excel("alumnos_insc.xlsx", index_col = 0, converters={'cuenaexo': lambda x: str(x)})
alumnos.rename(columns = {'cuenaexo': 'CUE Anexo'}, inplace=True)
alumnos.head()


# ### Generar un nuevo dataframe con los establecimientos de la provincia del Chaco.

# In[14]:


est_chaco = mae[mae[(" ", "Jurisdicción")] == 'Chaco']
est_chaco


# ### Generar un nuevo dataframe con el resultado del cruce entre alumnos y establecimientos

# In[15]:


alum_est = pd.merge(alumnos, mae, left_on=["CUE Anexo"], right_on=[(" ", "CUE Anexo")])
alum_est


# ### Exportar a csv

# In[16]:


alum_est.to_csv('alum_est.csv')


# ### Generar un excel con todos aquellos alumnos cuyo resultado NO haya sido exitoso. 

# In[17]:


## Primero agrego una fila en alumnos donde el CUE Anexo no este en la tabla mae
alumnos.drop(alumnos.tail(4).index,inplace=True)
alumnos = alumnos.append({'CUE Anexo': '909000901', 'alumno': 'Juan CARRIZO'}, ignore_index=True)
alumnos


# In[26]:


alum_todos = pd.merge(alumnos, mae, left_on=["CUE Anexo"], right_on=[(" ", "CUE Anexo")], how="left")
alum_error = alum_todos[alum_todos[(" ", "CUE Anexo")].isna()][["alumno", "CUE Anexo"]]
alum_error


# #### Generar una nueva columna con el sexo del alumno pero de forma descriptiva:

# In[31]:


#Generar una nueva columna con el sexo del alumno pero de forma descriptiva:
# F (“Femenino”) M (“Masculino”)
# Para esto deberá utilizar una función lambda
#No hay una columna que especifique el sexo del alumno
alum_error.to_csv('alum_error.csv', index=False)

