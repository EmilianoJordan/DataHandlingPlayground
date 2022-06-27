import numpy as np
import pandas as pd
import pytest

from dhp.models import FRF, PSD, Data, TestData, TimeHistory


@pytest.mark.parametrize("model_class", [Data, PSD, TestData, TimeHistory, FRF])
def test_data_model_polymorphism_data_query(model_class, db_session):
    """
    When a polymorphic class of Data is used to persist to the db
    And the Data class is used to query
    Then the polymorphic subclass is returned.
    """
    data_obj = model_class(data=1)

    db_session.add(data_obj)

    db_session.flush()

    id = data_obj.id

    db_session.expire_all()

    loaded_data_object = db_session.query(Data).filter(Data.id == id).one()

    assert isinstance(loaded_data_object, model_class)


@pytest.mark.parametrize("model_class", [Data, PSD, TestData, TimeHistory, FRF])
def test_data_model_polymorphism(model_class, db_session):
    """
    When a polymorphic class of Data is used to persist to the db
    And the subclass class is used to query
    Then the polymorphic subclass is returned.
    """
    data_obj = model_class(data=1)

    db_session.add(data_obj)

    db_session.flush()

    id = data_obj.id

    db_session.expire_all()

    loaded_data_object = (
        db_session.query(model_class).filter(model_class.id == id).one()
    )

    assert isinstance(loaded_data_object, model_class)


@pytest.mark.parametrize("model_class", [PSD, TestData, TimeHistory, FRF])
def test_data_model_polymorphism_filtering(model_class, db_session):
    """
    When a polymorphic class of Data is used to persist to the db
    And the subclass class is used to query
    Then only objects of the subclass are returned.
    """
    db_session.add(Data(data=1))

    data_obj = model_class(data=1)

    db_session.add(data_obj)

    db_session.flush()

    db_session.expire_all()

    assert db_session.query(model_class).count() == 1


def test_data_model_pandas_dataframe_persistence(db_session):
    """
    When a Data object is persisted
    And is loaded
    Then the pandas dataframe stored as Data.data is loaded as a dataframe object.
    """
    # This is an incomplete test, if I was going to use this type of pickle storage
    # I would test more than just integer dataframes. Large float values, and complex
    # number would be a good place to start. I'd also install hypothesis and get some
    # help with what to test.
    df = pd.DataFrame(np.random.randint(0, 10, (2, 2)))

    data_obj = Data(data=df)

    db_session.add(data_obj)

    db_session.flush()

    db_session.expire_all()

    loaded_data_obj = db_session.query(Data).filter(Data.id == data_obj.id).one()

    assert df.equals(loaded_data_obj.data)
