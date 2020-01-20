-- 1. Select, for each boat, the sailor who made the highest number of reservations for that boat

SELECT DISTINCT b.bid, s.sname, count(*) as rank
FROM boats b join reserves r on b.bid = r.bid
JOIN sailors s on s.sid = r.sid
GROUP BY b.bid, b.bname, s.sid, s.sname
HAVING count(*) >= all(
                        SELECT count(*)
                        FROM reserves r1
                        WHERE r1.bid = b.bid
                        GROUP BY r1.sid
                      )
ORDER BY b.bid, s.sname;

-- 2. List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved (list the id and the name).
SELECT b.bid, b.bname, count(r.bid) as reserve_cnt
FROM boats b join reserves r
ON b.bid = r.bid
GROUP BY r.bid;

-- 3. List those sailors who have reserved every red boat (list the id and the name).
SELECT s.sid, s.sname, r.bid
FROM sailors s join reserves r
ON s.sid  = r.sid
WHERE r.bid = ALL (
    SELECT b.bid FROM boats b
    WHERE b.color = 'red'
);

-- 4.	List those sailors who have reserved only red boats.
SELECT DISTINCT s.sid, s.sname
FROM sailors as s 
WHERE 'red'= ALL (
    SELECT b.color FROM boats b join reserves r 
    ON b.bid = r.bid where r.sid = s.sid
) AND s.sid IN (
    SELECT r.sid FROM reserves r
);

-- 5.	For which boat are there the most reservations?
SELECT b.bid, b.bname, count(*)
FROM boats as b join reserves as r 
ON b.bid = r.bid
GROUP BY b.bid, b.bname
ORDER BY count(*) DESC
LIMIT 1;

-- 6.	Select all sailors who have never reserved a red boat.
SELECT s.sid, s.sname
FROM sailors as s
LEFT JOIN (
    reserves as r
    INNER JOIN boats as b
    ON r.bid = b.bid AND b.color='red'
    )
ON s.sid = r.sid
WHERE b.color IS NULL;

-- 7.	Find the average age of sailors with a rating of 10.
SELECT AVG(s.age) 
FROM sailors as s 
WHERE s.rating = 10
GROUP BY age;