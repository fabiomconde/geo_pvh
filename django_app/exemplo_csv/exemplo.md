# 📂 Exemplos de Arquivos CSV para Importação

Abaixo estão 8 conjuntos de dados de exemplo, cada um indicando o tipo de visualização mais indicada e o nome do arquivo CSV correspondente.

---

## 1. 📈 Evolução do Desmatamento

> **Ideal para:** Gráfico de Linhas ou Tabela

Mostra a evolução ao longo dos anos. Com duas colunas de dados, o gráfico de linhas criará duas linhas diferentes.

**Nome do arquivo:** `1_evolucao_desmatamento.csv`

```csv
Ano,Desmatamento (ha),Degradacao (ha)
2019,35000,12000
2020,41000,15500
2021,39500,18200
2022,45000,21000
2023,42000,19500
2024,38000,14000
2025,36500,11000
```

---

## 2. 🥧 Alertas DETER por Classe

> **Ideal para:** Gráfico de Pizza ou Rosca

Com apenas os rótulos e 1 coluna de valores, o gráfico de Pizza dividirá as fatias perfeitamente.

**Nome do arquivo:** `2_alertas_deter_classes.csv`

```csv
Classe de Alerta,Area Afetada (ha)
Desmatamento Solo Exposto,12500
Degradacao Florestal,8400
Corte Seletivo,4200
Cicatriz de Incendio,15600
Mineracao Ilegal,3100
```

---

## 3. 📊 Focos de Calor Mensais

> **Ideal para:** Gráfico de Barras

Compara os focos de calor capturados por dois satélites diferentes ao longo dos meses.

**Nome do arquivo:** `3_focos_calor_mensal.csv`

```csv
Mes,Satelite AQUA,Satelite TERRA
Jan,15,10
Fev,12,8
Mar,25,20
Abr,45,35
Mai,120,95
Jun,350,280
Jul,850,700
Ago,1450,1200
Set,2100,1850
Out,950,800
Nov,300,250
Dez,50,40
```

---

## 4. 🗄️ Municípios de Rondônia

> **Ideal para:** Tabela de Dados

Contém textos e números misturados, ideal para preencher a tabela de ponta a ponta na tela.

**Nome do arquivo:** `4_municipios_ro_dados.csv`

```csv
Municipio,Populacao Estimada,Area Total (km2),Bioma Predominante
Porto Velho,548952,34090,Amazonia
Ji-Parana,130009,6896,Amazonia
Ariquemes,109523,4426,Amazonia
Vilhena,102211,11518,Cerrado/Amazonia
Cacoal,86895,3792,Amazonia
Guajara-Mirim,39386,24855,Amazonia
```

---

## 5. 🍩 Tipos de Conflitos Registrados

> **Ideal para:** Gráfico de Rosca

Mostra a distribuição percentual/fatiada das fases dos conflitos territoriais.

**Nome do arquivo:** `5_conflitos_fases.csv`

```csv
Fase do Conflito,Quantidade de Casos
Latente (Tensao),15
Manifesto (Declarado),42
Violento (Com vitimas),18
Resolvido/Acordo,8
```

---

## 6. 📊 Setores Econômicos dos Atores

> **Ideal para:** Gráfico de Barras Horizontais ou Tabela

Lista os setores que mais figuram como atores nos casos do Observatório.

**Nome do arquivo:** `6_atores_setores.csv`

```csv
Setor Economico,Numero de Atores Envolvidos
Agronegocio,85
Mineracao/Garimpo,42
Madeireiro,64
Energia/Hidreletricas,15
Poder Publico,38
Comunidades Tradicionais,92
```

---

## 7. 📊 Pressão em Áreas Protegidas

> **Ideal para:** Gráfico de Barras

Duas colunas numéricas que, no gráfico de barras, criarão duas barras lado a lado por Área Protegida — permitindo comparar o total vs. o que está sob pressão.

**Nome do arquivo:** `7_areas_protegidas_pressao.csv`

```csv
Area Protegida,Area Total (ha),Area Desmatada (ha)
TI Karipuna,152000,18500
RESEX Jaci-Parana,191000,145000
FLONA Bom Futuro,280000,85000
PARNA Pacaas Novos,764000,12000
TI Uru-Eu-Wau-Wau,1867000,45000
```

---

## 8. 📉 Direitos Afetados

> **Ideal para:** Gráfico de Linhas ou Tabela

Fica ótimo como segundo gráfico na opção **"2 Gráficos Lado a Lado"**.

**Nome do arquivo:** `8_direitos_afetados.csv`

```csv
Direito Violado,Total de Denuncias
Direito a Terra e Territorio,145
Meio Ambiente Equilibrado,112
Direito a Vida e Seguranca,45
Consulta Previa (OIT 169),88
Acesso a Agua Potavel,67
```