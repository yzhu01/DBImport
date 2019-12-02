import os
def test_file_path_config():
	assert os.path.exists(os.getcwd() + "/config/file_paths.config")

def test_setting_config():
	assert os.path.exists(os.getcwd() + "/config/setting.config")
