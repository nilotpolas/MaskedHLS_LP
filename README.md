# Overview of MaskedHLS

**MaskedHLS** is a domain-specific high-level synthesis tool designed to aid in the automated generation of secure and optimized gadget-based masked cryptographic hardware implementations from their masked C versions. It incorporates the following features:

## Key Features
1. **High-Level Synthesis**  
   Converts high-level cryptographic designs (e.g., C programs) into Register-Transfer Level (RTL) representations, focusing on mimimizing registers via low-hanging latency optimizations in hardware masked designs secure against power side-channel attacks.

2. **Masking and Balancing Verification**
   - Ensures lowest possible latency given the set of gadgets used to mask the high-level code.
   - Automatically verifies whether the generated RTL design is register balanced.

4. **Customizable Parameters**  
   - Accepts various user-defined parameters such as bit width, input file, and balancing checks, enabling flexible design exploration.

5. **Functional Verification**  
   Provides support for simulation-based verification to ensure functional correctness of the generated designs using tools like Icarus Verilog.

6. **Security Analysis**  
   Offers a pipeline for TVLA (Test Vector Leakage Assessment) to analyze the security of the design after synthesis steps.

7. **Graphical Analysis**  
   Supports visualization of the Abstract Syntax Tree (AST) and Data Flow Graph (DFG) at various stages of the synthesis process for debugging and analysis.

## Applications
MaskedHLS is primarily designed for the cryptographic hardware community. It is particularly useful for:
- Generating secure S-box designs for AES, PRESENT, and other cryptographic algorithms.
- Automating the implementation of hardware masking techniques at C level.

## Why MaskedHLS?
The tool reduces the manual effort involved in designing, implementing, and verifying masked cryptographic hardware while ensuring high efficiency and strong side-channel resistance. MaskedHLS bridges the gap between high-level design and secure hardware implementation with a focus on seamless design-space exploration.

# Instructions to Install and Execute the Tool
## Installing the dependencies

```bash
  pip install -r requirements.txt
```
    
## Run the tool

cd to the folder where the script.py file is present.
Run the following command:
```
 $ python script.py <options>
```
The following operations are supported.


| Option  | Use |
| ------------- | ------------- |
| --topModule  | Name of the top topModule (mandatory)  |
| --inputFile  |  Name of the input file (it is mandatory too and shouldbe in the same directory as script.py |
| --rtlFile|the final verilog code file(default is output.v) |
| --bitWidth|specify the bitWidth for the rtl code |
| --checkBalancing|Set to 1 to verify the balancing (default is 0) |



## Note

- Temporary files will be generated in the tempFiles folder.
- The output Verilog file will be in the same folder as the input file.
  
## Getting Started: 

### Example 1: AES DOM Masked S-box
**Input:**
```bash
$ python3 script.py --topModule=sbox --inputFile=../test/AES/DOM/input.c --rtlFile=../test/AES/DOM/output.v --bitWidth=8
```
**Output:**
```
----------Nodes and edges------------
1308
2402
-------------------------------------
Max path weight 4
No of registers if added levelwise: 4752
Execution Time
--- 1.644021987915039 seconds ---
```

**Output Meaning:** 
- **Nodes and edges:**  
  - 1308 // number of nodes in the HLS-model  
  - 2402 // number of edges in the HLS-model  
- **Max path weight:** 4 // desired minimum latency  
- **No of registers if added levelwise:** 4752 // manual number of registers adding level-wise  
- **Execution Time:** 1.644021987915039 seconds  

### Example 2: PRESENT DOM Masked S-box
**Input:**
```bash
$ python3 script.py --topModule=sbox --inputFile=../test/PRESENT/DOM/input.c --rtlFile=../test/PRESENT/DOM/output.v --bitWidth=1
```
**Output:**
```
----------Nodes and edges------------
105
180
-------------------------------------
Max path weight 3
No of registers if added levelwise: 168
Execution Time
--- 0.04634523391723633 seconds ---
```

### Example 3: Checking balancing PRESENT DOM Masked S-box
**Input:**
```bash
$ python3 script.py --topModule=sbox --inputFile=../test/PRESENT/DOM/input.c --rtlFile=../test/PRESENT/DOM/output.v --bitWidth=1 --checkBalancing=1
```
**Output:**
```
----------Nodes and edges------------
105
180
-------------------------------------
Max path weight 3
No of registers if added levelwise: 168
Execution Time
--- 0.05016446113586426 seconds ---
Design is balanced.
```

**Output Meaning:**
- **Check balancing** verifies if the balancing is correct. Runs another pass.
- **Nodes and edges:** 105 and 180, respectively.
- **Max path weight:** 3 // checks the latency
- **No of registers if added levelwise:** 168 // checks the number of registers added levelwise
- **Execution Time:** 0.05016446113586426 seconds // takes a little more time than the actual balancing process
- **Design is balanced.**

## Bonus Features:
1. **Checking functional correctness via Simulation-Based Verification:**  
   **Step1: Install ICARUS-verilog**
   ```
   sudo apt-get install iverilog
   ```
   **Step2: Write a testbench file**
    We have testbenches for the AES and PRESENT S-boxes:
   ```
   MaskedHLS_LP-master/src/FunctionalCorrectness/PRESENT/present_tb.v
   ```
   ```
   MaskedHLS_LP-master/src/FunctionalCorrectness/AES/aes_tb.v
   ```
    **Step3: Generate the simulation input files**
   The input generator code generates the input simulation files: 
   ```
   MaskedHLS_LP-master/src/FunctionalCorrectness/input_generator.py
   ```
   Run it using:
   ```
   python input_generator.py
   ```
   You can edit the *total_record = 50000* on line *37* in the file to specify the total number of records
   It asks for the following input
   ```
   Enter Size of N: 
   ```
   Here N means the number of samples you want to test the design for:
   Say we put 498, it gives us the test for that many number of samples into files "out0Comb.txt","out1Comb.txt"  with the 0-shares and 1-shares respectively.

    **Step4: Simulate the verilog file using**
   ```
   iverilog -o simulation design.v design_tb.v
   ```
   ```
   vvp simulation
   ```

   **Step5:Sort and compare the generated simulation file with the original S-box output**
   ```
   diff simulation_out_cfile_sorted.csv simulation_out_iverilog_sorted.csv
   ``` 

2. **Checking the AST-graphs**
    We can print the AST after dummy node insertion (or at any step in the algorithm by re-using the same function) by uncommenting line 62 in:
   
    ```
    MaskedHLS_LP-master/src/RegBalancer/src/main.py
    ```
  
    the line is: 
    
    ```
    save_graph(dfg_gen.dfg, "graph.png")
    ```
  
    The graph will be generated at:
    
    ```
    MaskedHLS_LP-master/src/graph.png
    ```
    Note: Doing this for bigger designs (AES) is not scalable due to the screen being unable to render such a huge graph.

  
3. **TVLA - analysis**: Automated scripts to be used after the design compiler is used to generate netlist.

   Use design compiler to generate the netlist:  
   **Steps for Netlist Generation:**

   1. Given that RTL output from MaskedHLS_LP is `present_hpc2.v`.

   2. Run:

      ```bash
      dc_shell -f dc_script.tcl
      ```
      This will generate `present_hpc2.dc.v`, `file1.sdc`, `sbox.area`, `sbox.timing`, `sbox.power` (make sure all the paths are correct in the `dc_script.tcl` file).

   **Steps for TVLA:**

   **Tools required: Synopsys PrimeTime, Synopsys Design Compiler, Synopsys WaveView**

   1. a. Remove unnecessary files (you can write a script for it: `cleanup.sh`):

         ```bash
         bash cleanup.sh
         ```

      b. **Replace the value of the variables in the file in the path:**

         ```bash
         MaskedHLS_LP-master/src/SecurityAnalysis/PRESENT/5cycle/hpc2/input_generator.py
         ```
         - `parameter latency = 5;` (design latency)
         - `parameter N = x;` // use `x` from one of the values in the following table

         These values are only for PRESENT for 5 cycles (hpc1, hpc2):  

         ```
         /---------------------------------------------\
         | Picoseconds(ps)|  N   |  3N  |    Traces    |
         ----------------------------------------------
         |      300       | 166  | 498  |      82k     |
         |      275       | 181  | 543  |      98k     |
         |      240       | 208  | 624  |     129k     |
         |      225       | 222  | 666  |     147k     |
         |      215       | 232  | 696  |     161k     |
         |      175       | 285  | 855  |     243k     |
         |       85       | 588  | 1764 |   103.7k     |
         |       75       | 666  | 1998 |     133k     |
         \---------------------------------------------/
         ```

      c. **Run input generator:**

         ```bash
         python3 input_generator.py
         ```

   2. **Run vlogan**:

      ```bash
      vlogan -full64 tsl18fs120_scl.v present_hpc2.dc.v present_tb.v
      ```

   3. **Run vcs**:

      ```bash
      vcs -full64 -debug_all present_tb  # This command will generate simv executable file.
      ```

   4. **Run simv**:

      ```bash
      ./simv > simv_output.txt  # Generates sbox_vcd.vcd file, used in px_sbox.tcl.
      ```

   5. **Run primetime** (make sure all paths and file names are correct):

      ```bash
      pt_shell -f px_sbox.tcl
      ```
      This generates `sbox_hpc2.fsdb` file, which we need to open in custom waveview to get power traces.

   6. **Open traces using waveview**:

      ```bash
      wv sbox_hpc2.fsdb  # This command will open custom waveview.
      ```

   7. *Collect power traces in CSV format with values in ps corresponding to x in the table.*  
      For example, for `N = 166`, it will be `traces_300ps.csv`.  
      Do this for `300, 275, 240, 225, 215, 175, 85, 75 ps` by starting from step 1.

   8. **Download `present_hpc2_300ps.csv` to local and run the file:**  
      Change `file_num = hpc2` (or gadget concerned) in `tvla_parser_2d.py`.

   9. **Run TVLA**:

      ```bash
      python3 tvla_parser_2d.py
      ```
      This will generate the plots and the TVLA results in the same folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Feedback and Acknowledgment

We seek to improve the usability and expand the features in our tool. Please feel free to reach out to Nilotpola Sarma at s.nilotpola@iitg.ac.in with feedback and queries.
Apart from the authors, this code has been majorly contributed by : [Sujeet Narayan Kamble](https://github.com/SujeetKamble120).

## Citation

If you use this tool in your work, please cite our paper:

**[MaskedHLS: Domain-Specific High-Level Synthesis of Masked Cryptographic Designs](https://ieeexplore.ieee.org/abstract/document/10745861)**  
Nilotpola Sarma, Anuj Singh Thakur, and Chandan Karfa  
Presented at the INTERNATIONAL CONFERENCE ON COMPILERS, ARCHITECTURES, AND SYNTHESIS FOR EMBEDDED SYSTEMS 2024 ([Best Paper Candidate](https://2024.esweek.org/awards-2024/#:~:text=MaskedHLS%3A%20Domain%2DSpecific%20High%2DLevel%20Synthesis%20of%20Masked%20Cryptographic%20Designs%0ANilotpola%20Sarma%20%28Indian%20Institute%20of%20Technology%20Guwahati%29%2C%20Anuj%20Singh%20Thakur%20%28Indian%20Institute%20of%20Technology%20Guwahati%29%2C%20and%20Chandan%20Karfa%20%28Indian%20Institute%20of%20Technology%20Guwahati%29)) and 
Embedded System Software Competition 2024 as part of ESWEEK 2024.  

BibTeX:
```bibtex
@ARTICLE{10745861,
  author={Sarma, Nilotpola and Thakur, Anuj Singh and Karfa, Chandan},
  journal={IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems}, 
  title={MaskedHLS: Domain-Specific High-Level Synthesis of Masked Cryptographic Designs}, 
  year={2024},
  volume={43},
  number={11},
  pages={3973-3984},
  keywords={Integrated circuits;Design automation;Side-channel attacks;Hardware;Software;Registers;Optimization;High level synthesis;High-level synthesis (HLS);masking;power side-channel security;retiming},
  doi={10.1109/TCAD.2024.3447223}}


