# variable name structure:  pagename_pagesection_sectionpart
# The source of this file is in https://docs.google.com/document/d/1Vg_mEmAr4P-WyQ2pOZzwse0f7IqpcxOKioHX5s_5R_w/edit?usp=sharing

about_tool_title = ''' About the tool '''

about_tool_textbox1 = ''' 

Agricultural drought indices are calculated from in situ-observed precipitation data, 
remote sensing, and satellite-derived soil moisture to indicate whether agricultural 
lands are subjected to drought stress over Brazil. Using more than one type of index 
provides more reliable indication of droughts. Therefore, three types of indices are 
presented in this tool, accordingly with the data source it was generated. An 
integrated index is also presented, which is a combination of all the three indices. 
More information of each index and how to interpret their results are given below:

 '''

about_tool_textbox2_title = ''' 1. Precipitation-based drought monitoring indices: '''

about_tool_textbox2_text = ''' 

- Standardized Precipitation Index (SPI)

The Standard Precipitation Index-SPI is a drought index proposed by Mckee et al 
(1993) to quantify the probability of a precipitation deficit occurrence at a specific 
monthly time scale (3, 6, 12-month, etc). The index is widely recommended for drought 
monitoring due to its simplicity and multiscale characteristic in quantifying the abnormal 
wetness and dryness conditions. Negative SPI values indicate less than median precipitation, 
and positive values indicate greater than median precipitation. As SPI is a normalized index, 
wetter and drier climates can be represented in the same way (McKee 1995). Weakness and strengths 
of the SPI indices are discussed by Keyantash (2018).

SPI is calculated from monthly accumulated rainfall provided by the Center for Weather Forecasting 
and Climate Studies/National Institute for Space Research (CPTEC/INPE). The dataset consists of 
measurements from approximately 1500 weather stations from different sources, such as the National 
Institute of Meteorology (INMET) and regional meteorological centers. As of 2010, the World Meteorological 
Organization (WMO) selected the SPI as a key meteorological drought indicator to be produced operationally 
by meteorological services (Svoboda et al. 2012).

 '''
 
about_tool_textbox3_title = ''' 2. Vegetation-based drought monitoring indices: '''

about_tool_textbox3_text  = ''' 

- Vegetation Health Index (VHI) 

VHI is a combination of vegetation condition index (termed VCI) and thermal condition
index (TCI). VCI is obtained by scaling the Normalized Difference Vegetation
Index (NDVI) values by their multi-year absolute minimum and maximum values. 
The VCI allows quantifying the impact of weather and climate on vegetation. 
The TCI algorithm is similar to the VCI one but relates to brightness temperature 
(TB) estimated from the thermal infrared band of AVHRR (channel 4). 
TCI provides an opportunity to identify subtle vegetation health changes due to thermal effects. 
The absolute minimum and maximum values are related to the weekly VCI–TCI time series 
from 1981 to 2020 and are normalized for each pixel. 

Therefore, the VHI index can be applied to monitor the drought dynamics of large vegetated, 
including agriculture (A. P. M. Cunha et al. 2015). VHI dataset is available in the National 
Environmental Satellite, Data and Information Service – NESDIS (http://www.star.nesdis.noaa.gov) 
of the National Oceanic and Atmospheric Administration (NOAA).

 '''
about_tool_textbox4_title = ''' 3. Soil moisture-based drought monitoring indices '''

about_tool_textbox4_text = ''' 

- Root Zone Soil Moisture (RZSM)

The soil moisture index is based on the Root Zone Soil Moisture (RZSM) from 
NASA’s Grace satellite. The raw data which is publicly available consists 
of weekly products with 25 km of resolution for South America. The data 
represents fractions of soil moisture within the first 1 meter of the soil 
layer, in relation to a long-term climatology. The product shown here is 
a post-processing consisting of averaging of the available products for 
the current month, and interpolation into a finer resolution (4 km), 
and average for each Brazilian municipality. Finally, the original values 
of soil moisture ranging from 0 to 100 (historic fraction) are converted 
according to classes of drought in Table 1.

 '''
 
about_tool_textbox5_title = ''' 4. Combined drought monitoring Indices '''

about_tool_textbox5_text = ''' 

- Integrated Drought Index (IDI)

The Integrated Drought Index (IDI) consists of combining the SPI with the VHI and RZSMI.
 Since precipitation is the primary cause of drought development, negative SPI anomalies 
do not always correspond to drought in reality. It takes no account of impact, that is, 
the response of vegetation to water stress. Therefore, VHI presents a general picture and 
perceptions of drought (A. P. M. A. Cunha et al. 2019). 

In this context, SPI, VHI, and RZSM were selected to jointly represent the precipitation 
deficit (drought trigger) and the surface response to water deficit, in addition to 
soil water status. These three indices are, therefore, complementary information for 
identifying agricultural lands affected by drought. The IDI is calculated based on 3 
and 6 months (IDI-3, IDI-6) of integrated values of VHI, and SPI-3 and SPI-6, and RZSM. 
The IDI maps present the drought conditions classified into drought 
categories as in Table 1.

 '''

about_tool_textbox6_title = ''' Indices Interpretation '''

about_tool_textbox6_text = ''' 
Table 1. Drought classification for SPI, VHI and RZSM, ISS3
 '''
#------------#
#--- Tab1 ---#
#------------#

about_tool_textbox7_title = ''' How to use it '''

about_tool_textbox7_text = ''' 
We integrate three indices (SPI, VHI and RZSM) in a single one IDI for diagnosing drought 
conditions in agriculture. As the magnitude of indices are different among each other, 
we provide a table with drought classification according to each value interval. 

Users can click in a municipality and download the current month and the past time 
series for those indices to visualize and understand the drought patterns of their 
given location. 

These indices and classifications are developed to capture the average pattern of 
drought in agriculture. Therefore, given the vast spectrum of crops and management 
strategies taking place at the same time across Brazil, users must keep in mind 
that these classifications may change according to the crop and management strategy 
taking place in the aimed condition. Nevertheless, we believe that users can also 
relate the indices values to the observed drought conditions in their sites, being 
able to generate a customized classification like in the Table 1 for their own needs 
and conditions.

 '''
 
about_tool_textbox8_title = ''' References '''

about_tool_textbox8_text = ''' 
Cunha, Ana Paula M. A., Marcelo Zeri, Karinne Deusdará Leal, Lidiane Costa, Luz Adriana Cuartas, José Antônio Marengo, Javier Tomasella, et al. 2019. “Extreme Drought Events over Brazil from 2011 to 2019.” Atmosphere 10 (11): 642.
Cunha, A. P. M., R. C. Alvalá, C. A. Nobre, and M. A. Carvalho. 2015. “Monitoring Vegetative Drought Dynamics in the Brazilian Semiarid Region.” Agricultural and Forest Meteorology 214-215 (December): 494–505.
Keyantash, Jncfarse, and Others. 2018. “The Climate Data Guide: Standardized Precipitation Index (SPI).” National Center for Atmospheric Research Staff (Eds) 8.
McKee, Thomas B. 1995. “Drought Monitoring with Multiple Time Scales.” In Proceedings of 9th Conference on Applied Climatology, Boston, 1995. https://ci.nii.ac.jp/naid/10028178079/.
McKee, Thomas B., Nolan J. Doesken, John Kleist, and Others. 1993. “The Relationship of Drought Frequency and Duration to Time Scales.” In Proceedings of the 8th Conference on Applied Climatology, 17:179–83. Boston.
Svoboda, M., M. Hayes, D. Wood, and Others. 2012. “Standardized Precipitation Index User Guide.” World Meteorological Organization Geneva, Switzerland 900.
 '''

