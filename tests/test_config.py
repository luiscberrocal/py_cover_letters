from py_cover_letters.config import ConfigurationManager


def test_write(output_folder):
    config_file = output_folder / 'configuration.toml'
    config_file.unlink(missing_ok=True)

    config_manager = ConfigurationManager(output_folder)
    config = config_manager.get_sample_config()
    config_manager.write_configuration(config)

    assert config_manager.config_file.exists()
