# variable name structure:  pagename_pagesection_sectionpart
# The source of this file is in https://docs.google.com/document/d/1fGuYaJOWJixb99-qZEj_Urqk2wb4JnLupFYybIRu3pw/edit?usp=sharing

about_tool_title = ''' Sobre a ferramenta '''

about_tool_textbox1 = ''' 

Agricultural drought indices are calculated from in situ-observed precipitation data, 
remote sensing, and satellite-derived soil moisture to indicate whether agricultural 
lands are subjected to drought stress over Brazil. Using more than one type of index 
provides more reliable indication of droughts. Therefore, three types of indices are 
presented in this tool, accordingly with the data source it was generated. An 
integrated index is also presented, which is a combination of all the three indices. 
More information of each index and how to interpret their results are given below:

 '''

about_tool_textbox2_title = ''' 1. Precipitation-based drought monitoring indices '''

about_tool_textbox2_text = ''' 

### Índice de precipitação padronizado (SPI):  



O Standard Precipitation Index-SPI é um índice de seca proposto por Mckee et al (1993) para 
quantificar a probabilidade de ocorrência de déficit de precipitação em uma escala de tempo 
mensal específica (3, 6, 12 meses, etc.). O índice é amplamente recomendado para monitoramento 
de secas devido à sua simplicidade e característica multiescala na quantificação das condições 
anormais de umidade e seca. Os valores de SPI negativos indicam precipitação inferior à mediana 
e os valores positivos indicam precipitação superior à mediana. Como o SPI é um índice 
normalizado, climas mais úmidos e secos podem ser representados da mesma forma (McKee 1995). 
Os pontos positivos e negativos dos índices SPI são discutidos por Keyantash (2018).

O SPI desta ferramenta é calculado a partir da precipitação acumulada mensal fornecida pelo 
Centro de Previsão de Tempo e Estudos Climáticos / Instituto Nacional de Pesquisas Espaciais 
(CPTEC/INPE). O conjunto de dados consiste em medições de aproximadamente 1.500 estações 
meteorológicas de diferentes fontes, como o Instituto Nacional de Meteorologia (INMET) 
e centros meteorológicos regionais. Em 2010, a Organização Meteorológica Mundial (OMM) 
selecionou o SPI como um indicador chave de seca meteorológica a ser produzido 
operacionalmente por serviços meteorológicos (Svoboda et al. 2012).

 '''
 
about_tool_textbox3_title = ''' 2. Índices de monitoramento de seca com base na vegetação '''

about_tool_textbox3_text  = ''' 

### Índice de saúde vegetal (VHI):  



O VHI é uma combinação de índice de condição de vegetação (denominado VCI) e índice de 
condição térmica (TCI). O VCI é obtido escalando os valores do Índice de Vegetação por 
Diferença Normalizada (NDVI) por seus valores mínimos e máximos absolutos plurianuais. 
O VCI permite quantificar o impacto do tempo e do clima na vegetação. O algoritmo TCI é 
semelhante ao VCI, mas se refere à temperatura de brilho (TB) estimada a partir da banda 
infravermelha térmica do AVHRR (canal 4). A TCI oferece uma oportunidade para identificar 
mudanças sutis na saúde da vegetação devido aos efeitos térmicos. Os valores mínimos e 
máximos absolutos estão relacionados à série temporal VCI – TCI semanal de 1981 a 2020 e 
são normalizados para cada pixel.

Portanto, o índice VHI pode ser aplicado para monitorar a dinâmica da seca em grandes 
áreas com vegetação, incluindo a agricultura (Cunha et al. 2015). O conjunto de dados 
VHI está disponível no Serviço Nacional de Satélite, Dados e Informações Ambientais - 
NESDIS (http://www.star.nesdis.noaa.gov) da Administração Oceânica e Atmosférica 
Nacional (NOAA).

 '''
about_tool_textbox4_title = ''' 3. Índices de monitoramento de seca com base na umidade do solo '''

about_tool_textbox4_text = ''' 

### Umidade do solo da zona raiz (RZSM):  



O índice de umidade do solo é baseado na umidade do solo da zona raiz (RZSM) do satélite 
Grace da NASA. Os dados brutos, publicamente disponíveis, consistem em produtos semanais 
com 25 km de resolução para a América do Sul. Os dados representam frações de umidade 
do solo dentro do primeiro metro da camada de solo, em relação a uma climatologia de 
longo prazo. O produto mostrado aqui é um pós-processamento que consiste na média dos 
produtos disponíveis para o mês atual e na interpolação em uma resolução mais precisa 
(4 km) e média para cada município brasileiro. Por fim, os valores originais de umidade 
do solo variando de 0 a 100 (fração histórica) são convertidos de acordo com as classes 
de seca da Tabela 1.

 '''
 
about_tool_textbox5_title = ''' 4. Índices combinados de monitoramento de seca '''

about_tool_textbox5_text = ''' 

### Índice de Seca Integrado (IDI):  



O Índice de Seca Integrado (IDI) consiste na combinação do SPI com o VHI e o RZSMI. 
Uma vez que a precipitação é a principal causa do desenvolvimento da seca, as anomalias 
do SPI negativo nem sempre correspondem à seca na realidade. Logo, o SPI não leva em 
consideração o impacto, ou seja, a resposta da vegetação ao estresse hídrico. Portanto, 
o VHI apresenta um quadro geral da percepção de seca pela vegetação (Cunha et al. 2019).

Nesse contexto, nós selecionamos o SPI, VHI e RZSM para representar conjuntamente o 
déficit de precipitação (gatilho de seca) e a resposta da superfície ao déficit hídrico, 
além do estado hídrico do solo. Esses três índices são, portanto, informações 
complementares para a identificação de lavouras afetadas pela seca. O IDI é calculado 
com base em 3 e 6 meses (IDI-3, IDI-6) de valores integrados de VHI e SPI-3 e SPI-6 e RZSM. 
Os mapas de IDI apresentam as condições de seca classificadas em categorias de seca 
conforme a Tabela 1.

 '''

about_tool_textbox6_title = ''' Interpretação dos índices '''

about_tool_textbox6_text = ''' 
Tabela 1. Classificação de seca para SPI, VHI, RZSM e IDI  

 '''
#------------#
#--- Tab1 ---#
#------------#

about_tool_textbox7_title = ''' Como usar '''

about_tool_textbox7_text = ''' 
Integramos três índices (SPI, VHI e RZSM) em um único IDI para o diagnóstico de secas 
na agricultura. Como as magnitudes dos índices são diferentes entre si, 
disponibilizamos uma tabela (Tabela 1) com a classificação das secas de acordo com 
cada intervalo de valores.

Os usuários podem clicar em um município e baixar o mês atual e as séries temporais 
anteriores desses índices para visualizar e compreender os padrões de seca de sua localidade.

Vale ressaltar que esses índices e classificações são desenvolvidos para capturar 
o padrão médio de seca em lavouras agrícolas. Portanto, dado o vasto espectro de 
culturas e estratégias de manejo que ocorrem ao mesmo tempo em todo o Brasil, os 
usuários devem ter em mente que essas classificações podem mudar de acordo com a 
cultura e a estratégia de manejo que ocorrem na condição desejada. No entanto, 
acreditamos que os usuários também possam relacionar os valores dos índices às 
condições de seca observadas em seus locais, podendo gerar uma classificação 
customizada como na Tabela 1 de acordo com suas próprias necessidades e condições.

 '''
 
about_tool_textbox8_title = ''' Referências '''

about_tool_textbox8_text = ''' 
Cunha, Ana Paula M. A., Marcelo Zeri, Karinne Deusdará Leal, Lidiane Costa, Luz Adriana Cuartas, José Antônio Marengo, Javier Tomasella, et al. 2019. “Extreme Drought Events over Brazil from 2011 to 2019.” Atmosphere 10 (11): 642.
Cunha, A. P. M., R. C. Alvalá, C. A. Nobre, and M. A. Carvalho. 2015. “Monitoring Vegetative Drought Dynamics in the Brazilian Semiarid Region.” Agricultural and Forest Meteorology 214-215 (December): 494–505.
Keyantash, Jncfarse, and Others. 2018. “The Climate Data Guide: Standardized Precipitation Index (SPI).” National Center for Atmospheric Research Staff (Eds) 8.
McKee, Thomas B. 1995. “Drought Monitoring with Multiple Time Scales.” In Proceedings of 9th Conference on Applied Climatology, Boston, 1995. https://ci.nii.ac.jp/naid/10028178079/.
McKee, Thomas B., Nolan J. Doesken, John Kleist, and Others. 1993. “The Relationship of Drought Frequency and Duration to Time Scales.” In Proceedings of the 8th Conference on Applied Climatology, 17:179–83. Boston.
Svoboda, M., M. Hayes, D. Wood, and Others. 2012. “Standardized Precipitation Index User Guide.” World Meteorological Organization Geneva, Switzerland 900.
 '''

