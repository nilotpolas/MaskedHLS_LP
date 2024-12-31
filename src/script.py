# Copyright (c) 2024 AVS LAB, IIT Guwahati
# All rights reserved.
# 
# Authors:
# Chandan Karfa, Nilotpola Sarma
# 
# This software is licensed under the terms of the MIT License.
# See the LICENSE file for details.
#
# For queries or feedback, please contact:
# Nilotpola Sarma (s.nilotpola@iitg.ac.in)
# 
# This code is provided "as is" without warranty of any kind, express or implied,
# including but not limited to the warranties of merchantability, fitness for a particular
# purpose, and noninfringement. In no event shall the authors or copyright holders be
# liable for any claim, damages, or other liability, whether in an action of contract,
# tort, or otherwise, arising from, out of, or in connection with the software or the use
# or other dealings in the software.
import subprocess
import sys
import json
sys.path.extend(['.', '..'])
import argparse
import os

#constants
TEMP_FILES_DIR = "tempFiles"
INLINER_OUTPUT_FILE = TEMP_FILES_DIR + "/inlinerOut.c"
RETIMED_OUTPUT = TEMP_FILES_DIR + "/retimedOut.c"
POST_PROCESSOR_OUTPUT = TEMP_FILES_DIR + "/postProcessedOut.c"
GENERATED_RTL = "/rtl.v"

def run_script(script):
    subprocess.run(['python', script])

def main():
    if not os.path.exists(TEMP_FILES_DIR):
    # Create the directory
        os.makedirs(TEMP_FILES_DIR)
    a = 1
    argparser = argparse.ArgumentParser()
    #argument for the top module
    argparser.add_argument('--topModule',
                           default='none',
                           nargs='?',
                           help='The top module of design')
    #argument for input file
    argparser.add_argument('--inputFile',
                           default='none',
                           nargs='?',
                           help='name of the balanced design')
    #argument for output file
    argparser.add_argument('--rtlFile',
                           default='./output.v',
                           nargs='?',
                           help='name of the balanced design')
    #argument for bit width
    argparser.add_argument('--bitWidth',
                           default='1',
                           nargs='?',
                           help='specify the bit-width for the rtl file')
    #to verify the balancing
    argparser.add_argument('--checkBalancing',
                            default='0',
                            nargs='?',
                            help='Whether or not to verify the balancing')
    
    args = argparser.parse_args()
    #check of mandatory arguments
    if(args.topModule == 'None'):
        print("Fatal error : Top module not specified")
        sys.exit(1)
    if(args.inputFile == 'None'):
        print("Fatal error : Input file not specified")
        sys.exit(1)

    systemArgs = {
        "topModule": args.topModule,
        "inputFile": args.inputFile,
        "generatedRtl": args.rtlFile,
        "bitWidth": int(args.bitWidth),
        "inlinerOutput" : INLINER_OUTPUT_FILE,
        "retimedOutput" : RETIMED_OUTPUT,
        "postProcessorOutput" : POST_PROCESSOR_OUTPUT,
        "checkBalancing" : 0
    }

    #writing the arguments in json file
    with open('systemArgs.json', 'w') as json_file:
        json.dump(systemArgs, json_file, indent=4)
    
    #running the scripts
    run_script('./Inliner/inliner.py')
    run_script('./RegBalancer/src/main.py')
    run_script("./PostProcessor/processor.py")
    run_script("./Compiler/parser_1.py")

    systemArgs["checkBalancing"] = int(args.checkBalancing)
    with open('systemArgs.json', 'w') as json_file:
        json.dump(systemArgs, json_file, indent=4)
    run_script('./RegBalancer/src/main.py')

if __name__ == '__main__':
    main()
