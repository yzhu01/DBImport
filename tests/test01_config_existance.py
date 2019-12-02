

def test_file_path_config():
	with open('../config/file_paths.config', 'r') as f:
		assert f != NULL

def test_setting_config():
	with open('../config/setting.config', 'r') as f:
		assert f != NULL
