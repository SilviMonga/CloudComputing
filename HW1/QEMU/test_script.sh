#!/bin/bash

TestScenarios=(
    "cpu --cpu-max-prime=30000"
    "cpu --cpu-max-prime=50000"
    "memory --memory-block-size=2K"
    "memory --memory-block-size=4K"
    "fileio --file-test-mode=rndrw --file-total-size=3G"
    "fileio --file-test-mode=seqwr --file-total-size=3G"
)

# Iterate over test scenarios
for scenario in "${TestScenarios[@]}"; do
    read -r mode parameter value <<<"$scenario"
    echo "Executing sysbench with Mode: $mode, Parameter: $parameter, Value: $value"
    
    output_filename="${mode}${parameter}${value// /}.txt"

    if [[ $mode == "fileio" ]]; then
        sysbench fileio --file-total-size=3G --time=30 $parameter prepare
    fi

    for ((run_number=1; run_number<=5; run_number++)); do
        echo "Run $run_number:" | tee -a "$output_filename"
        echo "Command: sysbench $mode $parameter $value run" >> "$output_filename"
        results=$(sysbench $mode $parameter $value --time=30 run)
        echo "Results:" | tee -a "$output_filename"
        echo "$results" | tee -a "$output_filename"
        echo "----------------------------------------"| tee -a "$output_filename"
    done

    if [[ $mode == "fileio" ]]; then
        sysbench fileio --file-total-size=3G --time=30 $parameter cleanup
    fi
done
