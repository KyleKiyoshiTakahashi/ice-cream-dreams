-- INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) 
-- VALUES("JON", "JONES", "jj@gmail.com", "12345678", NOW(), NOW());

-- INSERT INTO users(first_name, last_name, email, password, created_at, updated_at) 
-- VALUES("Bob", "BONES", "bb@gmail.com", "12345678", NOW(), NOW());

-- INSERT INTO ice_cream_flavors( user_id, name, description, created_at, updated_at)
-- VALUES("1", "Jon's Vanilla", "tastes like jon", NOW(), NOW());

-- SELECT * FROM ice_cream_flavors LEFT JOIN users ON  ice_cream_flavors.id = users.id;

-- INSERT INTO ice_cream_flavors(user_id, name, description, created_at, updated_at) VALUES( 2,"BoB's Vanilla", "tastes like Bob", NOW(), NOW());





-- SELECT * FROM ice_cream_flavors;

-- INSERT INTO likes(user_id, ice_cream_flavor_id, created_at, updated_at) VALUES(1, 3, NOW(), NOW());

-- SELECT * FROM likes;

DELETE FROM likes WHERE likes.id = user_id