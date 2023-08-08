import pupil_labs.real_time_screen_gaze as this_project


def test_package_metadata() -> None:
    assert hasattr(this_project, "__version__")
