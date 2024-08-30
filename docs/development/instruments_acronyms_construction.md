### SITES Spectral Acronym Construction Guide Version 2024.0.1 (alpha)
Avoid the use of hyppens "-" as separator, better to use underscore or double underscore 

1. **Fixed Multispectral Sensors (FMS)**
   - **Mast**:
     - Format: `FMS_M<height>`
     - Example: `FMS_M4` for a Fixed Multispectral Sensor on a 4-meter Mast.
     - Typical Heights: 4 meters, 10 meters, 15 meters, 25 meters, 50 meters.
   - **Rooftop (RF) building name ()**:
     - Format: `FMS_RFB<building_number or initial>`
     - Example: `FMS_RFBH_1` for a Fixed Multispectral Sensor on Rooftop Building H sensor number 1.

2. **Mast (M)**
   - **PhenoCam**:
     - Format: `P_M<height>`
     - Example: `P_M4` for a PhenoCam on a 4-meter Mast.
     - Typical Heights: 4 meters, 10 meters, 15 meters, 25 meters, 50 meters.
   - **Rooftop Building**:
     - Format: `P_RFB<building_number or initial>`
     - Example: `P_RFBH_1` for a Fixed Multispectral Sensor on Rooftop Building H camera 1.

   - **Fixed Multispectral Sensors**:
     - Format: `FMS_M<height>`
     - Example: `FMS_M4` for a Fixed Multispectral Sensor on a 4-meter Mast.

3. **UAV (UAV)**
   - **General UAV Flight Height**:
     - Format: `UAV<height>_<optional uav index>`
     - Example: `UAV30_1` for UAV flying at 30 meters, UAV 1.
     - Typical Heights: 30 meters, 50 meters, 100 meters, etc.
   - **UAV M3M (with UAV model) Flight Height**:
     - Format: `<UAV model>_UAV<height>_<optional index>`
     - Example: `M3M_UAV30_1` for DJI Mavic 3 Multispectral UAV flying at 30 meters, UAV 1.
     - Example: `P4M_UAV30_1` for DJI Phantom 4 Multispectral UAV flying at 30 meters, UAV 1.

4. **PhenoCam (P)**
   - **Mast**:
     - Format: `P_M<height>_<required index if more than 1>`
     - Example: `P_M4_1` for a PhenoCam on a 4-meter Mast device 1.
     - Typical Heights: 4 meters, 10 meters, 15 meters, 25 meters, 50 meters.
   - **Rooftop Building (RFB)**:
     - Format: `P_RFB<building_number or letter>_<required index if more than 1>`
     - Example: `P_RFB1_1` for a PhenoCam on Rooftop Building 1 device 1.


6. **Satellite (SAT)**
   - **Sentinel-2 MSI**:
     - Format: `SAT_S2MSI`
     - Example: `SAT_S2MSI` for Sentinel-2 MSI.
   - **Sentinel-3 OLCI**:
     - Format: `SAT_S3OLCI`
     - Example: `SAT_S3OLCI` for Sentinel-3 OLCI.
   - **Landsat 8**:
     - Format: `SAT_LS8`
     - Example: `SAT_LS8` for Landsat 8.

### Examples

1. **Fixed Multispectral Sensor on a 10-meter Mast**:
   - Acronym: `FMS_M10`

2. **PhenoCam on Rooftop Building 2**:
   - Acronym: `P_RFB2`

3. **UAV 3 flying at 50 meters**:
   - Acronym: `UAV50_3`

4. **M3M UAV 2 flying at 100 meters**:
   - Acronym: `M3M_UAV100_2`

5. **P4M UAV 4 flying at 30 meters**:
   - Acronym: `P4M_UAV30_4`

6. **PhenoCam 2  on a 15-meter Mast**:
   - Acronym: `P_M15_2`

7. **Fixed Multispectral Sensor 2 on Rooftop Building 1**:
   - Acronym: `FMS_RFB1_2`

8. **Sentinel-2 MSI 1**:
   - Acronym: `SAT_S2MSI`

9. **Sentinel-3 OLCI 2**:
   - Acronym: `SAT_S3OLCI_2`

10. **Landsat 8 1**:
    - Acronym: `SAT_LS8_1`

---

## Best Practice for platform metadata.
'PhenoCams':{   
        'P_RFBH-1':{
            'description': 'Building H Top at ANS. Lars Eklundh custom optical camera.', 
            'legacy_acronym':"ANS-FOR-P01", 
            'status': 'active',
            'platform_key': 'P_RFBH_01',
            'ROI': 'Forest in Alpine Montain - Abiskojaure at Abisko National Park',
            'Viewing_Direction': 'West',
            
        }, 
    }, 

## Best practice for naming UAV files pre-processing

`SITES-<STATION acronym>-<LOC_Acronym>-<Ecosystem-Acronym>-AOI<number>-<TYPEofDrone (Mavic3Multispectral [M3M] or Phantom 4 Multispectral [P4M])>-UAV<FlyingHeight>`

Example:

```
'SITES-​SVB-​DEG-MIR-AOI3-M3M-UAV40':
        {
        "name": "Degero Mire North|South|West|East|Center|MeaninfulName ",
        "description": "UAV 2024-- Polygon 1out 2 in case it was splited",
        "ecosystems": ['MIR'],
        "is_active": True,        
        }, 

'SITES-DEG-MIR-AOI4-M3M-UAV40':
        {
        "name": "Degero Mire North|South|West|East|Center|MeaninfulName ",
        "description": "UAV 2024-- Polygon 2 out 2 in case it was splited",
        "ecosystems": ['MIR'],
        "is_active": True,        
        }, 
```