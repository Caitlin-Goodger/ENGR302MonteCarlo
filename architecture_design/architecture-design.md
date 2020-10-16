# ENGR 301: Architectural Design and Proof-of-Concept

## Table of Contents [1]

- [ENGR 301: Architectural Design and Proof-of-Concept](#engr-301--architectural-design-and-proof-of-concept)
  * [Table of Contents](#Table of Contents)
- [ENGR 301 Project 14 Architectural Design and Proof-of-Concept](#engr-301-project-14-architectural-design-and-proof-of-concept)
  * [1. Introduction](#1-introduction)
    + [Client](#client)
    + [1.1 Purpose](#11-purpose)
    + [1.2 Scope](#12-scope)
    + [1.3 Changes to requirements](#13-changes-to-requirements)
  * [2. References](#2-references)
  * [3. Architecture](#3-architecture)
    + [3.1 Stakeholders](#31-stakeholders)
    + [3.2 Architectural Viewpoints](#32-architectural-viewpoints)
   + [4. Architectural Views](#4-architectural-views)
    + [4.1 Logical](#41-logical)
    + [4.2 Development](#42-development)
    + [4.3 Process](#43-process)
    + [4.4 Physical](#44-physical)
    + [4.5 Scenarios](#45-scenarios)
  * [5.1 Development Schedule](#51-development-schedule)
    + [5.2 Budget and Procurement](#52-budget-and-procurement)
    + [5.3 Risks](#53-risks)
    + [5.4 Health and Safety](#54-health-and-safety)
  * [6. Appendices](#6-appendices)
  * [7. Contributions](#7-contributions)

# ENGR 301 Project 14 Architectural Design and Proof-of-Concept

Caitlin Goodger, Luisa Kristen, Zac Durant, Zak Kiernander, Nicole Stallinger and Matthew Butterfield.

## 1. Introduction

Amateur rockets are flown regularly worldwide. These rockets are typically flown with off the shelf rocket motors, and widely available propellant reloads. These rockets often exceed the speed of sound, with altitudes above 30 km not being unheard of. These rockets are almost never controlled, they are stable due to passive aerodynamic features.

While passively stable rockets are reasonably simple and reliable if well designed, they are susceptible to a variety of disturbances, particularly early in flight. Unexpected winds can cause the rocket to weathercock; flexibility in the launch tower/rail can cause rail-whip, imparting a random launch angle to the rocket; the thrust from the rocket motor is also never perfectly symmetrical.

Amateur rockets are often designed in OpenRocket. OpenRocket gives the ability to simulate rockets while altering some parameter variables as a suggestion for the rocket’s performance. After a rocket has been built, it can be precisely measured to give a more accurate simulation to allow for smaller, finalising adjustments, including moving the centre of mass. Automation can allow follow this process to be sped up and determine to a higher confidence of the safety of the flight.

### Client

Andre Geldenhuis is the client for this project. He has experience with rockets and experience working with similar projects. He can be reached in the Customer Channel on Mattermost. He also has occasionally Q&A sessions during ENGR301 Lectures and can be reached during those times with questions. He can also be reached at andre.geldenhuis@vuw.ac.nz.

### 1.1 Purpose

The purpose of the system to provide a rocket simulation that can help determine, given certain conditions, the rocket's path and where it will likely land. By having a range of conditions, the system will show a range of paths and possible landing points.

### 1.2 Scope

This product is a Rocket Simulation program. 

*  The program shall provide an automation of simulation program OpenRocket to give a prediction of the flight performance of a rocket. 
*  The program shall provide likely landing locations based on varying parameters such as launch angle and parachute ejection time, through a form of Monte Carlo simulation to determine whether the flight is safe. 


### 1.3 Changes to requirements

The program originally was scoped to either generate suitable PID control parameters through the simulations, or take PID values as input parameters. This because out of scope for this project due to the limitations brought by OpenRocket. This feature would require complex and messy changes to OpenRocket and is not well supported. 

## 2. References

[1] “GitHub Wiki TOC generator,” Generate TOC Table of Contents from GitHub Markdown or Wiki Online. [Online]. Available: http://ecotrust-canada.github.io/markdown-toc. [Accessed: 11-June-2020].

[2] “Developer's Guide,” Developer's Guide - OpenRocket wiki, 30-Apr-2020. [Online]. Available: http://wiki.openrocket.info/Developer's_Guide. [Accessed: 08-May-2020].

[3] “Features of OpenRocket,” OpenRocket. [Online]. Available: http://openrocket.info/features.html. [Accessed: 22-May-2020].

[4] “gnu.org,” GNU Operating System. [Online]. Available: https://www.gnu.org/licenses/gpl-howto.html. [Accessed: 22-May-2020].

[5] S. Writer, “Top 10 Software Development Risks,” ITProPortal, 14-Jun-2010. [Online]. Available: https://www.itproportal.com/2010/06/14/top-ten-software-development-risks/. [Accessed: 22-May-2020].

[6] "Sequence Diagram", PlantUML. [Online]. Available: https://plantuml.com/sequence-diagram. [Accessed: 29-May-2020]

[7] "Class Diagram", PlantUML. [Online]. Available: https://plantuml.com/class-diagram. [Accessed: 29-May-2020]

[8] "What is Component Diagram", Visual-Paradigm. [Online]. Available: https://www.visual-paradigm.com/guide/uml-unified-modeling-language/what-is-component-diagram/ [Accessed: 29-May-2020]

## 3. Architecture

### 3.1 Stakeholders

#### Stakeholder Requirements

The stakeholder requirements are consistent with those found in section 3.8 of the Project Proposal and Requirements Document.

### 3.2 Architectural Viewpoints

**Logical:**

The logical view describes the how the system functions for the end user. The diagrams below help to illustrate how the system performs those functions and how the user interacts with the system. The diagram illustrates how the user interacts with each of the classes inside the system. It provides an explanation of how the classes interact with each other so that the user can utilise the system. 

**Development:**

 The development viewpoint describes the architecture the support the processes involved in the development cycle to manage the software. It describes the management system of the software to address the concerns regarding the management. 

**Process:**

The process viewpoint describes the dynamic and non-functional requirements. These requirements include concerns around performance and availability concurrency. It also describes how the logical views fits with the process view.  

**Physical:**

The physical viewpoint describes how the software fits with the hardware of the system. It describes the how the software deals with the hardware availability, reliability, performance and scalability of the system. 

**Scenarios:**

 The scenarios viewpoint describes the user cases of the system. It describes how the user and the system interact with each other. 

**Circuit Architecture:**

The circuit architecture viewpoint describes how the physical system is put together. Due to the fact that this is entirely a software project this section is not appropriate for this project.

**Hardware Architecture:**

The hardware architecture viewpoint describes how the hardware functions in the system, and allows it to function. Due to the fact that this is entirely a software project this section is not appropriate for this project. 

### 4. Architectural Views

This section describes our system's architecture, in a series of architectural views. Each of these views corresponds to one viewpoint. 

### 4.1 Logical


#### User interaction model

The user interaction model shows all the classes as well as the user and how they interact.  The user is shown on the far left of the diagram as they start off the process. The classes are shown in boxes along to top and bottom on the digram. The classes are at the top and the bottom so that it is easier for the user to read. There are red dotted lines between the two boxes for a class. This makes means that it is clear where each class sits. There are red arrows between classes to show how the classes interact with each other. These arrows are labeled with explanations so that it is clear why the two classes interact with each other. The arrows map out the entire process from the user running the system, to receiving the output at the end. Boxes with further explanations are also on the diagram to add further context as to what is happening.

![Actor Diagram](../project_requirement/actorDiagram.svg)


#### Class interaction model

The class interaction model shows how all the classes interact. Each class is has a box that shows the name of the class as well as a definition of the class and what it provides the user. There are then arrows between the classes show how they interact with each other. There is a definition associated with the arrow, as to why there is a connect between those two classes. 

![Class Diagram](../project_requirement/classDiagram.svg)


### 4.2 Development

#### Component Model

![Component Diagram](componentDiagram.PNG)

This diagram shows the relationships of our system with external components, and the necessary interfaces.

Most of the management for the development process is managed by GitLab, which is the version control system used for this project.  One of the risks that we had identified was the loss of files and work. We have managed this risk by ensuring that all files and work is to be stored on the Gitlab, either in the repository or on the wiki if that is more appropriate. By having all the work on Gitlab, all members of the group are able to find and view the progress that is being made. 

We will also create branches for issues, so that there is no chance of overwriting someone else work and have less conflicts. It allows multiple features to be developed at once by having one branch per feature. This also allows for non-functioning code to be committed to GitLab. By keeping non-functioning code off of master, it means that master always contains a functioning version, while having developing code on other branches. This also allows for a branch to be removed and never merged into master if the feature is no longer required or is unable to correctly function. Once a feature is complete, and has been tested, it can be merged back into master by creating a merge request. This then allows the other group members the ability to review the code before it is merged into master. This requirement for approval ensures that every piece of code is reviewed by at least two members of the team. This also adds insurance that the written code functions as described in the issue. Branching is a feature that it built into GitLab, which means that it is easy to integrate with this project.

Another feature of GitLab that is being utilised for this project is that of Milestones and Issues. Issues are created for something that needs to be fixed or implemented. Issues can then be assigned weights. These issues are picked up by team members. This ensures that every member of the group knows what every other member is doing. It also prevents multiple people accidentally starting work on the same issue. Issues can be grouped in Milestones, which is a larger goal. An example of a Milestone could be the minimum viable product. These tools help manage the project, as it helps everyone understand what is currently being work on and how close to completing each step. GitLab offers multiple graphs, including burn-down charts to help illustrate this point. 


### 4.3 Process

The process viewpoint describes the dynamic and non-functional requirements. It shows the process what happens when the user runs the system. It shows all the interacts between classes and the order in which they happened. 

The sequence model diagram is set up in the same way as the user interaction model in the logical view. The user is shown on the left of the diagram and the classes being shown in boxes along the top and bottom. There is also a box for the output file, where the results are put at the end of the process. There are arrows between the classes and the user that shows when they classes and users interact with each other. The arrows include a definition of the arrow and explanation of what happens. This definition helps explain the process and show what happens. There is a box in the middle of the diagram what is labeled loop. This section loops through n times and is in a loop box so that the arrows don't need to be repeated and the diagram is clearer. 

Sequence model
![Sequence Diagram](sequenceDiagram.svg)

### 4.4 Physical 

This project is entirely a software project. This section describes the how the software deals with the hardware availability, reliability, performance and scalability of the system. Due to the fact that this is entirely a software project these are no concerns that need to be considered. As the software is creating a simulation, it doesn't have deal with hardware availability, reliability, performance and scalability. These would the hardware features that can made it harder to integrate the software with the hardware. 

However, this project is part of a larger system that does have hardware components. For this project to be able to interact with the larger system, there are some hardware concerns. When interacting with projects that have hardware, there may be some concerns around how the software integrates with the hardware of those projects. These concerns are the concerns mentioned above. While these aren't concerns for this project, they are concerns when interacting with other project. Since they aren't concerns for this project, there are no architecture views in this section, but they may need to be considered when interacting with other projects.

The simulation function of this project, this will be used by groups building a rocket to simulate how the rocket design will fly, and where it could land. The simulation is not dependent on the hardware, as it can be run with any model of a rocket, as long as this was created in OpenRocket.


### 4.5 Scenarios

We have determined our 2 most important scenarios for our MVP are: 
* The user is able to run multiple simulations, and be able to run these simulations on any valid rocket file that the user imports. 
	* As such, our design will utilise the OrHelper, which allows the user to import rocket files, while maintaining a consistent connection to OpenRocket.
* During these simulations, optional arguments are able to vary environmental factors
	* These factors impact the subsequently returned landing points. 

## 5.1 Development Schedule

Schedules must be justified and supported by evidences; they must be either direct client requirements or direct consequences of client requirements. If the requirements document did not contain justifications or supporting evidences, then both must be provided here.

Identified dates for key project deliverables: 

**Architectural prototype**
The architectural prototype will be complete by 18 June 2020. This date was chosen as it was the last lab before Performance Assessment 2. 

**Minimum viable product**
The minimum viable product as defined in part 1.3.2 of the Project Requirement document will be completed by 4 June 2020. This date was chosen based on time estimations; the combined estimated time for all tickets required estimated a completion date of the 4th of June. 

**Further releases**
Further releases will occur up until the final prototype release, scheduled for the 1 October 2020. This is the last week scheduled for this project. 

**Changes to these dates**
These dates have not been changed from the project requirement document.

### 5.2 Budget and Procurement

#### 5.2.1 Budget

Due to the nature of this project it does not have a budget. The project is extending open source software so there is no need for any licenses to be able to use it. There is also no physical hardware for this project, so no physical items need to be purchased.

#### 5.2.2 Procurement

As stated previously, the nature of the project being purely software means that it does not require hardware items which would need to be procured. The only software required is OpenRocket which is open source and available for access at any point. The storage of the code will be on a group gitlab which is supplied by the university.

### 5.3 Risks 

|                          Risks                          | Risk Type | Likelihood | Impact | Mitigation Strategies                                                                          |
| :-----------------------------------------------------: | --------- | ---------- | ------ | ---------------------------------------------------------------------------------------------- |
|Program functioning unexpectedly on different devices          | Technical     | 2          | 3      | Test on multiple different devices.                                                                                                                                                                                                         |
|Adding team members that do not work well with the team        | Teamwork      | 1          | 2      | Have a team contract which all members agree to at time of joining the group.                                                                                                                                                               |
|Losing team member temporarily or permanently at crucial times | Teamwork      | 1          | 3      | Communicate and document issues, progress and plans to the git.                                                                                                                                                                             |
|Team members burning out                                       | Teamwork      | 3          | 3      | Members communicate when they are having issues. Members have regular breaks during lab times.                                                                                                                                              |
|Loss of access to files                                        | Technical     | 1          | 4      | Assure that all files are on the git and on team members devices.                                                                                                                                                                           |
|Not meeting deadlines by underestimating time required         | Technical     | 3          | 2      | Have regular meetings to manage milestones and divide tasks into smaller sections.                                                                                                                                                          |
|Unresolved conflicts between team members                      | Teamwork      | 2          | 3      | Have a team contract with paths to bringing up issues to the rest of the group.                                                                                                                                                             |
|Changes to project requirements                                | Requirements  | 3          | 4      | Create code that is easily adjustable. Only allow minor adjustments (or changes with good reasoning) to the project later.                                                                                                                  |
|Issues with integration of software                             | Technical     | 3          | 4      | Edit software to better flow between sections. Understand software used and the outputs given. Disable features that might be causing issues. Look at possibly using a different version of software for stability and ease of integration. |
|Bugs within the code go undetected                             | Technical     | 3          | 4      | Have test cases with high coverage over the program. Check tests frequently throughout development to assure that new issues have not occurred. Have multiple people working on and checking the same code to avoid logic errors.           |

### 5.4 Health and Safety

The project does not involve any external work or testing at any other workplaces or sites. This limits H&S concerns to those present in the team members development environment.

Due to COVID-19 response no work is taking place in the Victoria University labs and thus all H&S risks such as cable management, occupational strain and workspace ergonomics are the responsibility of the team member.
Regular breaks will be taken in the prearranged lab slots to ensure members have a chance to stretch and avoid strain. 

No ethical considerations need to be made around any animal or human subjects due to the nature of the project.

#### 5.4.1 Safety Plans

Project requirements do not involve risk of death, serious harm, harm or injury. The nature of the project as a pure software development exercise limits the safety concerns involved.

Due to the COVID-19 pandemic response safety concerns around the observation of social distancing and quarantine procedure were raised and have been addressed by ensuring all team meetings and work sessions are conducted remotely.

## 6. Appendices

### 6.1 Assumptions and dependencies 

- It is assumed that the user has access to a computer, which is able to run openRocket. 
- It is assumed that the members of the model rocket community, and other users, are familiar with openRocket.
- It is assumed that the user will already have a model rocket to load into openRocket.
- It is assumed that for use of the minimum viable product, the user is able to operate Command Line / Terminal, as this does not include the use of a GUI. 
- It is assumed that the inputs entered by the user are of the correct type in order to successfully run the simulations. 

### 6.2 Acronyms and abbreviations

H&S - Health and Safety

ECS - School of Engineering and Computer Science.

## 7. Contributions

| Name | Sections Contributed|
| ---- | ----               |
|Luisa Kristen| 1, 1.1, 1.2, 3.1, 4, 4.3, 4.4, 4.5,  5.1, 5.2.1, 5.4, 5.4.1, Spelling & Grammar |
|Zac Durant   | 4.1, 4.3             |
|Zak Kiernander | 4.5          |
|Nicole Stallinger| 4.2        |
|Caitlin Goodger|1,1.1,3.2,4.1,4.2,4.3,4.4,5.2.1           |
|Matthew Butterfield| 5.1, 5.2.2, 5.3, 6.1, 6.2 |
