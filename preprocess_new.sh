#!/bin/bash -
#title          :preprocess_new.sh
#description    :Generate new figures from uploads
#author         :CEMAC - Helen
#date           :2022 Jan
#version        :1
#usage          :./preprocess_new.sh
#notes          :
#bash_version   :4.2.46(2)-release
#============================================================================
############################################################################
#   Check uploads for new tif and run preprocessing                        #
#                                                                          #
############################################################################
# activate python env
eval "$(/var/www/miniconda3/bin/conda shell.bash hook)"
conda activate agro-python
# create str arrays to loop through
declare -a index_list=("IIS3" "RZSM" "VHI" "spi")
declare -a spi_n=("01" "03" "06" "12")
# set file paths
data_folder="/var/www/AgroClimatic-Monitor/uolstorage/Data/"
upload_folder="${data_folder}upload/"

# check if new files
no_files=$(ls -d ${upload_folder}/*/ | wc -l)

if [[ ! ${no_files} = 0  ]];
	then


  echo 'moving tif to data folder'
  # for each index mv from upload to data index folder
  for index in ${index_list[@]};
  do
    # if its SPI then mv to corresponding SPI folder
    if [[ ${index} = "spi" ]];
  	   then
       for i in ${spi_n[@]};
       do
        echo "moving ${upload_folder}*/spi${i}*.tif* to ${data_folder}/spi${i}/"
        #mv ${upload_folder}*/spi${i}*.tif*  ${data_folder}/spi${i}/
       done
    else
      #echo "moving ${upload_folder}*/${index}*.tif* to ${data_folder}/${index}/"
      mv ${upload_folder}*/${index}*.tif* ${data_folder}/${index}/
    fi
  done
  #python NewData.py
fi
