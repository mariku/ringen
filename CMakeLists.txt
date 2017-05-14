#-------------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.5)

#-------------------------------------------------------------------------------

function(test config_file output_dir filename_prefix)
    add_executable(${filename_prefix}
        ${output_dir}/${filename_prefix}.c
        ${output_dir}/${filename_prefix}test.c
        ${output_dir}/${filename_prefix}test_runner.c
    )
    add_custom_target(generate_${filename_prefix}
        COMMAND
            python3 ${CMAKE_CURRENT_LIST_DIR}/reader.py -i ${config_file} -o ${output_dir}
        DEPENDS 
            ${config_file}
    )
    add_custom_target(generate_test_runner_${filename_prefix}
        COMMAND
        python3 ${CMAKE_CURRENT_LIST_DIR}/create_test_runner.py generate ${output_dir}/${filename_prefix}test.c -o ${output_dir}/${filename_prefix}test_runner.c --doxygen-dir ${output_dir}/doxygen
        DEPENDS 
            generate_${filename_prefix}
    )

    set_source_files_properties(${output_dir}/${filename_prefix}.c GENERATED)
    set_source_files_properties(${output_dir}/${filename_prefix}test.c GENERATED)
    set_source_files_properties(${output_dir}/${filename_prefix}test_runner.c GENERATED)
    add_dependencies(${filename_prefix} generate_${filename_prefix})
    add_dependencies(${filename_prefix} generate_test_runner_${filename_prefix})
endfunction()

#-------------------------------------------------------------------------------

include_directories(test_files/01)
include_directories(.)

test(${CMAKE_CURRENT_LIST_DIR}/test_files/01/ring.py 
    test_files/01/out
    Logging_rb_
)
