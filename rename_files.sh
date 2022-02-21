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
#   RENAME                                                                 #
#                                                                          #
############################################################################


# create str arrays to loop through
declare -a index_list=("IIS3" "RZSM" "VHI" "spi")
declare -a spi_n=("01" "03" "06" "12")
# set file paths
data_folder="/var/www/AgroClimatic-Monitor/uolstorage/Data/"
# Format required
# - <index_name>_YYYY_MM.tif
# (where <index_name> can take: IIS3, RZSM, SPI01, SPI03, SPI06 and SPI12)
# old formats
# IIS3_MM_YYYY.tif
# RZSM_YYYY_MM.tiff
# VHI_MM_YYYY.tiff
# spi_01_YYYYMM.tif
echo 'renaming tifs'
# for each index mv from upload to data index folder
for index in ${index_list[@]};
do
  # if its SPI then mv to corresponding SPI folder
  if [[ ${index} = "spi" ]];
	   then
     for i in ${spi_n[@]};
     do
      for f in ${data_folder}spi${i}/*;
      do
      echo $f
      echo ${data_folder}spi${i}/${index}${i}_${f:59:4}_${f:63:2}.tif
      mv $f ${data_folder}spi${i}/${index}${i}_${f:59:4}_${f:63:2}.tif
     done
   done
  elif [[ ${index} = "RZSM" ]];
    then
      echo "renaming RZSM to tif not tiff"
      for f in ${data_folder}RZSM/*;
      do
        echo $f
        echo ${f:0:67}
        mv $f ${f:0:67}
      done
  elif [[ ${index} = "IIS3" ]];
    then
      for f in ${data_folder}IIS3/*;
      do
        echo $f
        echo ${data_folder}IIS3/IIS3_${f:59:4}_${f:56:2}.tif
        mv $f ${data_folder}IIS3/IIS3_${f:59:4}_${f:56:2}.tif
      done
  elif [[ ${index} = "VHI" ]];
    then
      for f in ${data_folder}VHI/*;
      do
        echo $f
        echo ${data_folder}VHI/VHI_${f:57:4}_${f:54:2}.tif
        mv $f ${data_folder}VHI/ls
        VHI_${f:57:4}_${f:54:2}.tif
      done
  fi
done
