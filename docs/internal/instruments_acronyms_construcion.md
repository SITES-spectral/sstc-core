### SITES Spectral Acronym Construction Guide Version 2024.0.1 (alpha)

1. **Fixed Multispectral Sensors (FMS)**
   - **Mast**:
     - Format: `FMS-M<height>`
     - Example: `FMS-M4` for a Fixed Multispectral Sensor on a 4-meter Mast.
     - Typical Heights: 4 meters, 10 meters, 15 meters, 25 meters, 50 meters.
   - **Building Top**:
     - Format: `FMS-BT<building_number>`
     - Example: `FMS-BT1` for a Fixed Multispectral Sensor on Building Top 1.

2. **Mast (M)**
   - **PhenoCam**:
     - Format: `P-M<height>`
     - Example: `P-M4` for a PhenoCam on a 4-meter Mast.
     - Typical Heights: 4 meters, 10 meters, 15 meters, 25 meters, 50 meters.
   - **Fixed Multispectral Sensors**:
     - Format: `FMS-M<height>`
     - Example: `FMS-M4` for a Fixed Multispectral Sensor on a 4-meter Mast.

3. **UAV (UAV)**
   - **General UAV Flight Height**:
     - Format: `UAV<height>-<optional uav index>`
     - Example: `UAV30-1` for UAV flying at 30 meters, UAV 1.
     - Typical Heights: 30 meters, 50 meters, 100 meters, etc.
   - **UAV M3M (with UAV model) Flight Height**:
     - Format: `<UAV model>-UAV<height>-<optional index>`
     - Example: `M3M-UAV30-1` for DJI Mavic 3 Multispectral UAV flying at 30 meters, UAV 1.
     - Example: `P4M-UAV30-1` for DJI Phantom 4 Multispectral UAV flying at 30 meters, UAV 1.

4. **PhenoCam (P)**
   - **Mast**:
     - Format: `P-M<height>-<required index if more than 1>`
     - Example: `P-M4-1` for a PhenoCam on a 4-meter Mast device 1.
     - Typical Heights: 4 meters, 10 meters, 15 meters, 25 meters, 50 meters.
   - **Building Top (BT)**:
     - Format: `P-BT<building_number>-<required index if more than 1>`
     - Example: `P-BT1-1` for a PhenoCam on Building Top 1 device 1.


6. **Satellite (SAT)**
   - **Sentinel-2 MSI**:
     - Format: `SAT-S2MSI`
     - Example: `SAT-S2MSI` for Sentinel-2 MSI.
   - **Sentinel-3 OLCI**:
     - Format: `SAT-S3OLCI`
     - Example: `SAT-S3OLCI` for Sentinel-3 OLCI.
   - **Landsat 8**:
     - Format: `SAT-LS8`
     - Example: `SAT-LS8` for Landsat 8.

### Examples

1. **Fixed Multispectral Sensor on a 10-meter Mast**:
   - Acronym: `FMS-M10`

2. **PhenoCam on Building Top 2**:
   - Acronym: `P-BT2`

3. **UAV 3 flying at 50 meters**:
   - Acronym: `UAV50-3`

4. **M3M UAV 2 flying at 100 meters**:
   - Acronym: `M3M-UAV100-2`

5. **P4M UAV 4 flying at 30 meters**:
   - Acronym: `P4M-UAV30-4`

6. **PhenoCam 2  on a 15-meter Mast**:
   - Acronym: `P-M15-2`

7. **Fixed Multispectral Sensor 2 on Building Top 1**:
   - Acronym: `FMS-BT1-2`

8. **Sentinel-2 MSI 1**:
   - Acronym: `SAT-S2MSI`

9. **Sentinel-3 OLCI 2**:
   - Acronym: `SAT-S3OLCI-2`

10. **Landsat 8 1**:
    - Acronym: `SAT-LS8-1`

---

## Best Practice for platform metadata.
'PhenoCams':{   
        'P-BH-FOR-01':{
            'description': 'Building H Top at ANS. Lars Eklundh custom optical camera.', 
            'legacy_acronym':"ANS-FOR-P01", 
            'status': 'active',
            'platform_key': 'P-BH-FOR-01',
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