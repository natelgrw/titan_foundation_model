#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:/homes/natelgrw/Documents/titan_foundation_model/turbo_optimizer/working_current"
export BASE_TMP_DIR="/homes/natelgrw/Documents/titan_foundation_model/results"
	#cat /homes/dkochar/migration_project/open-source/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/specs_test/single_ended_cascode_current_mirror_initial.yaml > /homes/dkochar/migration_project/open-source/new_folder_7nmsingle_ended_cascode_current_mirror/working_current/eval_engines/spectre/specs_test/single_ended_cascode_current_mirror.yaml
	
	source /homes/natelgrw/.bashrc #conda for script setup
	conda activate rlenv38 #conda environment activate
	python /homes/natelgrw/Documents/titan_foundation_model/turbo_optimizer/working_current/sample/random_sample_turbo.py #run the actual turbo code
	conda deactivate





