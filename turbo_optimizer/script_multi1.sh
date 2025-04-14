#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/working_current"
export BASE_TMP_DIR=/homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/base_tmp/

	#cat /homes/dkochar/migration_project/open-source/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/specs_test/single_ended_cascode_current_mirror_initial.yaml > /homes/dkochar/migration_project/open-source/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/specs_test/single_ended_cascode_current_mirror.yaml
	
	source /homes/dkochar/.bashrc #conda for script setup
	conda activate rlenv38 #conda environment activate
	python /homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/sample/random_sample_turbo.py > /homes/dkochar/migration_project/open-source/nathan/new_folder_7nmsingle_ended_cascode_current_mirror/dummy.txt #run the actual turbo code
	conda deactivate





