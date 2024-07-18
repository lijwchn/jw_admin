INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (1, 'system', 'lijw', '2024-07-09 00:08:17.416659', '2024-06-25 23:10:17.000000', 'Setting', '系统管理', 0, 1,
        '/system', 1, NULL, 5);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (2, 'system', 'lijw', '2024-07-08 15:20:54.760842', '2024-06-04 23:17:32.000000', '', '菜单管理', 0, 2,
        '/system/menu', 1, 1, 2);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (3, 'system', 'lijw', '2024-07-08 09:50:28.931578', '2024-06-04 23:18:42.000000', '', '角色管理', 0, 2,
        '/system/role', 1, 1, 2);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (4, 'system', 'lijw', '2024-07-09 00:09:02.739579', '2024-06-11 23:20:10.000000', 'Promotion', '常用工具', 0, 1,
        '/tools', 1, NULL, 1);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (5, 'system', 'lijw', '2024-07-09 00:09:18.813253', '2024-06-18 23:21:06.000000', '', '条形码', 0, 2,
        '/tools/barcode', 1, 4, 1);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (6, 'system', 'lijw', '2024-07-08 09:50:43.042378', '2024-06-11 11:13:28.000000', '', '部门管理', 0, 2,
        '/system/dept', 1, 1, 5);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (7, 'system', 'lijw', '2024-07-08 15:20:44.965722', '2024-06-11 11:13:28.000000', '', '用户管理', 0, 2,
        '/system/user', 1, 1, 1);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (8, 'lijw', 'lijw', '2024-07-09 12:44:22.597821', '2024-07-09 12:42:44.262762', '', '条形码生成', 0, 2,
        '/tools/create_barcode', 1, 4, 2);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (9, 'lijw', 'lijw', '2024-07-10 20:09:45.882014', '2024-07-10 20:08:29.203017', 'Compass', '学习菜单', 0, 1,
        '/learn', 1, NULL, 5);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (10, 'lijw', 'lijw', '2024-07-10 21:58:26.991799', '2024-07-10 20:09:14.026712', '', '菜单demo1', 0, 2,
        '/learn/demo1', 1, 9, 1);
INSERT INTO `ninja_demo`.`system_menu` (`id`, `creator`, `updater`, `update_time`, `create_time`, `icon`, `title`,
                                        `is_ext`, `type`, `path`, `status`, `parent_id`, `order`)
VALUES (11, 'lijw', 'lijw', '2024-07-10 21:58:47.314152', '2024-07-10 21:58:47.314152', '', '菜单demo2', 0, 2,
        '/learn/demo2', 1, 9, 2);


INSERT INTO `ninja_demo`.`system_role` (`id`, `creator`, `updater`, `update_time`, `create_time`, `name`, `code`,
                                        `status`, `remark`)
VALUES (1, 'sys', 'lijw', '2024-07-18 01:06:40.547571', '2024-06-11 16:59:03.000000', '领导', 'tester_leader', 1,
        '总监的角色');


INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (1, 1, 1);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (2, 1, 2);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (3, 1, 3);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (4, 1, 4);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (5, 1, 5);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (6, 1, 6);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (7, 1, 7);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (8, 1, 8);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (9, 1, 9);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (10, 1, 10);
INSERT INTO `ninja_demo`.`system_role_menu` (`id`, `role_id`, `menu_id`)
VALUES (11, 1, 11);

INSERT INTO `ninja_demo`.`system_users_role` (`id`, `users_id`, `role_id`)
VALUES (1, 1, 1);