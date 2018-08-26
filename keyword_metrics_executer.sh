#!/bin/bash
echo "$(tput setaf 2) 
***************************************************************
***************************************************************
#                                                              #
#                                                              #
# Please wait while report is being generated...               #
# Converting .xml to .html file                                #
# This may take few minutes                                    #
#                                                              #
#                                                              #
***************************************************************
***************************************************************
$(tput sgr0)"

# Launch report if converstion is success
{ python keyword_metrics_report_creator.py && 
start chrome "keyword_metrics_result.html" ;} ||
cmd.exe /k