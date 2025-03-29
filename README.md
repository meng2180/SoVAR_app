### SoVAR

---

This is an automatic driving software test case generation system based on large language model. The system can extract information from the traffic accident report imported by users, and generate test cases that meet the accident description. The generated test cases can be directly applied to the simulator LGSVL.



#### Features

---

* **High accuracy of information extraction**. By default, the system uses GPT-4 to extract traffic accident information reports, and the average accuracy rate of information is over 80%. At the same time, the system also supports other models, and all of them have high accuracy.

* **Good reproduction effect for car accident description**.  The system uses the constraint solver Z3 to solve the waypoints that conform to the actual action of the accident vehicle, and automatically analyzes the simulator map information through the algorithm, and finally maps the waypoints to the road corresponding to the accident scene in the simulator map, so as to generate a test case with better reproduction effect.
* **Easy to install and use**. The use of the system only needs to clone the code locally and install the required Python dependencies to run.



#### How to use?

---

1. Click the file menu in the menu bar and select the Import Report button, and the file selector will pop up. At this time, select the text file of the accident report and import it, and the system will automatically analyze the report and display the analysis results in the extraction result display area. 

   If "Add information extraction record" is checked, which means that you fill in the truth value of the report and want to count the cumulative extraction accuracy of the system, then the system will compare the extraction result with the information in the truth configuration area, so as to record and update the cumulative extraction accuracy of information.

   You can also customize the configuration information in the information truth configuration area without importing reports, which means that you want to generate test cases from customized accident scenarios.

2. Next, you need to click the Use Case Generation button in the File menu, and the system will generate corresponding test cases according to the information in the information extraction result display area, and then display the generated use cases in the use case generation result display area; 

   If you check "Used for test case generation", the system will generate test cases according to the information in the information truth configuration area; Then, you can click the use case preview button in the file menu to preview the trajectory effect of the generated test case in the two-dimensional coordinate system.

3. Finally, you can click the Recurrence Test button or Simulation Test button in the menu to test by connecting the simulator LGSVL and autopilot software Apollo. 

   

   It is worth noting that the system provides a copy function for each display result, and you can copy this information for use.
