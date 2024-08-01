# SHACL-based Schema Converter

## Project Objective
- Convert IFC-LD schema into Brick schema using SHACL approach
- Generate detailed Brick triples for interoperability between Building Informatino Modeling (BIM) and Building Management System (BMS)
- Develop an API prototype for Architecture, Engineering, Construction, and Operaiton (AECO) experts to adopt this approach in their industrial projects

## Installation libraries using Conda
1. Download the Conda installer for your OS setup. https://docs.conda.io/en/latest/miniconda.html
2. After installing Conda, create a virtual environment for the IFCLDtoBrick converter with:
```
conda create --name IFCLDtoBrick
```
3. Then activate the new virtual environment:
```
conda activate IFCLDtoBrick
```
4. Install RDFLib and PySHACL package:
```
pip install rdflib pyshacl
```


## Usage
- Install RDFLib and PySHACL library on your environment
- Download the Github repository and unzip the Zip file
- Run the 'IFCLDtoBrick_Converter.py' Python file, as follows:
```
python IFCLDtoBrick_Converter.py -i CIEE_IFC-LD_light.ttl -o CIEE_Brick.ttl -s IfcLDtoBrick_SHACL.ttl
```
```
optional arguments:
  -h, --help  show this help message and exit
  -i I        input IFC-LD file path
  -o O        output Brick file path
  -s S        SHACL file path
```

## References
- Devon Sparks, ‘IFC-LD Instance Builder’, available at https://github.com/devonsparks/ifcld-service
- Gabe Fierro, ‘IFC to Brick’, available at https://github.com/gtfierro/brick-ifc-convert/