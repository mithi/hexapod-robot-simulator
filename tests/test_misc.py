from settings import (
    DEBUG_MODE,
    ASSERTION_ENABLED,
    PRINT_IK_LOCAL_LEG,
    PRINT_IK,
    PRINT_MODEL_ON_UPDATE,
    RECOMPUTE_HEXAPOD,
)


def test_deploy_minimum():
    assert not DEBUG_MODE
    assert not ASSERTION_ENABLED
    assert not PRINT_IK_LOCAL_LEG
    assert not PRINT_IK
    assert not PRINT_MODEL_ON_UPDATE
    assert RECOMPUTE_HEXAPOD
