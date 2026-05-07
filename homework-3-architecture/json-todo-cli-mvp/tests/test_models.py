# [TODO-MVP]
import uuid

import pytest
from passlib.hash import bcrypt

from core.models import User, UserManager

pwd_context = bcrypt.using()


@pytest.fixture
def empty_manager():
    return UserManager([])


@pytest.fixture
def manager_with_user():
    raw_password = "SecurePass1!"
    hashed = pwd_context.hash(raw_password)
    manager = UserManager([])
    user = manager.create_user("testuser", hashed)
    return manager, user, raw_password


class TestCreateUser:
    def test_returns_user_object(self, empty_manager):
        user = empty_manager.create_user("alice", "hashed_pw")
        assert isinstance(user, User)

    def test_user_stored_in_list(self, empty_manager):
        user = empty_manager.create_user("alice", "hashed_pw")
        assert user.user_id in empty_manager.user_list

    def test_user_id_is_uuid(self, empty_manager):
        user = empty_manager.create_user("alice", "hashed_pw")
        assert isinstance(user.user_id, uuid.UUID)

    def test_login_is_set_correctly(self, empty_manager):
        user = empty_manager.create_user("alice", "hashed_pw")
        assert user.login == "alice"


class TestCheckLogin:
    def test_existing_login_returns_true(self, manager_with_user):
        manager, _, _ = manager_with_user
        assert manager.check_login("testuser") is True

    def test_missing_login_returns_false(self, manager_with_user):
        manager, _, _ = manager_with_user
        assert manager.check_login("ghost") is False

    def test_empty_manager_returns_false(self, empty_manager):
        assert empty_manager.check_login("nobody") is False


class TestCheckUserPassword:
    def test_correct_password_returns_true(self, manager_with_user):
        manager, _, raw_password = manager_with_user
        assert manager.check_user_password("testuser", raw_password) is True

    def test_wrong_password_returns_false(self, manager_with_user):
        manager, _, _ = manager_with_user
        assert manager.check_user_password("testuser", "WrongPass1!") is False

    def test_nonexistent_user_raises_value_error(self, empty_manager):
        with pytest.raises(ValueError):
            empty_manager.check_user_password("nobody", "AnyPass1!")


class TestDeleteUser:
    def test_delete_existing_user_removes_from_list(self, manager_with_user):
        manager, user, _ = manager_with_user
        manager.delete_user(user.user_id)
        assert user.user_id not in manager.user_list

    def test_delete_nonexistent_user_raises_value_error(self, empty_manager):
        with pytest.raises(ValueError):
            empty_manager.delete_user(uuid.uuid4())


class TestSerialization:
    def test_to_dict_returns_list(self, manager_with_user):
        manager, _, _ = manager_with_user
        assert isinstance(manager.to_dict(), list)

    def test_to_dict_entry_has_required_keys(self, manager_with_user):
        manager, _, _ = manager_with_user
        assert set(manager.to_dict()[0].keys()) == {"id", "login", "password"}

    def test_from_dict_empty_returns_empty_dict(self):
        assert UserManager.from_dict([]) == {}

    def test_roundtrip_preserves_login(self, manager_with_user):
        manager, user, _ = manager_with_user
        restored = UserManager.from_dict(manager.to_dict())
        assert restored[user.user_id].login == user.login

    def test_roundtrip_preserves_id(self, manager_with_user):
        manager, user, _ = manager_with_user
        restored = UserManager.from_dict(manager.to_dict())
        assert user.user_id in restored
