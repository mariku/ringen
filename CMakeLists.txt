#-------------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.5)

#-------------------------------------------------------------------------------

function(test config_file output_dir prefix)
    add_executable(${prefix}
        ${output_dir}/${prefix}.c
        ${output_dir}/${prefix}_test.c
        ${output_dir}/${prefix}_test_runner.c
    )
    add_custom_target(generate_${prefix}
        COMMAND
            python3 ${CMAKE_CURRENT_LIST_DIR}/reader.py -i ${config_file} -o ${output_dir}
        DEPENDS 
            ${config_file}
    )
    add_custom_target(generate_test_runner_${prefix}
        COMMAND
        python3 ${CMAKE_CURRENT_LIST_DIR}/create_test_runner.py generate ${output_dir}/${prefix}_test.c -o ${output_dir}/${prefix}_test_runner.c --doxygen-dir ${output_dir}/doxygen
        DEPENDS 
            generate_${prefix}
    )

    set_source_files_properties(${output_dir}/${prefix}.c GENERATED)
    set_source_files_properties(${output_dir}/${prefix}_test.c GENERATED)
    set_source_files_properties(${output_dir}/${prefix}_test_runner.c GENERATED)
    add_dependencies(${prefix} generate_${prefix})
    add_dependencies(${prefix} generate_test_runner_${prefix})
endfunction()

#-------------------------------------------------------------------------------

include_directories(test_files/01)
include_directories(.)

test(${CMAKE_CURRENT_LIST_DIR}/test_files/01/ring.py 
    test_files/01/out
    Logging_rb
)
