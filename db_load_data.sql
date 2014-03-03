BEGIN TRANSACTION;

INSERT INTO "user" ([username],[email], [pwd_hash],[is_admin]) VALUES (1,'steve1373','steve1373@hotmail.com','$2a$12$/4WjJ3b9oKUVWzOwYBDlHODGtqsgvFacrUtMESVa2T2kvx.OiHNBO',true');

INSERT INTO "category" ([name],[description]) VALUES('Music','Musical talents');
INSERT INTO "category" ([name],[description]) VALUES('Software','Software development');
INSERT INTO "category" ([name],[description]) VALUES('Volunteer','Volunteer opportunities');
INSERT INTO "category" ([name],[description]) VALUES('Management','Management and coordination');
INSERT INTO "category" ([name],[description]) VALUES('Planning','Organizational and reporting skills');
INSERT INTO "category" ([name],[description]) VALUES('Education','Educational skills');

INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Harp', 'Harp Player');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Violin', 'Violin Player');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Viola', 'Viola Player');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Cello', 'Cello Player');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Bass', 'Bass Player');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Flute', 'Flutist');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Trombone', 'Bass Player');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Music'), 'Percussion', 'Percussion');

INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'User Interface', 'UI/UX design');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Web site developer', 'Web design');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Database', 'DBA');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Middleware', 'Middleware developer');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Python', 'Python');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Java', 'Java');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Node.js', 'Node.js');
INSERT INTO "skill" ([categoryID], [name], [description]) VALUES( (SELECT ID FROM category WHERE category.name='Software'), 'Node.js', 'Node.js');

COMMIT;
