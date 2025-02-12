from sqlalchemy import text


CREATE_MAILING_GROUPS_TABLE = text("CREATE TABLE IF NOT EXISTS mailing_groups ("
                                   "group_name VARCHAR PRIMARY KEY, "
                                   "group_description VARCHAR)")

CREATE_CHAT_ROLES_TABLE = text("CREATE TABLE IF NOT EXISTS chat_roles ("
                               "role_name VARCHAR PRIMARY KEY, "
                               "role_description VARCHAR)")

CREATE_USERS_TABLE = text("CREATE TABLE IF NOT EXISTS users ("
                          "user_id INTEGER PRIMARY KEY, "
                          "user_name VARCHAR UNIQUE, "
                          "first_name VARCHAR, "
                          "last_name VARCHAR, "
                          "is_bot BOOLEAN NOT NULL, "
                          "is_subscribed BOOLEAN NOT NULL, "
                          "last_update DATETIME, "
                          "role_name VARCHAR, "
                          "FOREIGN KEY (role_name) "
                          "REFERENCES chat_roles(role_name))")

CREATE_USERS_MAILING_GROUPS_TABLE = text('CREATE TABLE IF NOT EXISTS users_mailing_groups ('
                                         'user_id INTEGER,'
                                         'group_name INTEGER,'
                                         'PRIMARY KEY (user_id, group_name),'
                                         'FOREIGN KEY (user_id) REFERENCES users(user_id),'
                                         'FOREIGN KEY (group_name) REFERENCES mailing_groups(group_name))')

SELECT_GROUPS_NUMBER = text("SELECT count(*) AS mailing_groups_number FROM mailing_groups")

SELECT_ROLES_NUMBER = text("SELECT count(*) AS roles_number FROM chat_roles")

ADD_GROUP_NAME_DESCRIPTION = text("INSERT INTO mailing_groups (group_name, group_description)"
                                  "VALUES (:group_name, :group_description)")

ADD_GROUP_NAME = text("INSERT INTO mailing_groups(group_name) "
                      "VALUES (:group_name)")

DELETE_GROUP = text("DELETE FROM mailing_groups "
                    "WHERE group_name = :group_name")

SELECT_GROUP_DESCRIPTION = text("SELECT group_description "
                                "FROM mailing_groups "
                                "WHERE group_name = :group_name")

ADD_CHAT_ROLE_DESCRIPTION = text("INSERT INTO chat_roles (role_name, role_description) "
                                 "VALUES (:chat_role, :role_description)")

ADD_CHAT_ROLE = text("INSERT INTO chat_roles(role_name) "
                     "VALUES (:chat_role)")

DELETE_CHAT_ROLE = text("DELETE FROM chat_roles "
                        "WHERE role_name = :chat_role")

SELECT_ROLE_DESCRIPTION = text("SELECT role_description "
                               "FROM chat_roles "
                               "WHERE role_name = :chat_role")

ADD_USER = text("INSERT INTO users(user_id, user_name, first_name, last_name, is_bot, is_subscribed, last_update, role_name) "
                "VALUES (:user_id, :user_name, :first_name, :last_name, :is_bot, :is_subscribed, :last_update, :role_name)")

ADD_USER_TO_MAILING_GROUP = text("INSERT INTO users_mailing_groups(user_id, group_name) VALUES (:user_id, :group_name)")

UPDATE_SUBSCRIPTION = text("UPDATE users SET is_subscribed = :is_subscribed WHERE user_id = :user_id")

SELECT_ALL_USERS = text("SELECT * FROM users")

SELECT_USER_GROUPS = text("SELECT group_name FROM users_mailing_groups WHERE user_id = :user_id")

SELECT_USER_BY_ID = text("SELECT * FROM users WHERE user_id = :user_id")

REMOVE_USER_FROM_MAILING_GROUP = text("DELETE FROM users_mailing_groups WHERE user_id = :user_id AND group_name = :group_name")

DELETE_USER = text("DELETE FROM users WHERE user_id = :user_id")

UPDATE_USER_ROLE = text("UPDATE users SET role_name = :role_name WHERE user_id = :user_id")

SELECT_ALL_MAILING_GROUPS = text("SELECT * FROM mailing_groups")
