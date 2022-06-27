from dhp.models import FRF, PSD, TimeHistory


def test_source_to_many_derived_data_records(db_session):
    """
    Given a data object exists
    When multiple objects are derived from the data object.
    Then the derived objects are persisted on derived_data
    and the data object is persisted on the derived.source_data attribute.
    """
    time_history = TimeHistory(data=1)
    psd = PSD(data=2)
    psd_two = PSD(data=3)

    time_history.derived_data.append(psd)
    time_history.derived_data.append(psd_two)

    db_session.add(time_history)

    db_session.flush()

    db_session.expire_all()

    queried_time_history = db_session.query(TimeHistory).one()

    assert len(queried_time_history.derived_data) == 2

    for d_d in queried_time_history.derived_data:
        assert d_d.source_data[0] == queried_time_history


def test_derived_to_many_source_data_records(db_session):
    """
    When multiple objects are used to derive a data object.
    Then the source objects are persisted on source_data
    and the data object is persisted on the source.derived_data attribute.
    """
    time_history = TimeHistory(data=1)
    time_history_two = TimeHistory(data=3)
    frf = FRF(data=2)

    frf.source_data.append(time_history)
    frf.source_data.append(time_history_two)

    db_session.add(frf)

    db_session.flush()

    db_session.expire_all()

    queried_frf = db_session.query(FRF).one()

    assert len(queried_frf.source_data) == 2

    for s_d in queried_frf.source_data:
        assert s_d.derived_data[0] == queried_frf
