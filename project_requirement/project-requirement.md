# ENGR 301: Project Requirements Document

The aim of this document is to specify the requirements of the system your group is to build. The focus of a requirements document is the problem you are attempting to solve:  not a first attempt at a solution to that problem. This document should communicate clearly to the supervisor, client and course coordinator what the system you build is going to do, and what constraints it must meet while doing so.

The document should also demonstrate your understanding of the main analysis principles and quality guidelines, and applicable standards, using tools and notations as necessary to communicate the requirements precisely, unambiguously and clearly in a written technical document. Page specifications below are *limits not targets* and refer to the pages in the PDF generated from the markdown. Because the size of your document is necessarily limited, you should ensure that you focus your efforts on those requirements that are most important to completing a successful system: if sections are at their page limit, indicate how many items would be expected in a complete specification. 

The ENGR 301 project proposal and requirements document should be based on the standard ISO/IEC/IEEE 29148:2011(E), primarily sections 8.4 and 9.5, plus section 9.4 for projects involving hardware and ISO 25010 SQuaRE for systemic requirements. While excerpts from the standard have been quoted within the template, to understand what is required it will be necessary to read earlier sections of the standards themselves. A supplementary treatment of requirements gathering in engineering projects may be found in [Requirements in Engineering Projects](https://victoria.rl.talis.com/items/F166DA94-DAD8-FBDB-0785-7A63C9BA3603.html?referrer=%2Flists%2F5886F297-2506-1F17-45D9-7F04CEE284EE.html%23item-F166DA94-DAD8-FBDB-0785-7A63C9BA3603) (Talis). The requirements document should contain the sections listed below, and conform to the formatting rules listed at the end of this brief. 

All team members are expected to contribute equally to the document and list their contributions in section 6 of the document. You should work on your document in your team's GitLab repository. While collective contributions are expected to be the exception rather than the rule, if more than one team member has contributed to a particular commit then all those team member IDs should be included in the first line of the git commit message. `git blame`, `git diff`, file histories, etc. will be tools used to assess individual contributions, so everyone is encouraged to contribute individually, commit early and commit often. Any team wishing to separate individually contributed sections into a single file before collation into the single proposal document for submission is welcome to do so.

Access to the standard can be found [here](https://ieeexplore-ieee-org.helicon.vuw.ac.nz/stamp/stamp.jsp?tp=&arnumber=6146379). Jump to page 62.

---

<div style="page-break-after: always;"></div>

# ENGR 301 Project *NN* Project Proposal and Requirements Document
Caitlin Goodger, Luisa Kristen, Zac Durant, Zak Kiernander, Nicole Stallinger and Matthew Butterfield. 

## 1. Introduction

Amateur rockets are flown regularly worldwide. These rockets are typically flown with off the shelf rocket motors with widely available propellant reloads. These rockets often exceed the speed of sound, altitudes above 30 km are not unheard of. These rockets are almost never controlled, they are stable due to passive aerodynamic features. 

While passively stable rockets are reasonably simple and reliable if well designed, they are susceptible to a variety of disturbances, particularly early in flight. Unexpected winds can cause the rocket to weathercock; flexibility in the launch tower/rail can cause railwhip, imparting a random launch angle to the rocket; the thrust from the rocket motor is also never perfectly symmetrical.

Amateur rockets are often designed in OpenRocket. OpenRocket gives the ability to simulate rockets while altering some parameter variables as a suggestion for the rocket’s performance. After a rocket has been built, it can be measured accurately to give a more accurate simulation to allow for smaller, finalising adjustments including moving the centre of mass. Automation can allow follow this process to be sped up and determine to a higher confidence of the safety of the flight.

The rocket uses a PID (Proportional Integral Derivative) controller to keep it fixed on an axis. Normally, parameters of PID are difficult to obtain due to the short period of time that the rocket motors are burning. Simulation can allow for estimate parameters for the PID controller.


### Client

Andre Geldenhuis is the client for this project. He has experience with rockets and experience working with similar projects. He can be reached in the Customer Channel on Mattermost. He also has occasionally Q&A sessions during ENGR301 Lectures and can be reached during those times with questions. He can also be reached at andre.geldenhuis@vuw.ac.nz. 

### 1.1 Purpose

The purpose of the system to provide a rocket simulation that can help determine, given certain conditions, the rocket's path and where it will likely land. By having a range of conditions, the system will show a range of paths and possible landing points.

### 1.2 Scope

This product is a Rocket Simulation program. The program shall provide an automation of simulation program OpenRocket to give a prediction of the flight performance of a rocket. The program shall provide likely landing locations based on varying parameters such as launch angle and parachute ejection time, through a form of Monte Carlo simulation to determine whether the flight is safe. The program shall provide estimate PID control parameters through the simulation.

### 1.3 Product overview 

The following subsections describe the product perspective, functions, characteristics and liimitations.

#### 1.3.1 Product perspective

The project is extending existing software. OpenRocket is an existing opensource project that allows users to design and simulate rocket models before creating the building them. This project is extending the simulation capabilities to allow for multiple simulations to be run at once. OpenRocket only allows for one simulation, with one set of conditions and parameters, so this project is extending this functionality to have multiple simulations and multiple conditions and parameters. Since this project is extending existing software it needs to be able to interact with OpenRocket and have similar looking interfaces for ease of use. The user will need to create the model for their rocket in OpenRocket. The project will then use that rocket to run the simulation. This means that it needs to be able to export the data from OpenRocket and be able to use it in the simulation. 

The user interface should be simple and clear. As the user is likely coming from or has experience with using OpenRocket, they will want this projec to function in similar ways. Due to the fact that it is an extension of OpenRocket, this is important because it is building on their base. The user interfaces for this porject don't need to be extremely complicated because most of the interfaces that the project is added are for the user to select parameters and then get the output of the simulation. For the minimal product, this output could be written to a file. This would be easy for the user to understand as long as it is laid out in a sensible fashion. For an extension, a graphical interface could be added so that the output of the simulation is clear for the user to understand. 

This project is also part of a large project. There is another project focused on building a rocket and another project focused on Mission Control. This project will be the go-between of the hardware and the software components. This means that the project needs to be interact with the other two projects and communicate with them. The project building a rocket needs to be able to use the simulation to know how the rocket they have designed will travel and where it could land. The Mission Control project also needs to use the simulation for functionality such as knowing if the current weather conditions are safe to launch in. Mission Control will be using this project while at the rocket launch site which will likely not have an internet connection. This means that the project needs to be able to function without requiring an internet connection as well. 

#### 1.3.2 Product functions

To meet the requirements of the minimum viable product the project will;

- Be able to import a rocket file designed in OpenRocket.

The program must be able to correctly load and work with OpenRocket .ork files defining the features of different rockets. This allows the customer to create simulations for a wide variety of different rocket configurations and enables the use of the already familar OpenRocket design system.

- Take a given latitude and longitude point for launch.

The program will need to correctly maintain and use a coordinate system to provide meaningful data from the simulation. This data could come in the form of simple projected latitude and longitude, distance-bearing predictions or scatter plots of posible landing zones.

- Run multiple simulations with the given rocket and co-ordinates and produce possible landing points.

The program must be able to create meaningful statistical variations to produce varying flights in the simulations. This is crucial to show the use a variety of possible landing sites should the environment chamge, minimising the chance of a dangerous launch.

- Output results to both the screen and to a file.

The program should output the results to the screen for quick viewing at mission control, allowing the user to quickly determine if the launch is safe. Outputting the results to a file would add functionality, allowing the user to use the tool as a method of evaluating rocket designs in various conditions.

#### 1.3.3 User characteristics   

1. Rocket Hobbyist

The main class of users is the rocket hobbyist engaged in designing and flying their own rockets. The program is designed specifically for these users to simulate their rockets and predict landing zones and the severity of environmental variations.
Several characteristics are assumed about the user;

- Familarity of rocket components and design

We assume some knowledge of rocket components and design. This is necessary as the data will be presented in a manner that might not be entirely accessable to a user with no rocket hardware knowledge.

- Experience with OpenRocket

We rely on the user having experience with OpenRocket, especially the process of designed and exporting custom rockets.

- Technologically literate

We expect some level of familarity with computer systems and using applications. Design of user interface will assume the user is comfortable with navigating typical interfaces.

- Understanding of coordinate system

Some understanding of latitude and longitude coordinates will be required to make full use of the program output. In the initial program the presentation of the data may require some evaluation by the user to determine if the launch is safe. Extensions to the program would reduce the importance of this assumption.

#### 1.3.4 Limitations

- PID Control

Inclusion of PID control will be limited in the intial development of the program by the lack of native support in OpenRocket's python scripting implementation. This functionality may be developed at a later date. 

-  Safety Considerations

The results of the simulations will be need to be given safety margins, reducing the possible precision. Variation of parameters such as wind will need to be slighty overestimated to ensure the program gives a worst case prediction.

-  Internet access

Under the assumption that the system must perform without access to the internet some functions might be impeded, particularly proposed extensions to the program such as google maps overlay and current weather data integration.

- Physical conditions

Some limitation will need to be placed on the range of environments the program is suitable to simulate. Outside of certain reasonable parameters the environment will likely be too extreme and unpredictable to remain reliable. Examples include extreme wind, rain or unreliable rocket designs.

- Reliability

Below the minimum required number of simulations the program output will not be reliable and should not be used to accurately predict the safety of a launch. In this configuration the program should warn the user and may not output all the usual predictions.

## 2. References

References to other documents or standards. Follow the IEEE Citation  Reference scheme, available from the [IEEE website](https://www.ieee.org/) (please use the search box). (1 page, longer if required)

## 3. Specific requirements  

20 pages outlining the requirements of the system. You should apportion these pages across the following subsections to focus on the most important parts of your product.

### 3.1 External interfaces

See 9.5.10. for most systems this will be around one page. 

### 3.2 Functions

This is typically the longest subsection in the document. List up to fifty use cases (in order of priority for development), and for at least top ten focal use cases, write a short goal statement and use case body (up to seven pages).  Identify the use cases that comprise a minimum viable product.

Steps marked with asterisks are sub-cases.

#### Run Multiple Simulations Automatically (Minimum Viable Product)

| User Intention                             	  	  | System Requirements                          |
| --------------------------------------------------- | -------------------------------------------- |
| *Import rocket (Minimum Viable Product)*            |                                              |
| *Edit Simulation Location* 						  |                                              |
| Click "Run Simulations"                    		  |                                              |
|                                            		  | *Automated parameter varying*                |
|                                            		  | Run multiple simulations                     |
|                                            		  | *Return results (Minimum Viable Product)*    |

This use case shows the minimum viable product of this project. This does not 
contain any extensions or features allowing the customisation of the 
simulations. This use case is the most important as it represents the minimum
level of functionality that would make a viable product. This is run through the command line and does not include any graphical user interface extensions.

#### Import a Rocket (Minimum Viable Product)

| User Intention              			  | System Requirements                             |
|-----------------------------------------|-------------------------------------------------|
| Input rocket file location with CL flag |                                      			|
|                            			  | Parse file \(Display error if relevant\)        |
|                               		  | Display base information for rocket from import |       

This use case allows users to import a customised rocket from OpenRocket into
our project. This use case is contained within the minimum viable product. It
is essential that users are able to import their own rockets so that the
results of the simulations are applicable to a user's situation, and therefore useful.

#### Edit Simulation Location

| User Intention                   | System Requirements  					 |
|----------------------------------|-----------------------------------------|
|                                  | Prompt for lat and long co-ordinates    |
| Input values       		       |                                         |
|                                  | Record changes                          |

This use case allows users to input custom lat long co-ordinates through the command line.

#### Automated parameter varying

| User Intention              | System Requirements                                                                     |
| --------------------------- | --------------------------------------------------------------------------------------- |
|                             | Take initial given values of parachute ejection time, launch angle or motor performance |
|                             | Create a collection of random inputs for each value type                                |
|                             | Run individual simulations, using the new inputs                                        |

This automated parameter varying forms the basis of the Monte Carlo simulations. 
Currently, users manually vary these values and run simulations. This use case 
is a part of the minimum viable product and important since it is what allows
the user to get results from the Monte Carlo technique.

#### Return Results (Minimum Viable Product)

| User Intention                             | System Requirements                                     |
| ------------------------------------------ | ------------------------------------------------------- |
|                                            | Produce CSV file with the aggregated simulation results |
| 					                         | Export and open results file 				   	       |

This is the returnable results of the minimum viable product. This does not include a scatter plot graph. The results are automatically exported and opened for the user.

#### Run Multiple Simulations Automatically (Extended)

| User Intention                             | System Requirements                          |
| ------------------------------------------ | -------------------------------------------- |
| *Import rocket (Extended)*   			     |                                              |
| *Edit Simulation Automation*               |                                              |
| Click "Run Simulations"                    |                                              |
|                                            | *Automated parameter varying*                |
|                                            | Run multiple simulations                     |
|                                            | *Return results (extended)*                  |

This is an extended workflow that we hope to achieve by the end of trimester. This can be extended more so with the listed features in the "Further Extensions" section. The main benefit of this workflow is it running with a GUI, instead of through the command line interface.

#### Import a Rocket (Extended)

| User Intention                | System Requirements                             |
|-------------------------------|-------------------------------------------------|
| Select "Import rocket"        |                                                 |
|                               | Prompt file selector                            |
| Navigate and open rocket file |                                                 |
|                               | Parse file \(Display error if relevant\)        |
|                               | Display base information for rocket from import |       

This extended use case includes a file selector and is prompted by users selecting "Import Rocket".

#### Edit Simulation Automation 

| User Intention                  	    | System Requirements                                |
| ------------------------------------- | -------------------------------------------------- |
| Select "Edit Simulation Automation"	|                                                    |
|                                     	| Display "Edit Simulation Automation" pop up window |
| Edit "Amount of Simulations"        	|                                                    |
| Set Longitude,Latitude          		|         				                             |
| Select "Save"          			  	|                                                    |
|                                     	| Record changes                                     |

This use case demonstrates how a user would interact with the multiple 
simulation settings. The pop up window will match the style of other OpenRocket setting windows.

#### Return Results (Extended)

| User Intention                             | System Requirements                                     |
| ------------------------------------------ | ------------------------------------------------------- |
|                                            | Produce CSV file with the aggregated simulation results |
|                                            | *Produce Scatter Plot* 								   |
|											 | Display results to user with export options.            |

The extended workflow of returning results includes a scatter plot graph of possible landing locations and a GUI display of results found.

#### Produce Scatter Plot

| User Intention                                      | System Requirements   |
| --------------------------------------------------- | --------------------- |
|                                                     | Generate plots        |
|                                                     | Draw plots onto a map |
|                                                     | Display map to user   |


This is the workflow of producing the scatter plot. This is an extension to the minimum viable product. 

#### Further Extensions:

- Define an upward vector for the rocket to follow

This would allow the user to specify the wind direction and minimise the distance travelled.
- Overlaying over google maps

This would allow the user to view the possible landing sites overlaid on a google maps representation of the launch site, reducing guess work and providing more clarity on landing safety.

- Fix computational listeners in OpenRocket

Fixing the implemenation of computational listeners would allow the program to make changes to the environment model mid-flight simulating for example varying wind speeds at different altitudes

- Motor gimbaling

Implemenation of motor gimbaling could be used to simulate the path of a rocket using a controller to adjust its direction.

- PID Controller simulation

Use the simulations to determine estimations for the PID control parameters.

- Current weather integration

Weather APIs could be used to fetch current environmental variables for simulation.


### 3.3 Usability Requirements

See 9.5.12. for most systems this will be around one page.

> **9.5.12 Usability requirements**<br>
> Define usability (quality in use) requirements. Usability requirements and objectives for the software system include measurable effectiveness, efficiency, and satisfaction criteria in specific contexts of use.

Goal: 
The purpose of the system to provide a rocket simulation that can help determine, given certain conditions, the rocket's path and where it will likely land. By having a range of conditions, the system will show a range of paths and possible landing points. Since this system will be extending OpenRocket, it is important that it is easy for the user to move between systems. It is also important that it is open to the wider avionics community, so it will be made open source so that other can learn and build from it. 

Purpose and Objective: 
For this system to be effective, the product needs to meet the minimum viable product. This means that the system needs to be able to import a rocket from OpenRocket and then run multiple simulations with a variety of parameters. To measure how effective the system is, it can be tested with a range of Rocket types from OpenRocket to ensure that it can be effective with a range of rocket types. It is hard to measure the effectiveness, so the best idea is to test it with a range to make sure that it will work effectively for the user. 

For the system to be efficient, the system needs to be able to complete the minimum viable product and any extensions in a reasonable time. This is means that user will be able to get the output within a reasonable time. This is also very hard to measure but the best way is to test it repeatively with a range of inputs so that the system will be able to function for all the user's needs. 

### 3.4 Performance requirements

See 9.5.13. for most systems this will be around one page. Hardware projects also see section 9.4.6.

> **9.5.13 Performance requirements** <br>
> Specify both the static and the dynamic numerical requirements placed on the software or on human interaction with the software as a whole. 
> 
> Static numerical requirements may include the following:
> 
> a) The number of terminals to be supported;  
> b) The number of simultaneous users to be supported;  
> c) Amount and type of information to be handled.
> 
> Static numerical requirements are sometimes identified under a separate section entitled Capacity.
> 
> Dynamic numerical requirements may include, for example, the numbers of transactions and tasks and the amount of data to be processed within certain time periods for both normal and peak workload conditions. The performance requirements should be stated in measurable terms.
> 
>  For example, "_95 % of the transactions shall be processed in less than 1 second._" rather than, "An operator shall not have to wait for the transaction to complete."
> 
> NOTE Numerical limits applied to one specific function are normally specified as part of the processing subparagraph description of that function.


### 3.5 Logical database requirements

See 9.5.14. for most systems, a focus on d) and e) is appropriate, such as an object-oriented domain analysis. You should provide an overview domain model (e.g.  a UML class diagram of approximately ten classes) and write a brief description of the responsibilities of each class in the model (3 pages).

You should use right tools, preferabley PlantUML, to draw your URL diagrams which can be easily embedded into a Mardown file (PlantUML is also supported by GitLab and Foswiki).

### 3.6 Design constraints

see 9.5.15 and 9.5.16. for most systems, this will be around one page.

> 9.5.15 Design constraints<br>
> Specify constraints on the system design imposed by external standards, regulatory requirements, or project limitations.
> 
> 9.5.16 Standards compliance<br>
> Specify the requirements derived from existing standards or regulations, including:
> 
> a) Report format;<br>
> b) Data naming;<br>
> c) Accounting procedures;<br>
> d) Audit tracing.
> 
> For example, this could specify the requirement for software to trace processing activity. Such traces are needed for some applications to meet minimum regulatory or financial standards. An audit trace requirement may, for example, state that all changes to a payroll database shall be recorded in a trace file with before and after values.

### 3.7 Nonfunctional system attributes

Present the systemic (aka nonfunctional) requirements of the product (see ISO/IEC 25010).
List up to twenty systemic requirements / attributes.
Write a short natural language description of the top nonfunctional requirements (approx. five pages).


### 3.8 Physical and Environmental Requirements 

For systems with hardware components, identify the physical characteristics of that hardware (9.4.10) and environment conditions in which it must operate (9.4.11).  Depending on the project, this section may be from one page up to 5 pages.

Due to the nature of the project being purely software does not have many physical or environmental requirements. The only requirement that the project has, is to have a computer to run the program on. This computer has to have JPype installed, and be running at least Python version 3.0, but Python 3.7.x is recommended.

#### Client Requirements

#### Faculty of Engineering and Computer Science
The faculty requires that all aspects of the project are properly licensed. 

The faculty requires that all aspects of the project follow the guidelines set out by ECS.

##### Critical success factor
It is critical to the success of the project and to the faculty that all guidelines set out by them are followed.

#### Wider Rocket Community

To improve and extend openRocket. To automate some processes, such as choosing variables, and exporting landing results.

##### Critical success factor
In order to be useful for the wider rocket community, it is vital that the software is open-source. This allows the community to use and edit our software under the open source license. If the project is not open source, the benefit to the rocket community would be greatly reduced. 

### 3.9 Supporting information

see 9.5.19. 

## 4. Verification

3 pages outlining how you will verify that the product meets the most important specific requirements. The format of this section should parallel section 3 of your document (see 9.5.18). Wherever possible (especially systemic requirements) you should indicate testable acceptance criteria.

## 5. Development schedule.

### 5.1 Schedule

Identify dates for key project deliverables: 

**architectural prototype**
The architectural prototype will be comeplete by 19 June 2020.

**minimum viable product**
The minimum viable product as defined in part 1.3.2 of this document will be completed by 4 June 2020.

**further releases**
Further releases will occur up until the final prototype release, scheduled for the 29 June 2020.

### 5.2 Budget

Present a budget for the project (table), and justify each budget item (one paragraph per item, one page overall). 

Due to the nature of this project it does not have a budget. The project is extending open source software so there is no need for any licenses to be able to use it. This means that there are no software items that need to be purchased for this project. There is also no physical hardware for this project, so no physical items need to be purchased. This means that there is no items, either hardware or software, to purchase for this project, so the lack of a budget.  

### 5.3 Risks 

Identify the ten most important project risks to achieving project goals: their type, likelihood, impact, and mitigation strategies (3 pages).

If the project will involve any work outside the ECS laboratories, i.e. off-campus activities, these should be included in the following section.

### 5.4 Health and Safety

The project does not involve any external work or testing at any other workplaces or sites. This limits H&S concerns to those present in the team members development environment.
Due to COVID-19 reponse no work is taking place in the Victoria University labs and thus all H&S risks such as cable management, occupational strain and workspace ergonomics are the responsibilty of the team member.
Regular breaks will be taken in the prearranged lab slots to ensure members have a chance to stretch and avoid strain. No ethical considerations need to be made around any animal or human subjects due to the nature of the project.

#### 5.4.1 Safety Plans

Project requirements do not involve risk of death, serious harm, harm or injury. The nature of the project as a pure software development exercise limits the saftey concerns involved.
Due to the COVID-19 pandemic response safety concerns around the observation of social distancing and quarantine procedure were raised and have been addressed by ensuring all team meetings and work sessions are conducted remotely.

## 6. Appendices
### 6.1 Assumptions and dependencies 

One page on assumptions and dependencies (9.5.7).

### 6.2 Acronyms and abbreviations

H&S - Health and Safety
ECS - School of Engineering and Computer Science.

## 7. Contributions

A one page statement of contributions, including a list of each member of the group and what they contributed to this document.

| Name                | Sections Contributed       |
| ------------------- | -------------------------- |
| Luisa Kristen       | 3.8, 5.1                        |
| Zac Durant          | 5.4, 6.2, 1.3                   |
| Zak Kiernander      | 3.2                        |
| Nicole Stallinger   | 3.2                        |
| Caitlin Goodger     | 1,1.1,1.3.1,5.2,3.3           |
| Matthew Butterfield | 1, 1.2, 3.8 spelling and grammar |

---

## Formatting Rules 

 * Write your document using [Markdown](https://gitlab.ecs.vuw.ac.nz/help/user/markdown#gitlab-flavored-markdown-gfm) and ensure you commit your work to your team's GitLab repository.
 * Major sections should be separated by a horizontal rule.


## Assessment  

The goal of a requirements document is the problem you are attempting to solve:  not a first attempt at a solution to that problem. The most important factor in the assessmernt of the document is how will it meet that goal. The document will be assessed for both presentation and content. 

The presentation will be based on how easy it is to read, correct spelling, grammar, punctuation, clear diagrams, and so on.

The content will be assessed according to its clarity, consistency, relevance, critical engagement and a demonstrated understanding of the material in the course. We look for evidence these traits are represented and assess the level of performance against these traits. While being comprehensive and easy to understand, this document must be reasonably concise too. You will be affected negatively by writing a report with too many pages (far more than what has been suggested for each section above).

We aim to evaluate ENGR301 documents and projects as if they were real projects rather than academic exercises &mdash; especially as they are real projects with real clients. The best way to get a good mark in a document is to do the right thing for your project, your client, and your team. We encourage you to raise questions with your tutor or course staff, as soon as possible, so you can incorporate their feedback into your work.

---
