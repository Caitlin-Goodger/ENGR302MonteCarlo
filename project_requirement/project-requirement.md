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

One page overall introduction including sections 1.1 and 1.2.

Amateur rockets are flown regularly worldwide. These rockets are typically flown with off the shelf rocket motors with widely available propellant reloads. These rockets often exceed the speed of sound, altitudes above 30 km are not unheard of. These rockets are almost never controlled, they are stable due to passive aerodynamic features. 

While passively stable rockets are reasonably simple and reliable if well designed, they are susceptible to a variety of disturbances, particularly early in flight. Unexpected winds can cause the rocket to weathercock; flexibility in the launch tower/rail can cause railwhip, imparting a random launch angle to the rocket; the thrust from the rocket motor is also never perfectly symmetrical.

Amateur rockets are often designed in OpenRocket. OpenRocket gives the ability to simulate rockets while altering some parameter variables as a suggestion for the rocket’s performance. After a rocket has been built, it can be measured accurately to give a more accurate simulation to allow for smaller, finalising adjustments including moving the centre of mass. Automation can allow follow this process to be sped up and determine to a higher confidence of the safety of the flight.

The rocket uses a PID (Proportional Integral Derivative) controller to keep it fixed on an axis. Normally, parameters of PID are difficult to obtain due to the short period of time that the rocket motors are burning. Simulation can allow for estimate parameters for the PID controller.


### Client

Identify the client and their contact details

Andre Geldenhuis is the client for this project. He has experience with rockets and experience working with similar projects. He can be reached in the Customer Channel on Mattermost. He also has occasionally Q&A sessions during ENGR301 Lectures and can be reached during those times with questions. He can also be reached at andre.geldenhuis@vuw.ac.nz. 

### 1.1 Purpose

One sentence describing the purpose of the system (9.5.1)

The purpose of the system to provide a rocket simulation that can help determine, given certain conditions, the rocket's path and where it will likely land. By having a range of conditions, the system will show a range of paths and possible landing points.

### 1.2 Scope

One paragraph describing the scope of the system (9.5.2)

This product is a Rocket Simulation program. The program shall provide an automation of simulation program OpenRocket to give a prediction of the flight performance of a rocket. The program shall provide likely landing locations based on varying parameters such as launch angle and parachute ejection time, through a form of Monte Carlo simulation to determine whether the flight is safe. The program shall provide estimate PID control parameters through the simulation.

### 1.3 Product overview 

The following subsections describe the product perspective, functions, characteristics and liimitations.

#### 1.3.1 Product perspective

One page defining the system's relationship to other related products
(9.5.3. but not the subsections in the standard.)

> **9.5.3 Product perspective** <br>
> Define the system's relationship to other related products. 
> 
> If the product is an element of a larger system, then relate the requirements of that larger system to the functionality of the product covered by the software requirements specification.
> 
> If the product is an element of a larger system, then identify the interfaces between the product covered by the software requirements specification and the larger system of which the product is an element. 
>
> A block diagram showing the major elements of the larger system, interconnections, and external interfaces can be helpful.
> 
> Describe how the software operates within the following constraints:  
a) System interfaces;  
b) User interfaces;  
c) Hardware interfaces;  
d) Software interfaces;  
e) Communications interfaces;  
f) Memory;  
g) Operations;  
h) Site adaptation requirements.

The project is extending existing software. OpenRocket is an existing opensource project that allows users to design and simulate rocket models before creating the building them. This project is extending the simulation capabilities to allow for multiple simulations to be run at once. OpenRocket only allows for one simulation, with one set of conditions and parameters, so this project is extending this functionality to have multiple simulations and multiple conditions and parameters. Since this project is extending existing software it needs to be able to interact with OpenRocket and have similar looking interfaces for ease of use. The user will need to create the model for their rocket in OpenRocket. The project will then use that rocket to run the simulation. This means that it needs to be able to export the data from OpenRocket and be able to use it in the simulation. 

This project is also part of a large project. There is another project focused on building a rocket and another project focused on Mission Control. This project will be the go-between of the hardware and the software components. This means that the project needs to be interact with the other two projects and communicate with them. The project building a rocket needs to be able to use the simulation to know how the rocket they have designed will travel and where it could land. The Mission Control project also needs to use the simulation for functionality such as knowing if the current weather conditions are safe to launch in. Mission Control will be using this project while at the rocket launch site which will likely not have an internet connection. This means that the project needs to be able to function without requiring an internet connection as well. 

#### 1.3.2 Product functions

One page summary of the main functions of the product (9.5.4), briefly characterising the minimum viable product.

One page summary of the main functions of the product (9.5.4), briefly characterising the minimum viable product.

To meet the requirements of the minimum viable product the project will;
-Be able to take a rocket designed in OpenRocket
-Take a given latitude and longitude point
-Run mutliple simulations with the given rocket and co-ordinates and produce possible landing points

#### 1.3.3 User characteristics   

One page identifying the main classes of users and their characteristics (9.5.5) 

#### 1.3.4 Limitations

One page on the limitations on the product (9.5.6)

## 2. References

References to other documents or standards. Follow the IEEE Citation  Reference scheme, available from the [IEEE website](https://www.ieee.org/) (please use the search box). (1 page, longer if required)

## 3. Specific requirements  

20 pages outlining the requirements of the system. You should apportion these pages across the following subsections to focus on the most important parts of your product.

### 3.1 External interfaces

See 9.5.10. for most systems this will be around one page. 

### 3.2 Functions

This is typically the longest subsection in the document. List up to fifty use cases (in order of priority for development), and for at least top ten focal use cases, write a short goal statement and use case body (up to seven pages).  Identify the use cases that comprise a minimum viable product.

#### Simulations for Range Safety and Site Selection- Monte Carlo:


| Run Multiple Simulations Automatically |  |
| ----------- | ----------- |
| Configure rocket and simulation parameters | |
| *Edit Simulation Automation* |        |
| Click "Run Simulations"|         |
| | *Automated parameter varying* |
| | *Return the results of multiple simulations* |

This use case is important because it automates the running of multiple
simulations. Currently, if users want to run multiple simulations for a given 
rocket, they have to run each simulation individually.  

| Automated parameter varying |  |
| ----------- | ----------- |
|    | Take initial given values of parachute ejection time, launch angle or motor performance |
| | Create a collection of random inputs for each value type|
| | Run individual simulations, using the new inputs|

This use case is important as it reduces a significant amount of manual work 
done by users. Currently, users manually vary these values across several 
simulations to form an average. The new values will be random within a
range. The size of the range can be varied in the Simulation Automation
settings. The mid point of the range is provided by the user when configuring
the base simulation. 

| Edit Simulation Automation |  |
| ----------- | ----------- |
| Select "Edit Simulation Automation" |        |
| | Display "Edit Simulation Automation" pop up window |
| Edit "Amount of Simulations" |         |
| Edit "Maximum Value Variance" | |
| Select "Save as Default" | |
| | Record changes |

This use case demonstrates how a user would interact with the multiple 
simulation settings. The "Edit Simulation Automation" button will be a button
next to "Edit Simulation". The pop up window contains an input box and slider 
for the two available settings, matching the style of other OpenRocket settings.

| Return the results of multiple simulations  |  |
| ----------- | ----------- |
|       |   |
|    |         |

| Produce scatter plot from automations of landing sites  |  |
| ----------- | ----------- |
| Highlight wanted simulations, or click "Select all"      |        |
| Click "Plot / Export"   |         |
| | Open "Plot / Export" setting pop up window |
| | Default to 

| Visually showing possible landing locations          |                       |
|------------------------------------------------------|-----------------------|
| Highlight wanted simulations, or click "Select all"  |                       |
| Click "Plot / Export"                                |                       |
|                                                      | Generate plots        |
|                                                      | Draw plots onto a map |
|                                                      | Display map to user   |
| Click download/export map                            |                       |

##### Extensions:

Define an upward vector for the rocket to follow (to minimise landing distance from launch).

#### Rocket Simulation for Control Tuning and Design:

Fix simulation listeners in Open Rocket.

Implement motor gimbaling.

Implement a PID controller simulation.

Use the simulations to determine estimations for the PID control parameters.


### 3.3 Usability Requirements

See 9.5.12. for most systems this will be around one page.

> **9.5.12 Usability requirements**<br>
> Define usability (quality in use) requirements. Usability requirements and objectives for the software system include measurable effectiveness, efficiency, and satisfaction criteria in specific contexts of use.

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
The minimum viable product as defined in part 1.3.2 of this document will be completed by 29 June 2020.

**further releases**
Further releases will occur up until the final prototype release, scheduled for the 16 October 2020.


### 5.2 Budget

Present a budget for the project (table), and justify each budget item (one paragraph per item, one page overall). 

Due to the nature of this project it does not have a budget. The project is extending open source software so there is no need for any licenses to be able to use it. There is also no physical hardware for this project, so no physical items need to be purchased. 

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

One page glossary _as required_.
H&S - Health and Safety

## 7. Contributions

A one page statement of contributions, including a list of each member of the group and what they contributed to this document.

| Name | Sections Contributed|
| ---- | ----               |
|Luisa Kristen| 5.1|
|Zac Durant   | 5.4, 6.2|
|Zak Kiernander | 3.2 |
|Nicole Stallinger      |3.2 |
|Caitlin Goodger|1,1.1,1.3.1,5.2|
|Matthew Butterfield| 1,1.2,spelling and grammar |

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
