# [Link to App](https://b2p-matrix-app.streamlit.app/)

# A Tool for Bridge Structure Type Selection in a Global South Context
![Welcome_page](https://github.com/bridgestoprosperity/matrix-streamlit/blob/main/Matrix_tool_welcome_page.png)
## Introduction
This repository contains the code for the prototype of the Bridges to Prosperity Infrastructure Matrix Tool prototype. This was a tool developed by [Mwendwa Kiko](www.linkedin.com/in/mwendwa-kiko), an [Engineering for Change (E4C)](https://www.engineeringforchange.org/) [impact fellow](https://www.engineeringforchange.org/fellowship/) who was working on this tool during the summer of 2023. 

The primary goal of this project was to analyze different types of river crossing structures that are suitable for a rural transportation context (e.g. cable suspended bridges, stone arch bridges, culvert) across a range of criteria (e.g. life cycle cost, span, climate resilience). The outcome of this project includes the development of the prototype of a matrix tool that can be used by infrastructure planners to decide on the most appropriate type of river crossing structure given a range of inputs.

The resulting matrix tool was built with the Python library streamlit, and provides a means for doing rapid assessments of potential crossing structure options for a given bridge site, once a minimum amount of information is available. 

## File Structure and Code Overview
The layout of files in this repository is as shown below: 

![File_structure](https://github.com/bridgestoprosperity/matrix-streamlit/blob/main/File_Structure.JPG). 

The information synthesis tab is built and rendered in 1_Information_Synthesis.py, and makes heavy use of Utils/utils.py. 2_Evaluation.py builds the material quantities table using Utils/material_quantities.py and then converts these to costs using Utils/default_costs.py. This is then used to construct the dynamic design flowchart. 

The figure below summarizes the flow of events in the evaluation tab: 
![Evaluation_tab_display_logic](https://github.com/bridgestoprosperity/matrix-streamlit/blob/main/Evaluation%20Tab2.drawio.png)

## Data Sources
A full explanation of the data sources used in this work can be found in the fellowship report on the E4C website. 
In summary, the sources of data used were of two kinds: previous similar studies and structural engineering design guides. 
The following are the previous similar studies used in constructing this tool: 
| Report Authors | Report title | Publishing Organisation | Target Region | Bridge Types Covered | 
| --- | --- | --- | --- | --- |
| P. Larcher, R. Petts, R. Spence | [Small Structures for Rural Roads: A Practical Planning, Design, Construction and Maintenance Guide](https://www.gtkp.com/knowledge/small-structures-for-rural-roads-guideline/) | Global Transport Knowledge partnership (gTKP) | Global South | Low-water crossing structures, pipe culverts, arch bridge, small bridges |
| Kasese District Local Government, and others | [Stone Arch Bridges: A strong & cost effective technology for rural roads](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj117nO_NeBAxWWm4kEHXKdAhwQFnoECBAQAQ&url=https%3A%2F%2Fwww.ctc-n.org%2Fsites%2Fwww.ctc-n.org%2Ffiles%2Fresources%2F531dafe7-b26c-4eda-844f-55c50a000075.pdf&usg=AOvVaw0B1IeZpAjqAQgKzoUuiJWI&opi=89978449) | Belgian Technical Cooperation (BTC) | Uganda | Masonry Arch Bridges | 
| Government of Nepal, Ministry of Urban Development and Helvetas | [Long Span Trail Bridge Standard: Technical Manual, Volume A: Design](https://skat.ch/wp-content/uploads/2021/07/Long-Span-Trail-Bridge-Standarad-Technical-Handbook.pdf) | Government of Nepal, Ministry of Urban Development and Helvetas  | Nepal | Suspended Cable Bridge |
| IT Transport  | [Footbridges: A Manual for Construction at Community and District Level](file:///C:/Users/mwendwa.kiko/Downloads/20100308-111426-8782-ITT+Footbridge+Supplement+A.pdf) | UK Department for International Development (DFID) | Global South | Bamboo Bridges, Timber Log Footbridges, Sawn Timber Footbridges, Steel Footbridges, Reinforced Concrete (RC) Footbridges |

In addition, as previously stated, structural engineering design guides from Australia, Canada, the United States and elsewhere were consulted in the course of the work. The table below gives some of the key guides consulted: 
| Authors | Title | Year | Country |
| --- | --- | --- | --- |
| Queensland Government Department of Transport and Main Roads | [Road Drainage Chapter 9: Culvert Design](https://www.tmr.qld.gov.au/_/media/busind/techstdpubs/hydraulics-and-drainage/road-drainage-manual/chapter9.pdf?sc_lang=enandhash=AA6B9000678F92BC28393CEF043F02CF) | 2019 | Australia |
| Ontario Ministry of Transportation | [Concrete Culvert Design and Detailing Manual](http://www.bv.transports.gouv.qc.ca/mono/1165314.pdf) | 2003 | Canada |
| Wisconsin Department of Transport | [Bridge Manual Chapter 36: Box Culverts](https://wisconsindot.gov/dtsdManuals/strct/manuals/bridge/ch36.pdf) | 2022 | United States |
| Florida Department of Transport | [Chapter 33: Reinforced Concrete Box and Three-sided Cuverts](https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/content2/roadway/ppmmanual/2017/volume1/chap33.pdf?sfvrsn=8bbdab3d_0) | 2017 | United States |
| Iowa Department of Transport | [Low Water Stream Crossings: Design and Construction Recommendations.](https://iowadot.gov/research/reports/Year/2003andolder/fullreports/tr453.pdf) | 2001 | United States |

## Running the app
Clone the repository, download the code, install the requirements in requirements.txt as explained [here](https://note.nkmk.me/en/python-pip-install-requirements/). Then run streamlit app as explained [on the streamlit website](https://docs.streamlit.io/knowledge-base/using-streamlit/how-do-i-run-my-streamlit-script). 

![Evaluation_page](https://github.com/bridgestoprosperity/matrix-streamlit/blob/main/Matrix_tool_evaluation_page_2.png)

